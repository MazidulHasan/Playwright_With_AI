"""Shared LangGraph state for the multi-agent QA pipeline."""

from typing import TypedDict, Dict, Any


class QAState(TypedDict, total=False):
    """State container threaded through every node in the workflow."""

    # --- input / context ---
    url: str
    current_page: str
    output_dir: str        # where reports go
    manual_dir: str        # where the manual test-case markdown goes
    project_dir: str       # the (pre-existing) Playwright project root

    # --- exploration ---
    ui_structure: Dict[str, Any]
    login_required: bool
    login_credentials: Dict[str, str]

    # --- generated artifacts ---
    manual_tests: str
    automation_tests: Dict[str, str]   # relative path -> file content
    page_objects: Dict[str, str]       # relative path -> file content

    # --- execution / analysis ---
    test_exit_code: int
    test_stdout: str
    test_stderr: str
    test_status: str   # "passed" | "failed" | "max_retries_exceeded"
    test_error: str

    # --- retry control ---
    retry_count: int
    max_retries: int
