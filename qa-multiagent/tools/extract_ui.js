// Headless Playwright helper that opens a URL and emits a structured JSON
// summary of the page's interactive elements on stdout. Invoked by
// tools/playwright_tool.py via subprocess.
//
// Usage: node extract_ui.js <url>

const { chromium } = require('playwright');

async function extractUI() {
  const url = process.argv[2];
  if (!url) {
    console.error('Usage: node extract_ui.js <url>');
    process.exit(1);
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    // Settle dynamic content. Cap at 3s so unsettled SPAs do not hang us.
    await page.waitForLoadState('networkidle', { timeout: 3000 }).catch(() => {});

    const data = await page.evaluate(() => {
      const trunc = (s, n = 200) => (s == null ? '' : String(s).slice(0, n));
      const visible = (el) => !!el && (el.offsetParent !== null || el.type === 'hidden');

      const buttons = Array.from(
        document.querySelectorAll('button, [role="button"], input[type="submit"], input[type="button"]')
      )
        .filter(visible)
        .slice(0, 60)
        .map((el) => ({
          text: trunc((el.innerText || el.value || el.textContent || '').trim()),
          id: el.id || null,
          name: el.getAttribute('name') || null,
          type: el.getAttribute('type') || null,
          ariaLabel: el.getAttribute('aria-label') || null,
          dataTestId: el.getAttribute('data-testid') || null,
        }));

      const inputs = Array.from(
        document.querySelectorAll('input, textarea, select')
      )
        .slice(0, 80)
        .map((el) => ({
          tag: el.tagName.toLowerCase(),
          type: (el.getAttribute('type') || el.tagName.toLowerCase()).toLowerCase(),
          name: el.getAttribute('name') || null,
          id: el.id || null,
          placeholder: el.getAttribute('placeholder') || null,
          ariaLabel: el.getAttribute('aria-label') || null,
          required: el.hasAttribute('required'),
          dataTestId: el.getAttribute('data-testid') || null,
          label: (() => {
            if (!el.id) return null;
            const lab = document.querySelector(`label[for="${el.id}"]`);
            return lab ? trunc(lab.innerText.trim()) : null;
          })(),
        }));

      const forms = Array.from(document.querySelectorAll('form'))
        .slice(0, 20)
        .map((el) => ({
          id: el.id || null,
          name: el.getAttribute('name') || null,
          action: el.getAttribute('action') || null,
          method: (el.getAttribute('method') || 'get').toLowerCase(),
          fieldCount: el.querySelectorAll('input, textarea, select').length,
        }));

      const links = Array.from(document.querySelectorAll('a[href]'))
        .filter(visible)
        .slice(0, 60)
        .map((el) => ({
          text: trunc((el.innerText || '').trim()),
          href: el.href,
          ariaLabel: el.getAttribute('aria-label') || null,
        }));

      const tables = Array.from(document.querySelectorAll('table'))
        .slice(0, 10)
        .map((el) => ({
          id: el.id || null,
          rowCount: el.rows.length,
          colCount: el.rows[0] ? el.rows[0].cells.length : 0,
          headers: Array.from(el.querySelectorAll('th'))
            .slice(0, 20)
            .map((th) => trunc((th.innerText || '').trim())),
        }));

      const headings = Array.from(
        document.querySelectorAll('h1, h2, h3')
      )
        .slice(0, 30)
        .map((el) => ({
          level: el.tagName.toLowerCase(),
          text: trunc((el.innerText || '').trim()),
        }));

      const hasPasswordField = !!document.querySelector('input[type="password"]');
      const hasSearchField = !!document.querySelector('input[type="search"]');

      return {
        title: document.title,
        url: location.href,
        headings,
        buttons,
        inputs,
        forms,
        links,
        tables,
        hasPasswordField,
        hasSearchField,
      };
    });

    process.stdout.write(JSON.stringify(data));
  } finally {
    await browser.close();
  }
}

extractUI().catch((err) => {
  console.error('extract_ui.js failed:', err && err.stack ? err.stack : err);
  process.exit(2);
});
