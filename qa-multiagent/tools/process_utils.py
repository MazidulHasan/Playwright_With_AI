"""Subprocess helper that streams stdout/stderr live while still capturing them."""

from __future__ import annotations

import logging
import subprocess
import sys
import threading
from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

logger = logging.getLogger(__name__)


def stream_run(
    cmd: Sequence[str],
    *,
    cwd: Optional[Union[str, Path]] = None,
    input_data: Optional[str] = None,
    timeout: int = 600,
    label: Optional[str] = None,
    stream_stdout: bool = True,
    stream_stderr: bool = True,
) -> Tuple[int, str, str]:
    """Run ``cmd`` as a subprocess and tee its output to the current terminal.

    Each line of stdout / stderr is printed with an optional ``[label]``
    prefix so the user sees what the spawned process is doing in real time
    (the "live log of other terminals"). The full output is also accumulated
    and returned so downstream code can parse it.

    Returns ``(exit_code, stdout_str, stderr_str)``.
    """
    logger.debug("$ %s (cwd=%s)", " ".join(cmd), cwd)
    proc = subprocess.Popen(
        list(cmd),
        cwd=str(cwd) if cwd else None,
        stdin=subprocess.PIPE if input_data is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    if input_data is not None and proc.stdin is not None:
        try:
            proc.stdin.write(input_data)
        finally:
            proc.stdin.close()

    stdout_buf: list[str] = []
    stderr_buf: list[str] = []
    prefix_out = f"[{label}] " if label else ""
    prefix_err = f"[{label}:err] " if label else ""

    def _drain(pipe, buf, prefix, do_stream):
        try:
            for line in iter(pipe.readline, ""):
                buf.append(line)
                if do_stream:
                    sys.stdout.write(prefix + line)
                    sys.stdout.flush()
        finally:
            try:
                pipe.close()
            except Exception:  # noqa: BLE001
                pass

    t_out = threading.Thread(
        target=_drain,
        args=(proc.stdout, stdout_buf, prefix_out, stream_stdout),
        daemon=True,
    )
    t_err = threading.Thread(
        target=_drain,
        args=(proc.stderr, stderr_buf, prefix_err, stream_stderr),
        daemon=True,
    )
    t_out.start()
    t_err.start()

    try:
        rc = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        raise

    t_out.join(timeout=5)
    t_err.join(timeout=5)

    return rc, "".join(stdout_buf), "".join(stderr_buf)
