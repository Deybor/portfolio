# Portfolio continuation — approved state, 02 October 2026

This is the continuation handoff for the existing local portfolio. Preserve the current working files. Do not rebuild the site, reset to Git, restore an older design or publish it without a new request. There is no unfinished task from this session; implement the user's next specific change.

## GitHub publication update

The user subsequently requested publishing this approved local portfolio to their existing GitHub site. The repository is `https://github.com/Deybor/portfolio`, and the live URL is `https://deybor.github.io/portfolio/`. Publication uses the clean clone at `C:\Users\Master\Documents\portfolio\.qa\github-publish`. The current editable project is retained under `site/` in the repository, and the existing Pages workflow deploys its committed `dist/` on `main`.

Read `docs/GITHUB-PAGES.md` for the deployment build and verification instructions. All 19 project routes are pre-rendered for Pages, assets are scoped to `/portfolio/`, and local dev remains on 8080. Do not publish later edits without the user's authorization. The first deployment commit was `1948353`; inspect the actual repository HEAD and newest successful Actions run for subsequent publishing fixes.

## Workspace and preview

- Website: `C:\Users\Master\Documents\portfolio\porfolio update` — this spelling is intentional. The older static site at `C:\Users\Master\Documents\portfolio` is a different project.
- Blender assets: `C:\Users\Master\Documents\itura`.
- Jewellery source assets: `C:\Users\Master\Documents\itura\PORFOLIO PIECES`.
- Local website: `http://127.0.0.1:8080/jewellery`.
- Current piece: `http://127.0.0.1:8080/jewellery/iced-out-ring`.
- Other pages: `/jewellery/confluence`, `/jewellery/heartline-pendant`, `/jewellery/ribbon-leaf`, `/jewellery/amara`, `/jewellery/workbench`, `/objects`.
- Built preview: `http://127.0.0.1:8081`. Both servers were running at handoff; verify them before starting another server. Process IDs may change.
- This is Windows/PowerShell. Some repository instructions assume a Linux sandbox; adapt environment-specific commands to this actual local workspace.

Read `AGENTS.md` and `AGENTS.project.md` in the website root, then inspect relevant current source files. This handoff records the latest user-approved state; older narrative notes may describe superseded decisions.

## Approved presentation and interactions

- Preserve the charcoal, warm cream, serif design system, existing home page, jewellery study pages and printed-object collection.
- Jewellery showcase order: Amara studs first, followed by Confluence, Iced-out ring, Heartline and Ribbon Leaf. Autoplay is 4 seconds. Retain arrows, pause and other working interactions.
- The main jewellery pieces appear before the separate Amara companion study entry. The Amara study entry retains its compact approved presentation: “Amara's companion,” “A companion for an existing necklace,” and “Open study.”
- Portfolio piece covers have a fixed diagonal split between the beauty image and a black wireframe on warm ivory. It is not an interactive slider. This is a cover treatment; do not impose it on the large render displays or inside-piece galleries. Preserve its existing angle and styling.
- Large Confluence, Iced-out and Heartline renders use a blurred image fill around the contained image. The Amara heart studs do not need that blurred background.
- Images and SVG drawings open in an in-site popup rather than redirecting. It has previous/next arrows, left/right keyboard navigation, image counter, zoom/fit, download, Escape and close. Downloads follow the current image. Single-image galleries hide navigation. Preserve focus return and page scroll restoration.
- PDF downloads remain downloads; do not route them through the image viewer.

## Latest terminology and reviewer copy

The user approved describing this Blender-based work as **3D modelling**, **Model views** and **Model dimensions**. Keep **Technical drawings**, **Technical specification** and **Wireframe**. This correction was applied to current page copy, metadata/alt text, SVG labels and all five currently linked specification/dimension PDFs.

Do not reintroduce CAD claims into reviewer-facing copy for these studies. Existing internal `cad` view keys, asset filenames, Blender object names and provenance filenames remain for compatibility; do not rename those blindly. This terminology decision does not redefine any separately documented CAD experience on a CV.

Reviewer copy was cleaned of chat replies, edit history, defensive explanations, local evidence filenames/hashes and unrelated disclaimers. Keep meaningful dimensions, material proposals, physical-sample requirements and TBC fields. Do not invent manufacturing, commissions, quotes, supplier relationships, sales, production release or ITURA affiliation.

## Gallery images and model choices

### Confluence

- Render 01 and cover: `public/jewellery/confluence/render-01-environment.webp` / `.png`, from `C:\Users\Master\Documents\itura\PORFOLIO PIECES\BlenderKit_Beauty\Confluence_Environment.png`.
- Render 02: `render-02-studio.webp` / `.png`, from `C:\Users\Master\Downloads\convo.png`.
- Render 03 remains the setting detail.
- Original approved model: `C:\Users\Master\Documents\itura\PORFOLIO PIECES\Confluence_First_Ring\Approved_Model\Confluence_Refined_Print.blend`.
- Current specification/wireframe model: `C:\Users\Master\Documents\portfolio\porfolio update\public\jewellery\confluence\technical\Confluence-Refined-Centre-Prongs-CAD.blend`.
- It is a separate pre-setting metal revision with stones removed. Four centre prongs retain their lower curvature and end in approximately 0.62 mm of straight open stock. The eight side prongs remain. Do not revert to the earlier all-straight approximation or alter the approved beauty renders.
- Sheet 03, `technical/03-construction-stone-setting.svg`, has **one vector front elevation** on the left. It is not section A–A and must not show an overlapping cut/front outline or floating cut blobs. The two model views on the right remain shaded model images, as approved.
- Eight specification sheets appear under the Dimensions tab. Sheet 08 is titled “Sample approval & release”; its historical filename remains `08-release-checklist-source-control.svg` for link compatibility.

### Iced-out ring

- Render 01 and cover: `public/jewellery/iced-out-ring/render-01-gallery.webp` / `.png`, from `C:\Users\Master\Documents\itura\PORFOLIO PIECES\BlenderKit_Beauty\Iced_Ring_Gallery.png`.
- Render 02 is the former 01, still stored as `render-01.webp` / `.png`. No third render.
- Use the **original retained model**, not the modified model: `C:\Users\Master\Documents\itura\PORFOLIO PIECES\Ring_Iced_Out_03\Ring_Iced_Out_03.blend`. The extraction identifies `CAD base - exact source mesh`.
- Eight specification sheets appear under Dimensions. Source-unit calibration, nominal ring size, purchased-stone sizes/counts/row allocation remain TBC. Do not infer those from beauty renders.

### Heartline

- Render 01 and cover: `public/jewellery/heartline-pendant/render-01-studio.webp` / `.png`, from `C:\Users\Master\Documents\itura\PORFOLIO PIECES\BlenderKit_Beauty\Heartline_Studio.png`.
- Render 02 is the former 01 (`render-01.webp` / `.png`).
- Use the original pendant: `C:\Users\Master\Documents\itura\PORFOLIO PIECES\Heartline_Pendant_01.blend`.
- Dimensions include the metal body and suspension loop, exclude the chain: 15.73 W × 16.52 H × 1.63 D mm. The Dimensions tab and SVG download are present.

### Amara Nest

- Independent companion study for the ITURA Amara necklace; retain the compact asymmetric stud and existing CZ composition.
- Current measured source: `C:\Users\Master\Documents\itura\model\engineering48\Amara49_LowerProng_Refined_ViewFix.blend`.
- Frozen measurement/mask inputs: `C:\Users\Master\Documents\itura\portfolio-revision\technical49`.
- Preserve the current model/render comparison and technical drawing system. Do not substitute a different revision when deriving dimensions.
- Material/finish are proposed; weight is estimated and excludes backs. Earring back and sample approval remain pending. Do not present the planning cost as a supplier quote.

### Ribbon Leaf

- Current approved entry has one studio render and one assembly-dimension SVG. Do not restore discarded separate model/wireframe tabs.
- Source scene variants are under `C:\Users\Master\Documents\itura\PORFOLIO PIECES\BlenderKit_Beauty`, including `Ribbon_Leaf_Aligned_Drops.blend`.
- Current data in `src/lib/jewellery-pieces.ts` is authoritative. This piece was also being updated in another chat; reread its current files before editing.

## Main website files

All paths below are relative to `C:\Users\Master\Documents\portfolio\porfolio update`.

- Piece data, gallery order, labels and downloads: `src/lib/jewellery-pieces.ts`.
- Shared piece pages: `src/components/jewellery/piece-page.tsx`.
- Showcase and covers: `src/components/jewellery/showcase.tsx`, `pieces.tsx`, `landing.tsx`; styles in `src/styles/collection.css`.
- Amara study: `src/components/jewellery/amara-page.tsx`, `amara-story.tsx`, `model-comparison.tsx`, `workbench-page.tsx`, `specification-table.tsx`.
- Shared Amara specification data: `src/data/amara-spec.json`; styles in `src/styles/jewellery-story.css`.
- Main page copy: `src/components/home-page.tsx`; jewellery route metadata in `src/routes/jewellery`.
- Shared image popup: `public/image-viewer.js`, `public/image-viewer.css`, loaded by `src/components/image-preview.tsx` and `src/routes/__root.tsx`. Standalone specification HTML also loads it.
- Printed objects: `src/components/objects/object-project.tsx`, `objects-index.tsx`, `src/lib/printed-objects.ts`, `printed-objects.json`.
- Deployed assets: `public/jewellery/{confluence,iced-out-ring,heartline-pendant,ribbon-leaf,amara-nest}` and `public/objects`.

## Specifications, builders and evidence

Currently linked final PDFs:

1. `public/jewellery/confluence/technical-specification.pdf` — 8 pages.
2. `public/jewellery/confluence/dimensions.pdf` — 1 page, corresponding to sheet 02.
3. `public/jewellery/iced-out-ring/technical-specification.pdf` — 8 pages.
4. `public/jewellery/iced-out-ring/dimensions.pdf` — 1 page, corresponding to sheet 02.
5. `public/jewellery/amara-nest/Amara-Nest-Spec-Sheet-Rev49.pdf` — 4 pages.

Each ring has `specification.html` and eight SVGs in its `technical` folder. Amara has `specification.html`, drawings in `technical49`, model/parts views in `model49`, and sketches in `sketches49`.

Ring pack builder: `scripts/build-ring-specifications.py`. It rebuilds both rings, standalone HTML, drawings, gallery thumbnails and dimension PDFs from the frozen register `docs/ring-specification-cad-data.json`. Preserve its source hashes, nominal/measured distinctions and proposed/TBC fields.

Amara builders, in dependency order: `scripts/build-amara-technical49.py`, `scripts/build-amara-html-spec.py`, `scripts/build-amara-download-spec.py`. Heartline builder: `scripts/build-heartline-drawing.py`, using `docs/heartline-dimensions.json`.

Confluence checks: `scripts/verify-confluence-spec-c.py`; supporting records include `docs/confluence-centre-prong-refinement.json`, `confluence-tip-scope-audit.json` and `confluence-section-audit.json`. Older `docs/ring-technical-specifications.md` and other historic notes can describe superseded prong/drawing/terminology states; use current source, registers and this handoff first.

Initial source briefs, if needed:

- Portfolio request: `C:\Users\Master\.codex\attachments\7d5c9368-d108-4703-b16d-817478462aa4\Pasted text.txt`.
- Supplied role/specification requirements: `C:\Users\Master\.codex\attachments\f7361ccb-cffb-44ab-a198-04eed81c174f\Pasted text.txt`.

## Verification and Windows tooling

Latest checks passed: `npm run build`, `npm run typecheck`, Confluence SVG/source verification, real desktop/mobile browser checks on dev and built previews, image popup navigation/keyboard/zoom/download/close checks, and visual review of all five PDFs. After the terminology edit, all numeric values and PDF page counts matched the prior files. Original models were not edited.

- Recent PDF renders, comparisons and logs: `.qa/model-terminology`.
- Browser screenshots/verdicts: `screenshots/terminology-*.png` / `.json`; settled built screenshots include `terminology-built-index-settled` and `terminology-built-workbench-settled`.
- Earlier broad popup checks: `screenshots/reviewer-*.json` and `.qa/reviewer-*.log`.
- Browser helper: `scripts/browser-smoke.mjs`; popup interaction checks: `scripts/check-reviewer-viewer.mjs`.
- On Windows the helper uses installed Edge. It checks desktop 1280×800 and mobile 390×844. Set `BROWSER_SMOKE_REVIEWER=1` and `BROWSER_SMOKE_GALLERY=dimensions` to exercise the popup. Set `BROWSER_SMOKE_SETTLE_MS=5000` for slow images before screenshots. It accepts `--baseline` for built/dev comparison. Put screenshot outputs under the website's `screenshots` directory.
- Browser example from the website root: `node scripts/browser-smoke.mjs http://127.0.0.1:8080/jewellery/iced-out-ring screenshots/next-iced.png`.
- Verify the actual images visually; build/HTTP status alone is not visual proof. CUA initialization previously failed with an ACL helper error, while this browser helper worked.
- Bundled Python: `C:\Users\Master\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`. Set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` before builders, avoiding the Windows cp932 output error.
- Bundled Node: `C:\Users\Master\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe`. System npm is also at `C:\Program Files\nodejs`; include that directory in PATH when needed.
- Blender: `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`.
- After new source changes, rerun build/typecheck, relevant dev/browser checks and a refreshed built preview. Use the app-env wrapper; preserve the 8080 dev server. Restart only confirmed preview processes; never kill a guessed PID. Latest preview parent PID is recorded in `.qa/reviewer-preview.pid`, but inspect the current process/command first. Launch background helpers hidden on Windows.
- If model changes are requested, inspect the actual model and open/unsaved state first. Preserve originals, create a separate revision, derive drawings from one frozen revision and validate it. Mesh checks are not a physical-fit or manufacturing-release certification.

Work in the existing files, keep changes focused, give concise progress updates, and verify the delivered local preview rather than asking the user to perform QA.
