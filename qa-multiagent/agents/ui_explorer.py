"""UI Explorer Agent — opens the page and extracts structured UI metadata."""

from __future__ import annotations

import logging

from graph.state import QAState
from tools.playwright_tool import extract_ui_structure

logger = logging.getLogger(__name__)


def ui_explorer_agent(state: QAState) -> dict:
    """Drive the headless browser and produce ``ui_structure``.

    Also flips ``login_required`` if a password field is present, which the
    workflow uses to route into the Login Agent.
    """
    url = state["url"]
    logger.info("UI Explorer: opening %s", url)
    try:
        structure = extract_ui_structure(url)
    except Exception as exc:  # noqa: BLE001 — surface and continue
        logger.exception("UI exploration failed")
        return {
            "ui_structure": {"error": str(exc)},
            "login_required": False,
            "current_page": url,
            "test_error": f"UI exploration failed: {exc}",
        }

    login_required = bool(structure.get("hasPasswordField"))
    logger.info(
        "UI Explorer: %d buttons / %d inputs / %d links — login_required=%s",
        len(structure.get("buttons", [])),
        len(structure.get("inputs", [])),
        len(structure.get("links", [])),
        login_required,
    )
    return {
        "ui_structure": structure,
        "login_required": login_required,
        "current_page": url,
    }
