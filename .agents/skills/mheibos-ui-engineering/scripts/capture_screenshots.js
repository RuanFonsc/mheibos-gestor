#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const args = Object.fromEntries(process.argv.slice(2).map((item) => {
  const [key, ...rest] = item.replace(/^--/, '').split('=');
  return [key, rest.join('=') || true];
}));
if (!args.url || !args.output) {
  console.error('Uso: capture_screenshots.js --url=http://... --output=DIR [--storage-state=FILE]');
  process.exit(2);
}

const matrix = [
  ['1366x768-100', 1366, 768, 1],
  ['1440x900-100', 1440, 900, 1],
  ['1536x864-100', 1536, 864, 1],
  ['1920x1080-100', 1920, 1080, 1],
  ['1366x768-125', 1093, 614, 1.25],
];
const selectedMatrix = args.only
  ? matrix.filter(([name]) => args.only.split(',').includes(name))
  : matrix;
const overflowScript = fs.readFileSync(path.join(__dirname, 'detect_overflow.js'), 'utf8');

(async () => {
  fs.mkdirSync(args.output, { recursive: true });
  const installedBrowsers = [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  ];
  const executablePath = args['executable-path'] || installedBrowsers.find(fs.existsSync);
  const browser = await chromium.launch({ headless: true, executablePath });
  for (const [name, width, height, deviceScaleFactor] of selectedMatrix) {
    const context = await browser.newContext({
      viewport: { width, height },
      deviceScaleFactor,
      storageState: args['storage-state'] || undefined,
    });
    const page = await context.newPage();
    if (args.username && args.password) {
      const origin = new URL(args.url).origin;
      await page.goto(`${origin}/login/`, { waitUntil: 'networkidle' });
      await page.locator('select[name="usuario"]').selectOption({ label: args.username });
      await page.locator('input[name="senha"]').fill(args.password);
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'networkidle' }),
        page.locator('button[type="submit"]').click(),
      ]);
    }
    await page.goto(args.url, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(args.output, `${name}.png`), fullPage: true });
    const overflow = await page.evaluate(overflowScript);
    fs.writeFileSync(path.join(args.output, `${name}.overflow.json`), JSON.stringify(overflow, null, 2));
    const layout = await page.evaluate(() => Object.fromEntries(
      ['.app-shell', '.sidebar', '.metric-grid', '.filter-grid'].map((selector) => {
        const element = document.querySelector(selector);
        if (!element) return [selector, null];
        const style = getComputedStyle(element);
        return [selector, {
          display: style.display,
          gridTemplateColumns: style.gridTemplateColumns,
          overflowX: style.overflowX,
          overflowY: style.overflowY,
          width: element.getBoundingClientRect().width,
          height: element.getBoundingClientRect().height,
        }];
      })
    ));
    fs.writeFileSync(path.join(args.output, `${name}.layout.json`), JSON.stringify(layout, null, 2));
    await context.close();
  }
  await browser.close();
})().catch((error) => { console.error(error); process.exit(1); });
