# Amara model and reveal revision

The choice reveal uses the supplied `C:/Users/Master/Documents/itura/amara stud images/6.png`, converted to `public/jewellery/amara-nest/beauty/06.webp`. It now has three native-scroll phases: “And I chose…”, the product photograph/render appearing as the charcoal background warms to amber, and the image moving beside a short explanation. Desktop and phone motion can be turned off. Reduced motion and short viewports use an ordinary static presentation.

The technical section is now “Building the stud”: a matching wireframe/render comparison, front and side clay views, a rear wireframe, then compact technical drawings and the bold spec sheet. The comparison range supports touch, mouse and keyboard. On phones the navigation label is shortened to “Model” so all links fit.

## Model source and exports

Source: `C:/Users/Master/Documents/itura/model/engineering48/Amara49_LowerProng_Refined_ViewFix.blend`. `portfolio-revision/inspect49.py` and `portfolio-revision/capture49.py` under the Itura directory inspect and render it in background Blender. They never save the source file. The neutral and wire views are actual geometry exports; the material view uses its packed materials and scene lights. Presentation cameras and temporary mesh-edge curves are used only in memory for exports. These images are not screenshots of the Blender interface.

Head measurements from evaluated world geometry: X 9.03596 mm, Z 9.34442 mm, Y 5.57901 mm; total Y depth 16.07901 mm. Rounded for presentation: 9.04 × 9.34 × 5.58 mm, total depth 16.08 mm. The CAD post has a 0.92 mm maximum envelope; 0.80 mm is the proposed shaft specification from the earlier sheet. No manufacturing approval is inferred.

Source SHA-256 before and after export: `389F96D412C9F5A93CAC36212C1E15089E241C389DCEDBF024E47CCF6055495C`.

New assets: `public/jewellery/amara-nest/model49/*.webp` and `line-studies49/*.svg`. The line studies use the current Cylinder prong objects, shell, seat, stone, attachment boss and post. The earlier drawings and PDFs remain saved; the earlier annotations are labelled as earlier design notes on the page.

## Revised document

`Amara-Technical-Specification-Rev49.pdf` has four pages: model dimensions, proposed specification, component callouts and the exploded seat view. It uses actual updated-prong clay renders, identifies the independent study, distinguishes the CZ reference mesh from the proposed moissanite stone, and preserves proposed materials, finish and tolerances. The earlier NGN 15,000 planning target is explicitly a target, with no supplier quote. Website links on Amara, the jewellery overview and workbench point to this revision. Page previews use `spec49-overview.webp` and `spec49-exploded.webp`.

All four pages were rendered and inspected. Callout positions were corrected on the post and lower prong before the final render.

## Writing and presentation references

[GOV.UK writing for user interfaces](https://www.gov.uk/service-manual/design/writing-for-user-interfaces) informed short sentences, ordinary words and descriptive headings. [Method Studio’s Bulut case](https://www.methodstudio.design/projects/bulut/) was reviewed for the sequence from product presentation to engineering evidence; its editorial tone was not copied. [W3C C39](https://www.w3.org/WAI/WCAG22/Techniques/css/C39) informed the reduced-motion fallback.

## Verification

Final typecheck and production build passed. Development checks confirmed the three desktop scroll phases, mobile reveal, matching mesh/material images, range keyboard endpoints and intermediate values, no-jump motion-off control, compact drawings and the new document targets. The three jewellery routes and new render/PDF/previews returned HTTP 200. The source file hash remained unchanged.

The final production preview was also inspected at 1280 × 800, 390 × 844 and 768 × 800. Mobile and tablet layouts had no horizontal overflow. At 1280 × 640 the short-viewport static fallback showed both image and text. Production browser error/warning logs were empty. All four final PDF pages were visually checked; desktop reveal/model/spec and mobile model screenshots are saved under `screenshots/collection/`. The local development preview remains on port 8080; this revision has not been published.
