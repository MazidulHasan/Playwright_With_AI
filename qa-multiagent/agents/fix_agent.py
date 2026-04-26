"""Fix Automation Agent — repairs failing Playwright tests."""

from __future__ import annotations

import json
import logging

from agents._llm import invoke
from agents.automation_agent import parse_file_blocks
from graph.state import QAState
from tools.file_utils import format_prompt, read_prompt

logger = logging.getLogger(__name__)


def _serialise_existing(state: QAState) -> str:
    parts: list[str] = []
    for path, content in (state.get("automation_tests") or {}).items():
        parts.append(f"===FILE: {path}===\n{content}\n")
    for path, content in (state.get("page_objects") or {}).items():
        parts.append(f"===FILE: {path}===\n{content}\n")
    return "\n".join(parts)


def fix_agent(state: QAState) -> dict:
    """Regenerate corrected files based on the failure log."""
    retry = state.get("retry_count", 0)
    logger.info("Fix Agent: repairing tests (retry %d)", retry)
    template = read_prompt("fix_prompt.md")
    prompt = format_prompt(
        template,
        url=state.get("url", ""),
        ui_structure=json.dumps(state.get("ui_structure", {}), indent=2)[:8000],
        existing_files=_serialise_existing(state),
        error_log=state.get("test_error", "")[-4000:],
    )
    text = invoke(prompt, temperature=0.1)
    fixes = parse_file_blocks(text)

    if not fixes:
        logger.warning("Fix Agent: no file blocks parsed — leaving files untouched")
        return {}

    tests = dict(state.get("automation_tests") or {})
    pages = dict(state.get("page_objects") or {})

    for path, content in fixes.items():
        if path.startswith("tests/"):
            tests[path] = content
        elif path.startswith("pages/"):
            pages[path] = content
        else:
            # Drop into tests/ by default — keeps the project shape stable.
            tests[f"tests/{path.split('/')[-1]}"] = content

    logger.info("Fix Agent: rewrote %d files", len(fixes))
    return {"automation_tests": tests, "page_objects": pages}
