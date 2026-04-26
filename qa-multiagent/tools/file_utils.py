"""Filesystem and prompt-loading helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def ensure_dir(path: Union[str, Path]) -> Path:
    """Create the directory (and parents) if it does not already exist."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_text(path: Union[str, Path], content: str) -> Path:
    """Write text to ``path``, creating parent directories as needed."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    logger.info("wrote %s (%d bytes)", p, len(content))
    return p


def read_prompt(name: str) -> str:
    """Load a prompt template from ``prompts/<name>``."""
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def format_prompt(template: str, **kwargs) -> str:
    """Substitute ``{var}`` placeholders without using ``str.format``.

    Using plain ``.replace`` avoids having to escape every ``{`` / ``}`` in
    the example code embedded in our prompt templates.
    """
    out = template
    for key, value in kwargs.items():
        out = out.replace("{" + key + "}", str(value))
    return out
