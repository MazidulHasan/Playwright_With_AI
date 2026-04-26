"""Backend-agnostic text generation. Default: Claude Code CLI (no API key).

Each call to :func:`invoke` spawns a fresh ``claude -p`` subprocess, pipes
the prompt through stdin, **streams the response live to the parent
terminal**, and returns the captured stdout. This uses the user's existing
Claude Code authentication — no ANTHROPIC_API_KEY is required.

Set ``QA_BACKEND=api`` to use the langchain-anthropic ChatAnthropic client
instead (requires ANTHROPIC_API_KEY and the optional dependency).
"""

from __future__ import annotations

import logging
import os
import shutil
import sys

from tools.process_utils import stream_run

logger = logging.getLogger(__name__)

CLAUDE_BIN = "claude.cmd" if sys.platform == "win32" else "claude"


def _find_claude() -> str:
    candidate = shutil.which(CLAUDE_BIN) or shutil.which("claude")
    if not candidate:
        raise RuntimeError(
            "Claude Code CLI not found on PATH. Install it with:\n"
            "  npm install -g @anthropic-ai/claude-code\n"
            "then run `claude` once interactively to authenticate."
        )
    return candidate


def _invoke_cli(prompt: str, timeout: int = 600,
                label: str = "claude") -> str:
    """One-shot text generation via ``claude -p`` with live output streaming."""
    binary = _find_claude()
    logger.info("Claude CLI: invoking (prompt %d chars)", len(prompt))

    if os.getenv("QA_DEBUG_PROMPT"):
        snippet = prompt[:2000].replace("\r", "")
        logger.debug("---- prompt (first 2000 chars) ----\n%s\n---- end ----", snippet)

    rc, stdout, stderr = stream_run(
        [binary, "-p", "--output-format", "text"],
        input_data=prompt,
        timeout=timeout,
        label=label,
        stream_stdout=True,
        stream_stderr=True,
    )

    if rc != 0:
        raise RuntimeError(
            f"Claude CLI failed (exit={rc}). stderr:\n{(stderr or '').strip()[:1500]}"
        )
    logger.info("Claude CLI: received %d chars", len(stdout))
    return stdout


def _invoke_api(prompt: str, temperature: float, max_tokens: int,
                timeout: int) -> str:
    """Fallback path that hits the Anthropic API directly (lazy import)."""
    try:
        from langchain_anthropic import ChatAnthropic  # noqa: WPS433
    except ImportError as exc:
        raise RuntimeError(
            "QA_BACKEND=api requires `pip install langchain-anthropic`."
        ) from exc

    model = os.getenv("QA_MODEL", "claude-sonnet-4-6")
    llm = ChatAnthropic(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
    )
    response = llm.invoke(prompt)
    content = getattr(response, "content", response)
    if isinstance(content, list):
        return "".join(
            (b.get("text", "") if isinstance(b, dict) else str(b)) for b in content
        )
    return str(content)


def invoke(prompt: str,
           *,
           temperature: float = 0.2,
           max_tokens: int = 8192,
           timeout: int = 600,
           label: str = "claude") -> str:
    """Send ``prompt`` to the configured backend and return text.

    ``label`` prefixes streamed CLI output (e.g. ``[manual]``, ``[fix]``)
    so the user can tell which agent is talking when running with verbose
    log streaming enabled.
    """
    backend = os.getenv("QA_BACKEND", "cli").lower()
    if backend == "api":
        return _invoke_api(prompt, temperature, max_tokens, timeout)
    return _invoke_cli(prompt, timeout=timeout, label=label)
