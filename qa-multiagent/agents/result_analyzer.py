"""Result Analyzer Agent — classifies the run as passed/failed."""

from __future__ import annotations

import logging

from graph.state import QAState

logger = logging.getLogger(__name__)


def result_analyzer_agent(state: QAState) -> dict:
    """Translate exit code + captured logs into ``test_status``."""
    exit_code = state.get("test_exit_code", -1)
    if exit_code == 0:
        logger.info("Result Analyzer: PASSED")
        return {"test_status": "passed", "test_error": ""}

    combined = (
        (state.get("test_stderr") or "")
        + "\n--- stdout ---\n"
        + (state.get("test_stdout") or "")
    )
    # Tail the log so the fix prompt does not blow past context limits.
    logger.warning("Result Analyzer: FAILED (exit=%s)", exit_code)
    return {
        "test_status": "failed",
        "test_error": combined[-6000:],
    }
