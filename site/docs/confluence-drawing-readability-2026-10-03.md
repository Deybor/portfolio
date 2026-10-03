# Confluence drawing readability refinement - 03 October 2026

The overview, assembly dimensions and front elevation now use actual shaded views of the same frozen pre-setting CAD body. The assembly sheet uses the original orthographic front, side and top camera views with the existing dimension labels. The construction sheet's 18.00 mm nominal bore dimension is projected through the original front camera and alpha crop, independently of the incomplete legacy line trace. Existing nominal/measured/proposed specifications and all file URLs are retained.

Source: `Confluence-Refined-Centre-Prongs-CAD.blend`, SHA-256 `e53e30c18b5efca3f4165d868b4d2afd045e4d75fa17013333251ead4a189fb5`. The geometry and source files were not edited. The user-supplied Downloads SVGs hash-matched the starting sheets.

Regeneration order: run `scripts/build-ring-specifications.py confluence`, then `scripts/build-confluence-previews.mjs` with the configured Sharp module, then the normal portfolio build. Inline WebP previews use `technical/previews/{original-SVG-basename}.webp`; all anchors still address the original SVGs. Missing preview files fall back to those SVGs. Always refresh preview files after changing a drawing.

Verification: full table/register and PDF text equality against the previously published specification; all source model hashes preserved; all Iced-out SVG/PDF/HTML hashes unchanged. The incomplete black vector traces are absent from sheets 02/03. Full specification remains eight pages and the dimension PDF remains one page. Every final PDF page was rendered and visually inspected. Backup and evidence: `.qa/confluence-solid-assembly-2026-10-03`.

The shaded views are the user's requested temporary live presentation. Fresh geometry-derived line drawings are being prepared separately for preview and review; they must not replace these live sheets without that review.
