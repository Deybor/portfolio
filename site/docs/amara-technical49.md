# Amara revision 49 technical drawings

Updated 2026-10-01. This change affects the standalone HTML specification only. The story page's Sketches heading and combined sketch image are preserved.

## Source and method

Source: `C:\Users\Master\Documents\itura\model\engineering48\Amara49_LowerProng_Refined_ViewFix.blend`.

Unchanged SHA256: `85314FD610597397320D2A560516F9E4B33E97584A9D016E72AFA2DFFAEDF055`.

The read-only Blender export evaluates the existing geometry in world coordinates. Visible outlines are traced from orthographic object masks into SVG paths; internal feature edges are projected from the evaluated mesh with an occlusion check. Section boundaries are actual plane/mesh intersections, not decorative shapes. Every section loop must close before sheet generation succeeds. Explicit camera axes keep top-view masks and projected edges aligned.

Output: three vector-only A3 sheets, in millimetres, with view labels, extension lines, arrowheads, centrelines, sections, hatching and revision/title blocks. Assembly views use 5:1, detail views 10:1, and shell views 7.5:1 at the exported A3 size. Screen resizing does not change the labelled dimensions.

## Measurements and references

| Feature | CAD measurement |
| --- | --- |
| Head width / height | 9.04 / 9.34 mm |
| Shell alone depth | 5.41 mm |
| Head depth including attachment boss | 5.58 mm |
| Assembly depth including post | 16.08 mm, reference |
| Shaft diameter | 0.80 mm, sampled in straight middle section |
| Post base collar diameter | 0.92 mm |
| Attachment boss diameter | 2.10 mm |
| Post component length | 10.60 mm, reference |
| Clear post beyond boss rear plane A | 10.50 mm |
| Post axis from front-left envelope B | 4.38 mm |
| Post axis above lowest shell envelope C | 6.00 mm |
| Seat W × H × D | 6.51 × 6.70 × 2.35 mm |
| CZ W × H × D | 6.00 × 6.00 × 3.55 mm |
| Prong tip projected envelope | 3 × Ø0.87 mm |
| Local shell back wall | 0.81 mm at S–S, Z = 4.036 mm |
| Local seat material spans | 1.00 / 1.02 mm at T–T, Y = 1.223 mm |
| Local seat opening | 3.75 mm at the same section line |

A is the actual rear planar face of the boss. B and C are CAD bounding-envelope references, explicitly not GD&T datum features. Rear-view X is mirrored correctly. Local section widths are not global minimum wall requirements or a claim of fitted-stone clearance. The seat includes its supported terminals. Values round to two decimals; raw coordinates are retained outside the public site in `itura/portfolio-revision/technical49/measurements.json`.

No tolerances, coating allowances or casting shrinkage were invented. Material/finish proposals remain labelled. These are CAD dimension studies; physical CZ fit and setting validation are outstanding.

## Reviewer wording and complete download

The subsequent review removed export-method language (mesh intersections, shaft sampling, and GD&T comparisons) from the displayed notes. Useful interpretation notes remain: millimetres and before-finishing dimensions, reference dimensions in parentheses, post position references, local section thickness limits and sample checks.

The visible table now separates shaft diameter (Ø0.80) and clear post length (10.50) from the collar diameter (Ø0.92) and component length (10.60) on the drawing. It also distinguishes shell-only depth (5.41) from the head including its attachment boss (5.58). Three-prong setting is stated; the earring back remains unknown. The table is shared with the main case-study specification and PDF.

Section locations now reference physical outlines: shell wall height 4.24 above C, and seat cut T–T 3.31 above the seat bottom. Local seat widths and opening are taken at mid-depth. This replaces unexplained world X/Y/Z coordinates without changing the cut geometry.

The header's **Download spec sheet** downloads `Amara-Nest-Spec-Sheet-Rev49.pdf`: four A3 pages with the material/dimension table and the three vector drawings. Per-sheet links are now **View drawing**. The new PDF does not replace older archival files; current links use the complete CZ specification.

After these changes: build and typecheck pass; actual desktop and phone layouts were inspected; the built preview loads all five images with no console errors. The full PDF download was exercised and matched the public file hash. All four final PDF pages were rendered and inspected. Drawing pages contain no raster images. Source Blender and main Sketches hashes are unchanged. No publication.

### Label-only correction

The user clarified that download behaviour should stay as it was. Each drawing again downloads its original SVG, with the visible label **Download**; its companion link says **View drawing**. The top action is restored to **Print / save PDF**. The complete PDF created above remains an unlinked artifact. The page subtitle now says **Specification**, and visible model revision wording is removed from the current drawing sheets. Internal asset names and provenance are retained. Both existing specification tabs were refreshed, and the final desktop and 390px phone previews were checked. Build passes.

## Primary references

## Model overview and estimates — 1 October 2026

The case-study specification cover and standalone HTML now share a compact sheet of front, back, side and top clay views plus a true isometric line sketch. The new top view and isometric projection were exported from the saved model without saving or altering the Blender file. The assembled and exploded model sheets follow the Dimension index, with labels for the shell, CZ, prongs, seat, attachment boss and post. Phone panels pan independently and provide full-size view links. Internal version wording was removed from the comparison badge and the story sketch footer; the existing sketch paths are unchanged.

The shared table shows **approximately 1.7 g per stud / 3.3 g per pair**, excluding backs and finishing. This is a model-based estimate for the proposed sterling-silver-and-CZ construction, not a weighed finished sample. Temporary copies of evaluated metal parts were joined and unioned by voxel remeshing; 0.04 mm and 0.02 mm closed-manifold results differed by less than 0.03 mm³. At 0.02 mm the union was 138.2064 mm³; after subtracting the CZ overlap it was 137.8796 mm³. CZ volume is 41.3624 mm³. Using 10.3 g/cm³ for sterling silver and 5.6–6.0 g/cm³ for CZ gives 1.652–1.672 g per stud; rounding is applied independently to the stud and pair. Backs, coating, finishing loss and actual casting variation are excluded.

- [Cookson bullion technical information](https://www.cooksongold.com/downloads/cat/Bullion_Technical_info_2008.pdf) gives sterling-silver density of 10.3 g/cm³.
- [GIA, Cubic Zirconia: an Update](https://www.gia.edu/doc/Cubic-Zirconia.pdf) gives CZ specific gravity of 5.6–6.0.

Weight provenance and convergence checks: `itura/portfolio-revision/technical49/weight-estimate.json`, generated by `measure-weight49.py`. The model SHA256 remains `85314FD610597397320D2A560516F9E4B33E97584A9D016E72AFA2DFFAEDF055`.

The user selected **₦15,000 per pair as the planning target**. The table says “Unit cost target” and “planning target”; this is not a supplier quote or a researched manufacturing price. The earring back stays unknown. No archived PDFs are linked as current specifications.

Build and typecheck pass. Desktop and 390 × 844 mobile previews were inspected: the compact sheet loads, all six standalone specification images load, the Dimension index opens, both labelled sheets appear below it, and the labelled panels pan without whole-page overflow. Proof images are in `screenshots/collection/amara-overview-phone.png`, `amara-labelled-phone.png` and `amara-spec-cover-*.png`.

## Drawing references

The user subsequently requested sketches only in the compact overview, then a reference-style sheet with three orthographic views and an isometric view. The current overview shows front, side and back outlines plus a true isometric projection. Extension lines and arrows mark measured overall width 9.04 mm, height 9.34 mm and depth 16.08 mm including the post. Dimension endpoints are projected from the measured shell and post bounds. The same asset is used on the case-study specification cover. The labelled assembled and exploded views below the Dimension index remain separate. The compact SVG contains no embedded raster views. Desktop and 390 × 844 phone views were inspected, with no page overflow. Proof: `screenshots/collection/amara-overall-dimensions-*.png`.

- [ISO 129-1 — presentation of dimensions and tolerances](https://www.iso.org/standard/64007.html)
- [ISO 5456-2 — orthographic representations](https://www.iso.org/standard/11502.html)
- [Onshape drawing dimensions](https://cad.onshape.com/help/Content/Drawing/drawing_dimensions.htm)
- [Onshape drawing views and sections](https://cad.onshape.com/help/Content/Drawing/views.htm)
- [GIA — quality assurance for stone settings](https://www.gia.edu/gia-website/bench-tip-avoid-stone-loss-with-quality-assurance-benchmarks)

These informed drawing conventions and the distinction between measured geometry and physical setting checks. No claim of full standards compliance or manufacturing certification is made.

## Verification

- Inspected all three SVG sheets in the actual desktop HTML preview at 1280 × 900; corrected top-view orientation, contour simplification and shell dimension spacing during review.
- At 390 × 844, drawings scroll inside bounded containers. Tested horizontal swipe; no whole-page horizontal overflow. Dimension index opens and remains within the phone width.
- All five specification/model images loaded. SVG routes return HTTP 200 with `image/svg+xml`. The assembly download was exercised in the browser and its downloaded file hash matches the public SVG.
- Back-to-Amara and full-specification links exercised in the browser. The main story Sketches image loads and is unchanged: SHA256 `2B81A655CABC0F97CE827CB52CCCB59897F37476B1368D64868E39AFEA670BAD`.
- `npm run build` passes. Existing module-directive notices remain; database migration skips because no DATABASE_URL is configured. Built output includes all three SVG assets.
- Desktop and phone screenshots saved in `screenshots/collection/amara-technical49-*.jpg`.
- Blender source hash verified unchanged after exporting. No deployment or source-model edit.
