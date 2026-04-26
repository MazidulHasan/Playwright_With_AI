"""Subprocess-based wrappers around the Playwright CLI."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from tools.process_utils import stream_run

logger = logging.getLogger(__name__)

# On Windows ``npx`` and ``npm`` ship as ``.cmd`` shims.
IS_WIN = sys.platform == "win32"
NPX = "npx.cmd" if IS_WIN else "npx"
NPM = "npm.cmd" if IS_WIN else "npm"
NODE = "node"

EXTRACT_SCRIPT = Path(__file__).resolve().parent / "extract_ui.js"


def extract_ui_structure(url: str, timeout: int = 90) -> Dict[str, Any]:
    """Open ``url`` with Playwright (Node helper) and return a JSON DOM summary.

    stdout from the helper is pure JSON, so we suppress the live stream for
    that pipe — we still tee stderr in case the helper logs warnings.
    """
    if not EXTRACT_SCRIPT.exists():
        raise FileNotFoundError(f"missing helper script: {EXTRACT_SCRIPT}")

    rc, stdout, stderr = stream_run(
        [NODE, str(EXTRACT_SCRIPT), url],
        timeout=timeout,
        label="explorer",
        stream_stdout=False,  # JSON payload — would be noise on screen
        stream_stderr=True,
    )
    if rc != 0:
        raise RuntimeError(
            f"extract_ui.js failed (exit={rc}): {stderr.strip() or stdout.strip()}"
        )
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"extract_ui.js produced non-JSON output: {stdout[:500]}"
        ) from exc


def run_playwright_tests(
    project_dir: Path | str,
    test_files: Optional[List[str]] = None,
    project: str = "chromium",
    timeout: int = 600,
) -> Tuple[int, str, str]:
    """Execute ``npx playwright test`` in ``project_dir``.

    ``test_files`` (relative to ``project_dir``) restricts the run to just the
    specs we generated, so any pre-existing ``example.spec.js`` in the user's
    project does not pollute pass/fail detection. ``--project=chromium``
    avoids running all configured browsers.
    """
    cmd: List[str] = [NPX, "playwright", "test"]
    if test_files:
        cmd.extend(test_files)
    cmd.extend([f"--project={project}", "--reporter=list"])

    rc, stdout, stderr = stream_run(
        cmd,
        cwd=project_dir,
        timeout=timeout,
        label="playwright",
    )
    return rc, stdout, stderr


def npm_install(project_dir: Path | str, timeout: int = 600) -> None:
    rc, stdout, stderr = stream_run(
        [NPM, "install"], cwd=project_dir, timeout=timeout, label="npm",
    )
    if rc != 0:
        raise RuntimeError(
            f"npm install failed: {stderr.strip() or stdout.strip()}"
        )


def install_playwright_browsers(project_dir: Path | str, timeout: int = 600) -> None:
    rc, stdout, stderr = stream_run(
        [NPX, "playwright", "install", "chromium"],
        cwd=project_dir, timeout=timeout, label="pw-install",
    )
    if rc != 0:
        raise RuntimeError(
            f"playwright install failed: {stderr.strip() or stdout.strip()}"
        )
