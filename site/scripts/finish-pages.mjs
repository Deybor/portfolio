import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { basename, join, resolve, sep } from "node:path";
import { chromium } from "playwright";
import { renderWebManifest } from "./grok-pwa-shared.mjs";

const root = process.cwd();
const output = resolve(root, "dist-pages");
if (!output.startsWith(resolve(root) + sep) || basename(output) !== "dist-pages") throw Error("Output must be this project's dist-pages directory");
const input = join(root, ".vercel/output/static");
if (!existsSync(join(input, "index.html"))) throw Error("Build with VITE_GITHUB_PAGES=true first");
if (existsSync(output)) rmSync(output, { recursive: true });
cpSync(input, output, { recursive: true, filter: (file) => !/\.(?:blend\d*|log|json)$/i.test(file) });
const base = "/portfolio/";
const rewrite = (html) => html.replace(/((?:href|src|poster|action)=["'])\/(?!\/|portfolio(?:\/|["']))/g, `$1${base}`);
function rewriteTree(folder) {
  for (const entry of readdirSync(folder, { withFileTypes: true })) {
    const file = join(folder, entry.name);
    if (entry.isDirectory()) rewriteTree(file);
    else if (/\.(?:html|svg)$/.test(entry.name)) writeFileSync(file, rewrite(readFileSync(file, "utf8")));
  }
}
rewriteTree(output);
const shell = readFileSync(join(output, "index.html"), "utf8");
const pieces = ["confluence", "iced-out-ring", "heartline-pendant", "ribbon-leaf"];
const objectData = JSON.parse(readFileSync(join(root, "src/lib/printed-objects.json"), "utf8"));
const objects = Array.isArray(objectData) ? objectData : objectData.projects;
const routes = ["", "jewellery", "jewellery/amara", "jewellery/workbench", ...pieces.map((slug) => `jewellery/${slug}`), "objects", ...objects.map(({ slug }) => `objects/${slug}`)];
for (const route of routes) {
  const folder = join(output, route); mkdirSync(folder, { recursive: true });
  if (!existsSync(join(folder, "index.html"))) throw Error(`Missing prerendered page: ${route}`);
}
writeFileSync(join(output, "404.html"), shell);
writeFileSync(join(output, ".nojekyll"), "");
const manifest = JSON.parse(renderWebManifest("deybor.github.io"));
Object.assign(manifest, { name: "Deybor 3D", short_name: "Deybor 3D", id: base, start_url: base, scope: base });
manifest.icons = [{ src: `${base}__grok/icon-180.png`, sizes: "180x180", type: "image/png" }];
mkdirSync(join(output, "__grok"), { recursive: true });
for (const file of ["manifest.webmanifest", "manifest.json"]) writeFileSync(join(output, "__grok", file), JSON.stringify(manifest, null, 2));
// Render the existing vector favicon as an install icon; no new artwork.
const browser = await chromium.launch({ headless: true, ...(process.platform === "win32" ? { channel: "msedge" } : {}) });
try {
  const page = await browser.newPage({ viewport: { width: 180, height: 180 } });
  const svg = readFileSync(join(root, "public/favicon.svg"), "utf8");
  await page.setContent(`<style>html,body{margin:0;width:180px;height:180px}svg{width:180px;height:180px;display:block}</style>${svg}`);
  await page.screenshot({ path: join(output, "__grok/icon-180.png") });
} finally { await browser.close(); }
console.log(`Prepared ${routes.length} directly accessible portfolio pages in ${output}`);
