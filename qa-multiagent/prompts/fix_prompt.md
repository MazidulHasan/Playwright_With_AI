You are a Playwright debugging expert. The tests below failed. Analyze the error log and regenerate the necessary files with **minimal targeted fixes**.

URL under test: {url}

UI Structure (current page):
{ui_structure}

Existing test files:
{existing_files}

Playwright error log (tail):
{error_log}

## Diagnosis checklist

Work through these in order; the first matching cause is usually the right one:

1. **Locator mismatch** — the selector does not resolve. Cross-reference the UI Structure JSON and switch to a more robust locator (`getByRole` with name, `getByLabel`, `getByPlaceholder`, `getByTestId`).
2. **Timing** — element exists but not yet visible/enabled. Replace any `waitForTimeout` with `await expect(locator).toBeVisible({ timeout: ... })`.
3. **Navigation** — wrong URL or missing `await page.goto('{url}')` before interaction. The project does **not** set `baseURL`, so always use the full URL string above (do not use `'/'`).
4. **Strictness** — locator matched multiple elements. Add `.first()`, `.nth(i)`, or scope by parent.
5. **Assertion mismatch** — the expectation is too strict (exact text/casing). Loosen with `toContainText` or regex.
6. **Login flow** — credential entry uses the wrong field. Re-derive from UI Structure inputs.

## Output format — STRICT

Re-emit **every file you change** using `===FILE: <relative-path>===` headers, exactly like the existing files were provided. You may omit unchanged files. File paths must start with `tests/` or `pages/`.

Example:

===FILE: pages/HomePage.js===
const { expect } = require('@playwright/test');
class HomePage { /* ... corrected ... */ }
module.exports = { HomePage };
===FILE: tests/home.spec.js===
const { test, expect } = require('@playwright/test');
/* ... corrected ... */

## Hard rules

- Output **only** the file blocks. No prose, no code fences around blocks.
- Preserve the public API of page-object classes used elsewhere; rename only when forced by a real conflict.
- Do not introduce new dependencies — only `@playwright/test` and your own modules.
