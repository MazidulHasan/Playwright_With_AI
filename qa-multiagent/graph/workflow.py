"""LangGraph workflow definition + conditional routing."""

from __future__ import annotations

import logging
from pathlib import Path

from langgraph.graph import END, StateGraph

from agents.automation_agent import automation_agent
from agents.file_writer import file_writer_agent
from agents.fix_agent import fix_agent
from agents.login_agent import login_agent
from agents.manual_agent import manual_agent
from agents.result_analyzer import result_analyzer_agent
from agents.test_runner import test_runner_agent
from agents.ui_explorer import ui_explorer_agent
from graph.state import QAState
from tools.file_utils import write_text

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Conditional routing
# ---------------------------------------------------------------------------

def route_login(state: QAState) -> str:
    """After UI exploration: login if a password field exists, else manual."""
    return "login" if state.get("login_required") else "manual"


def route_test_result(state: QAState) -> str:
    """After analysis: stop on pass, stop on retry exhaustion, else fix."""
    if state.get("test_status") == "passed":
        return "save_report"
    if state.get("retry_count", 0) >= state.get("max_retries", 5):
        logger.warning("retry budget exhausted — saving failure report")
        return "save_report"
    return "fix"


# ---------------------------------------------------------------------------
# Terminal node — saves a human-readable run report
# ---------------------------------------------------------------------------

def save_report_agent(state: QAState) -> dict:
    """Final node: persist a Markdown report and finalise ``test_status``."""
    output_dir = Path(state.get("output_dir", "output"))
    status = state.get("test_status", "unknown")
    retries = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 5)
    if status != "passed" and retries >= max_retries:
        status = "max_retries_exceeded"

    report = (
        "# QA Automation Run Report\n\n"
        f"- **URL:** {state.get('url')}\n"
        f"- **Status:** {status}\n"
        f"- **Retries used:** {retries} / {max_retries}\n"
        f"- **Login required:** {state.get('login_required')}\n\n"
        "## Last stdout\n\n"
        "```\n"
        f"{(state.get('test_stdout') or '')[:6000]}\n"
        "```\n\n"
        "## Last stderr\n\n"
        "```\n"
        f"{(state.get('test_stderr') or '')[:6000]}\n"
        "```\n"
    )
    write_text(output_dir / "reports" / "report.md", report)
    return {"test_status": status}


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_graph():
    """Compile and return the QA workflow.

    Topology::

        explore -> (login | manual)
        login   -> manual
        manual  -> automation -> write_files -> run_tests -> analyze
        analyze -> save_report (pass / retries exhausted)
        analyze -> fix -> write_files -> run_tests (retry loop)
        save_report -> END
    """
    workflow = StateGraph(QAState)

    workflow.add_node("explore", ui_explorer_agent)
    workflow.add_node("login", login_agent)
    workflow.add_node("manual", manual_agent)
    workflow.add_node("automation", automation_agent)
    workflow.add_node("write_files", file_writer_agent)
    workflow.add_node("run_tests", test_runner_agent)
    workflow.add_node("analyze", result_analyzer_agent)
    workflow.add_node("fix", fix_agent)
    workflow.add_node("save_report", save_report_agent)

    workflow.set_entry_point("explore")

    workflow.add_conditional_edges(
        "explore",
        route_login,
        {"login": "login", "manual": "manual"},
    )
    workflow.add_edge("login", "manual")
    workflow.add_edge("manual", "automation")
    workflow.add_edge("automation", "write_files")
    workflow.add_edge("write_files", "run_tests")
    workflow.add_edge("run_tests", "analyze")
    workflow.add_conditional_edges(
        "analyze",
        route_test_result,
        {"fix": "fix", "save_report": "save_report"},
    )
    workflow.add_edge("fix", "write_files")
    workflow.add_edge("save_report", END)

    return workflow.compile()
