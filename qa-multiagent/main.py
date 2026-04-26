"""Entry point for the multi-agent QA framework.

Usage:

    python main.py https://example.com/login
    python main.py                         # prompts for URL
    python main.py <url> --max-retries 3   # cap fix-loop iterations
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from graph.workflow import build_graph

# Project layout — paths relative to this file's parent directory:
#   <repo>/
#     qa-multiagent/    <- this script
#     manualTestCases/  <- generated manual test cases land here
#     playwright/       <- pre-installed Playwright project; specs land here
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent

DEFAULT_MANUAL_DIR = REPO_ROOT / "manualTestCases"
DEFAULT_PROJECT_DIR = REPO_ROOT / "playwright"
DEFAULT_OUTPUT_DIR = HERE / "output"


def _setup_logging(verbose: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Multi-agent QA framework: explore -> generate -> run -> self-heal. "
            "Subprocess output streams live to the current terminal."
        ),
    )
    parser.add_argument("url", nargs="?", help="URL of the page to test")
    parser.add_argument(
        "--max-retries", type=int, default=5,
        help="Maximum number of fix-and-retry iterations (default: 5)",
    )
    parser.add_argument(
        "--manual-dir", default=str(DEFAULT_MANUAL_DIR),
        help=f"Directory for manual test cases (default: {DEFAULT_MANUAL_DIR})",
    )
    parser.add_argument(
        "--project-dir", default=str(DEFAULT_PROJECT_DIR),
        help=f"Existing Playwright project root (default: {DEFAULT_PROJECT_DIR})",
    )
    parser.add_argument(
        "--output", default=str(DEFAULT_OUTPUT_DIR),
        help=f"Directory for run reports (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable DEBUG-level logging",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    args = parse_args(argv)
    _setup_logging(args.verbose)
    log = logging.getLogger("main")

    url = args.url or input("Enter URL: ").strip()
    if not url:
        log.error("URL is required")
        return 2

    initial_state: dict = {
        "url": url,
        "max_retries": args.max_retries,
        "retry_count": 0,
        "manual_dir": args.manual_dir,
        "project_dir": args.project_dir,
        "output_dir": args.output,
    }

    log.info(
        "Starting QA workflow for %s (max_retries=%d)\n"
        "  manual    -> %s\n"
        "  playwright -> %s\n"
        "  reports   -> %s",
        url, args.max_retries,
        args.manual_dir, args.project_dir, args.output,
    )

    graph = build_graph()
    final_state = graph.invoke(initial_state, {"recursion_limit": 60})

    status = final_state.get("test_status", "unknown")
    retries = final_state.get("retry_count", 0)

    print()
    print("=" * 64)
    print(f" Status        : {status}")
    print(f" Retries used  : {retries} / {args.max_retries}")
    print(f" Manual tests  : {Path(args.manual_dir) / 'test_cases.md'}")
    print(f" Playwright    : {args.project_dir}")
    print(f" Report        : {Path(args.output) / 'reports' / 'report.md'}")
    print("=" * 64)

    return 0 if status == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
