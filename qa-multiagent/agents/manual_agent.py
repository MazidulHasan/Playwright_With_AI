"""Manual Test Generator Agent."""

from __future__ import annotations

import json
import logging

from agents._llm import invoke
from graph.state import QAState
from tools.file_utils import format_prompt, read_prompt

logger = logging.getLogger(__name__)


def manual_agent(state: QAState) -> dict:
    """Produce a Markdown document of manual test cases."""
    logger.info("Manual Test Generator: drafting test cases")
    template = read_prompt("manual_prompt.md")
    prompt = format_prompt(
        template,
        url=state.get("url", ""),
        login_required=state.get("login_required", False),
        ui_structure=json.dumps(state.get("ui_structure", {}), indent=2)[:12000],
    )
    text = invoke(prompt, temperature=0.3)
    logger.info("Manual Test Generator: produced %d chars", len(text))
    return {"manual_tests": text}
