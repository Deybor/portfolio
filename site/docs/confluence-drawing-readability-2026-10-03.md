# Confluence drawing readability refinement - 03 October 2026

The overview now uses the existing shaded isometric image of the same frozen pre-setting body. Assembly dimensions and the front elevation retain their actual visible vector contour coordinates, with 1.20-point contours and 0.90-point feature lines. Existing nominal/measured/proposed specifications and all file URLs are retained.

Source: `Confluence-Refined-Centre-Prongs-CAD.blend`, SHA-256 `e53e30c18b5efca3f4165d868b4d2afd045e4d75fa17013333251ead4a189fb5`. The geometry and source files were not edited. The user-supplied Downloads SVGs hash-matched the starting sheets.

Regeneration order: run `scripts/build-ring-specifications.py confluence`, then `scripts/build-confluence-previews.mjs` with the configured Sharp module, then the normal portfolio build. Inline WebP previews use `technical/previews/{original-SVG-basename}.webp`; all anchors still address the original SVGs. Missing preview files fall back to those SVGs. Always refresh preview files after changing a drawing.

Verification: full table/register equality; PDF text unchanged except the added solid-view label; unchanged vector coordinates on sheets 02/03; all source model hashes preserved; all Iced-out SVG/PDF/HTML hashes unchanged. Full specification remains eight pages and the dimension PDF remains one page. Every final PDF page was rendered and visually inspected. Backup and evidence: `.qa/confluence-readability-2026-10-03`.
