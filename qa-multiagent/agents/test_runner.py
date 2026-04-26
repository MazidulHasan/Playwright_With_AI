"""Test Runner Agent — executes Playwright tests and captures output."""

from __future__ import annotations

import logging
from pathlib import Path

from graph.state import QAState
from tools.playwright_tool import run_playwright_tests

logger = logging.getLogger(__name__)


def test_runner_agent(state: QAState) -> dict:
    """Run ``npx playwright test`` restricted to the specs we generated.

    Restricting to our own files keeps any pre-existing tests in the user's
    project (e.g. the default ``example.spec.js``) from polluting pass/fail
    detection.
    """
    project_dir = Path(state.get("project_dir", "playwright"))
    retry_count = state.get("retry_count", 0)
    test_files = list((state.get("automation_tests") or {}).keys())

    logger.info(
        "Test Runner: %d spec(s) in %s (attempt %d)",
        len(test_files), project_dir, retry_count + 1,
    )

    try:
        exit_code, stdout, stderr = run_playwright_tests(
            project_dir,
            test_files=test_files or None,
            project="chromium",
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Playwright invocation failed")
        return {
            "test_exit_code": -1,
            "test_stdout": "",
            "test_stderr": f"Runner exception: {exc}",
            "retry_count": retry_count + 1,
        }

    logger.info("Test Runner: exit_code=%s", exit_code)
    return {
        "test_exit_code": exit_code,
        "test_stdout": stdout,
        "test_stderr": stderr,
        "retry_count": retry_count + 1,
    }
