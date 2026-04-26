"""Login Agent — captures credentials when the page requires auth."""

from __future__ import annotations

import logging
import os

from graph.state import QAState

logger = logging.getLogger(__name__)


def login_agent(state: QAState) -> dict:
    """Resolve credentials for downstream automation.

    Reads ``QA_USERNAME`` / ``QA_PASSWORD`` from the environment so users
    can wire real credentials without committing them. Falls back to safe
    placeholders so the pipeline still runs end-to-end.
    """
    username = os.getenv("QA_USERNAME", "test@example.com")
    password = os.getenv("QA_PASSWORD", "Password123!")
    logger.info("Login Agent: prepared credentials for %s", username)
    return {
        "login_credentials": {
            "username": username,
            "password": password,
        }
    }
