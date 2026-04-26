"""Automation Test Generator Agent — produces Playwright JS files."""

from __future__ import annotations

import json
import logging
import re
from typing import Dict

from agents._llm import invoke
from graph.state import QAState
from tools.file_utils import format_prompt, read_prompt

logger = logging.getLogger(__name__)


_FILE_BLOCK = re.compile(
    r"===FILE:\s*(?P<path>[^\n=]+?)\s*===\s*\n(?P<body>.*?)(?=\n===FILE:|\Z)",
    re.DOTALL,
)
_LEAD_FENCE = re.compile(r"^```[a-zA-Z0-9_-]*\s*\n")
_TRAIL_FENCE = re.compile(r"\n```\s*$")


def parse_file_blocks(text: str) -> Dict[str, str]:
    """Parse ``===FILE: path===`` blocks emitted by the LLM into a dict.

    Tolerates accidental code-fences around individual blocks.
    """
    files: Dict[str, str] = {}
    for match in _FILE_BLOCK.finditer(text):
        path = match.group("path").strip().lstrip("./")
        body = match.group("body").strip()
        body = _LEAD_FENCE.sub("", body)
        body = _TRAIL_FENCE.sub("", body)
        if path:
            files[path] = body
    return files


def automation_agent(state: QAState) -> dict:
    """Generate Playwright spec files and Page Objects."""
    logger.info("Automation Test Generator: drafting Playwright specs")
    template = read_prompt("automation_prompt.md")
    prompt = format_prompt(
        template,
        url=state.get("url", ""),
        login_required=state.get("login_required", False),
        login_credentials=json.dumps(state.get("login_credentials", {})),
        ui_structure=json.dumps(state.get("ui_structure", {}), indent=2)[:12000],
    )
    text = invoke(prompt, temperature=0.2)
    files = parse_file_blocks(text)

    tests = {p: c for p, c in files.items() if p.startswith("tests/")}
    pages = {p: c for p, c in files.items() if p.startswith("pages/")}

    if not tests:
        logger.warning(
            "Automation Test Generator: no ===FILE: tests/...=== blocks found; "
            "writing raw output as fallback spec"
        )
        tests = {"tests/generated.spec.js": text}

    logger.info(
        "Automation Test Generator: %d spec files, %d page objects",
        len(tests), len(pages),
    )
    return {"automation_tests": tests, "page_objects": pages}
