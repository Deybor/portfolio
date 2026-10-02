import { readFileSync, writeFileSync } from "node:fs";
import { chromium } from "playwright";

const origin = process.argv[2] || "http://127.0.0.1:8082";
const base = `${origin}/portfolio/`;
const objects = JSON.parse(readFileSync("src/lib/printed-objects.json", "utf8"));
const routes = ["", "jewellery", "jewellery/amara", "jewellery/workbench", "jewellery/confluence", "jewellery/iced-out-ring", "jewellery/heartline-pendant", "jewellery/ribbon-leaf", "objects", ...objects.map(({slug}) => `objects/${slug}`)];
const browser = await chromium.launch({ headless: true, ...(process.platform === "win32" ? { channel: "msedge" } : {}) });
const assets = new Set(); const failures = []; const pages = [];
try {
  const page = await browser.newPage();
  page.on("pageerror", error => failures.push(`${page.url()}: ${error.message}`));
  page.on("response", response => { if (response.status() >= 400 && response.url().startsWith(origin)) failures.push(`${response.status()} ${response.url()}`); });
  for (const route of routes) {
    const response = await page.goto(base + route + (route ? "/" : ""), { waitUntil: "domcontentloaded" });
    await page.locator("main").waitFor();
    await page.waitForTimeout(350);
    const text = await page.locator("main").innerText();
    if (response.status() !== 200 || text.length < 50) failures.push(`Page failed: ${route}`);
    if (/\bCAD\b/.test(text)) failures.push(`Reviewer CAD wording on ${route}`);
    if ((route.startsWith("jewellery") || route.startsWith("objects")) && !await page.locator("body").evaluate(body => body.classList.contains("world-jewel"))) failures.push(`Missing jewellery styling: ${route}`);
    const collect = async () => {
      const urls = await page.evaluate(() => {
        const links = [...document.querySelectorAll('a[href],img[src],video[src],source[src]')].map(node => node.href || node.src);
        for (const node of document.querySelectorAll('[data-preview-gallery]')) for (const item of JSON.parse(node.dataset.previewGallery)) links.push(new URL(item.href, location.href).href);
        return links;
      });
      for (const url of urls) if (url.startsWith(origin)) assets.add(url.split("#")[0]);
    };
    await collect();
    const tabs = page.getByRole("tab");
    for (let i = 0; i < await tabs.count(); i++) { await tabs.nth(i).click(); await collect(); }
    pages.push({ route, title: await page.title(), textLength: text.length });
  }
  const urls = [...assets];
  for (let i = 0; i < urls.length; i += 8) await Promise.all(urls.slice(i, i + 8).map(async url => {
    try { const result = await page.request.head(url); if (result.status() !== 200) failures.push(`Link ${result.status()}: ${url}`); }
    catch (error) { failures.push(`Link request failed: ${url}`); }
  }));
  const result = { base, pages, checkedUrls: urls.length, failures: [...new Set(failures)] };
  writeFileSync(".qa/pages-link-audit.json", JSON.stringify(result, null, 2));
  console.log(JSON.stringify({ pages: pages.length, checkedUrls: urls.length, failures: result.failures }, null, 2));
  if (failures.length) process.exitCode = 1;
} finally { await browser.close(); }
