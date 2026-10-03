/*
 * Derive fast display images from the existing Confluence SVG sheets.
 * Original SVG/PDF files are never rewritten. Full-size downloads can keep
 * their existing URLs while the gallery uses these separate preview files.
 *
 * Usage: node scripts/build-confluence-previews.mjs [--sharp-module <path>]
 * The optional path can point to the bundled workspace Sharp module when
 * Sharp is unavailable in this checkout's dependencies.
 */
import { createHash } from "node:crypto";
import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const moduleArgument = process.argv.indexOf("--sharp-module");
const modulePath = moduleArgument < 0 ? "sharp" : process.argv[moduleArgument + 1];
if (!modulePath) throw new Error("--sharp-module requires a module path.");
const sharp = require(modulePath);

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const pieceDirectory = path.join(root, "public", "jewellery", "confluence");
const sourceDirectory = path.join(pieceDirectory, "technical");
const outputDirectory = path.join(sourceDirectory, "previews");
const docsDirectory = path.join(root, "docs");
const previewWidth = 2380;
const thumbnailWidth = 240;
const sheetNames = [
  "01-design-specification-overview",
  "02-assembly-dimensions",
  "03-construction-stone-setting",
  "04-materials,-finish-bill-of-materials",
  "05-manufacturing-route-tolerances",
  "06-sample-review-quality-control",
  "07-costing,-moq-supplier-quotation",
  "08-release-checklist-source-control",
];

async function originalFiles(directory = pieceDirectory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(entries.map(async (entry) => {
    if (entry.name === "previews") return [];
    const filename = path.join(directory, entry.name);
    if (entry.isDirectory()) return originalFiles(filename);
    return /\.(svg|pdf)$/i.test(entry.name) ? [filename] : [];
  }));
  return nested.flat().sort();
}

async function snapshotOriginals() {
  return Promise.all((await originalFiles()).map(async (filename) => {
    const bytes = await readFile(filename);
    return {
      path: path.relative(root, filename).replaceAll(path.sep, "/"),
      bytes: bytes.length,
      sha256: createHash("sha256").update(bytes).digest("hex"),
    };
  }));
}

const before = await snapshotOriginals();
await mkdir(outputDirectory, { recursive: true });
await mkdir(docsDirectory, { recursive: true });
const records = [];
const tiles = [];
for (const name of sheetNames) {
  const source = await readFile(path.join(sourceDirectory, `${name}.svg`));
  // Render at two pixels per SVG unit. This retains the original drawing,
  // text, colours and embedded technical imagery rather than rebuilding it.
  const sourceImage = sharp(source, { density: 144 }).flatten({ background: "white" });
  // Lossless compression keeps vector-only sheets pixel-exact and is smaller
  // than high-quality lossy compression for this drawing/table artwork.
  const vectorOnly = !/<image\b/.test(source.toString("utf8"));
  const preview = await sourceImage.clone().resize({ width: previewWidth })
    .webp(vectorOnly ? { lossless: true, effort: 6 } : { quality: 94, effort: 6, smartSubsample: true }).toBuffer();
  const thumbnail = await sourceImage.clone().resize({ width: thumbnailWidth })
    .webp({ quality: 86, effort: 6, smartSubsample: true }).toBuffer();
  const previewPath = path.join(outputDirectory, `${name}.webp`);
  const thumbnailPath = path.join(outputDirectory, `${name}-thumb.webp`);
  await writeFile(previewPath, preview);
  await writeFile(thumbnailPath, thumbnail);
  const previewMetadata = await sharp(preview).metadata();
  const thumbnailMetadata = await sharp(thumbnail).metadata();
  records.push({
    source: `public/jewellery/confluence/technical/${name}.svg`,
    sourceBytes: source.length,
    preview: `public/jewellery/confluence/technical/previews/${name}.webp`,
    previewBytes: preview.length,
    previewWidth: previewMetadata.width,
    previewHeight: previewMetadata.height,
    previewEncoding: vectorOnly ? "lossless WebP" : "quality 94 WebP",
    thumbnail: `public/jewellery/confluence/technical/previews/${name}-thumb.webp`,
    thumbnailBytes: thumbnail.length,
    thumbnailWidth: thumbnailMetadata.width,
    thumbnailHeight: thumbnailMetadata.height,
    previewReductionPercent: Number((100 * (1 - preview.length / source.length)).toFixed(1)),
  });
  tiles.push(await sharp(preview).resize({ width: 595 }).png().toBuffer());
}

const after = await snapshotOriginals();
if (JSON.stringify(before) !== JSON.stringify(after)) {
  throw new Error("Original SVG/PDF hash changed while previews were generated.");
}
const composites = tiles.map((input, index) => ({
  input,
  left: 12 + (index % 2) * 607,
  top: 12 + Math.floor(index / 2) * 433,
}));
const contactSheet = path.join(docsDirectory, "confluence-previews-contact-sheet.png");
await sharp({ create: { width: 1226, height: 1744, channels: 3, background: "#dce0e2" } })
  .composite(composites).png().toFile(contactSheet);

const totalSourceBytes = records.reduce((sum, record) => sum + record.sourceBytes, 0);
const totalPreviewBytes = records.reduce((sum, record) => sum + record.previewBytes, 0);
const totalThumbnailBytes = records.reduce((sum, record) => sum + record.thumbnailBytes, 0);
const report = {
  generatedAt: new Date().toISOString(),
  renderer: "Sharp/libvips SVG renderer; directly derived from existing SVG sheets",
  rendererVersions: sharp.versions,
  preservation: { originalsUnchanged: true, before, after },
  previewSettings: { width: previewWidth, vectorOnly: "lossless", embeddedImages: "quality 94 / smartSubsample" },
  thumbnailSettings: { width: thumbnailWidth, quality: 86, smartSubsample: true },
  totals: {
    sourceBytes: totalSourceBytes,
    previewBytes: totalPreviewBytes,
    thumbnailBytes: totalThumbnailBytes,
    initialDimensionsGalleryBytes: records[0].previewBytes + totalThumbnailBytes,
    sourceMainAndAllThumbnailsBytes: totalSourceBytes,
  },
  sheets: records,
  contactSheet: path.relative(root, contactSheet).replaceAll(path.sep, "/"),
};
await writeFile(path.join(docsDirectory, "confluence-preview-performance.json"), `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify({ originalsUnchanged: true, sheets: records.length, totals: report.totals }, null, 2));
