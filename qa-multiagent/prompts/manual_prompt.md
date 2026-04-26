You are a senior QA engineer. Analyze the page UI structure below and produce comprehensive **manual** test cases.

URL: {url}
Login required: {login_required}

UI Structure (JSON):
{ui_structure}

## Coverage requirements

Generate **15–30** test cases distributed across these categories:

- **Positive** — happy-path flows that should succeed
- **Negative** — invalid input, missing data, wrong order of operations
- **Validation** — field-level rules (required, format, length, type)
- **Navigation** — links, redirects, back/forward, deep links
- **Boundary** — edge values: empty, max length, min/max numeric, special chars

## Strict format

Each test case **must** follow this structure:

### TC-001 — Short descriptive title

**Category:** Positive | Negative | Validation | Navigation | Boundary

**Preconditions:** What must be true before this test starts.

**Steps:**
1. First action.
2. Second action.
3. ...

**Expected Result:** What the user should observe after the final step.

---

## Output rules

- Output **Markdown only**.
- Do **not** wrap the whole response in code fences.
- Number test cases sequentially: TC-001, TC-002, ...
- Be specific about which UI element each step interacts with — reference the labels, placeholders, ids, or aria-labels visible in the UI Structure JSON.
- If the page has a login form, dedicate at least 4 test cases to authentication scenarios.
