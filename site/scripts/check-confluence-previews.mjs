/* Stop a Pages release if a regenerated Confluence drawing has stale previews. */
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const report = JSON.parse(readFileSync(resolve(root, "docs/confluence-preview-performance.json"), "utf8"));
if (report.sheets.length !== 8) throw new Error("Confluence must have eight current sheet previews.");
for (const sheet of report.sheets) {
  const expected = report.preservation.after.find((file) => file.path === sheet.source);
  const source = readFileSync(resolve(root, sheet.source));
  if (!expected || createHash("sha256").update(source).digest("hex") !== expected.sha256) {
    throw new Error(`Refresh Confluence previews after updating ${sheet.source}: run scripts/build-confluence-previews.mjs.`);
  }
  for (const asset of [sheet.preview, sheet.thumbnail]) {
    if (!readFileSync(resolve(root, asset)).length) throw new Error(`Missing drawing preview: ${asset}`);
  }
}
console.log("Confluence: all eight previews match the current drawings.");
