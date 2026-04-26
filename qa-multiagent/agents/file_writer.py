"""File Writer Agent — persists artifacts into the user's existing folders."""

from __future__ import annotations

import logging
from pathlib import Path

from graph.state import QAState
from tools.file_utils import write_text

logger = logging.getLogger(__name__)


def file_writer_agent(state: QAState) -> dict:
    """Write manual + automation artifacts to the configured directories.

    Layout:
      - manual_dir/test_cases.md
      - project_dir/tests/<spec>.js
      - project_dir/pages/<page>.js

    The Playwright project (``project_dir``) is assumed to be pre-installed
    and configured by the user; we do **not** scaffold ``package.json`` /
    ``playwright.config.js`` and we do **not** run ``npm install`` here.
    """
    manual_dir = Path(state.get("manual_dir", "manualTestCases"))
    project_dir = Path(state.get("project_dir", "playwright"))

    logger.info(
        "File Writer: manual=%s  project=%s",
        manual_dir, project_dir,
    )

    if state.get("manual_tests"):
        write_text(manual_dir / "test_cases.md", state["manual_tests"])

    for rel_path, content in (state.get("automation_tests") or {}).items():
        write_text(project_dir / rel_path, content)
    for rel_path, content in (state.get("page_objects") or {}).items():
        write_text(project_dir / rel_path, content)

    if not project_dir.exists():
        logger.error("File Writer: project_dir %s does not exist", project_dir)
        return {"test_error": f"project_dir does not exist: {project_dir}"}

    return {}
