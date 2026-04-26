You are a senior Playwright automation engineer. Generate runnable Playwright **JavaScript** tests for the page below using the **Page Object Model**.

URL: {url}
Login required: {login_required}
Login credentials (use only if login_required is true): {login_credentials}

UI Structure (JSON):
{ui_structure}

## Project layout (already exists — do not scaffold it)

Your files will be dropped into a Playwright project that already has:

- `package.json` with `@playwright/test`
- `playwright.config.js` (no `baseURL` is configured — always use the full URL in `goto`)
- `tests/` directory for spec files
- `pages/` directory for page objects (created on first write)

## Coding requirements

- **CommonJS** (`require` / `module.exports`), `.js` files.
- Use `const { test, expect } = require('@playwright/test');`
- Prefer resilient locators in this order: `getByRole`, `getByLabel`, `getByPlaceholder`, `getByTestId`, `getByText`. Avoid brittle CSS selectors when the UI Structure exposes a better alternative.
- Always navigate with the **full URL** — `await page.goto('{url}')`. Do not use `'/'` because the project does not configure `baseURL`.
- Use `await expect(locator).toBeVisible()` instead of fixed `waitForTimeout`.
- Generate **one Page Object class per logical area** in `pages/` — at minimum a `HomePage`. Add a `LoginPage` only when login_required is true.
- Generate **4–8 spec files in `tests/`**, each focused on one user journey or category.
- Each spec should contain 1–3 `test(...)` blocks.
- Tests must be deterministic. Do not depend on external network calls beyond the URL under test.

## Output format — STRICT

Emit each file as a block delimited by `===FILE: <relative-path>===` headers. Example:

===FILE: pages/HomePage.js===
const { expect } = require('@playwright/test');

class HomePage {
  constructor(page) {
    this.page = page;
    this.heading = page.getByRole('heading');
  }
  async goto() {
    await this.page.goto('{url}');
  }
}

module.exports = { HomePage };
===FILE: tests/home.spec.js===
const { test, expect } = require('@playwright/test');
const { HomePage } = require('../pages/HomePage');

test.describe('Home page', () => {
  test('renders main heading', async ({ page }) => {
    const home = new HomePage(page);
    await home.goto();
    await expect(home.heading.first()).toBeVisible();
  });
});

## Hard rules

- Output **only** the file blocks above.
- Do **not** wrap individual files in code fences.
- Do **not** include explanatory prose, headings, or comments outside the file blocks.
- Every file path must start with `tests/` or `pages/`.
- Every spec must `require` only `@playwright/test` and your own page objects.
