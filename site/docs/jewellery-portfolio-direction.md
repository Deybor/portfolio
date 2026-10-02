# Jewellery portfolio direction

Research and local preview review: 30 September 2026.

The agreed direction is a browsable project index with optional depth. An employer should see the finished work, understand the designer's contribution, and choose which project to investigate. The case study earns the second click. It should not be a compulsory introduction to the collection.

## Reference shortlist

These are presentation references, not an objective ranking of designers. The recommendations below combine direct reading of primary project pages with browser inspection. No single site solves every part of this portfolio.

| Reference | What is useful here | What to adapt |
| --- | --- | --- |
| [LAYER project index](https://layerdesign.com/projects/) | An image-led collection with discipline filters. The desktop grid makes different projects easy to compare; the mobile grid becomes one column. | Use a small, visible project index. Keep names and links visible without hovering. Add filters only when there is enough real work to justify them. |
| [BLOND: Peel Chair](https://blond.cc/work/peel-chair-furniture) | Finished images, an early line sketch and prototype photographs sit alongside concise explanations of particular design decisions. | Pair each important draft with its consequence in the selected design. Borrow the project page, rather than the studio's entrance screen. |
| [Sarah Eisman Studio](https://saraheismanstudio.com/) | Controlled jewellery photography, close crops and a distinctive visual identity give the objects presence. | Borrow photographic discipline and consistent image treatment. Its shop navigation serves a different purpose from an employer-facing portfolio. |
| [Kyle Anthony: CAD Design](https://kyleanthonycollection.com/cad-design) | Technical sheets show multiple views and dimensions; a thumbnail opens a larger drawing. | Give CAD drawings their own inspection view. At phone width, a complete sheet can become too small to read, so offer the full file and individual views. |
| [Morrama: Kibu Headphones](https://www.morrama.com/projects/kibu-headphones) | The project explains how assembly, printing and material choices affect the object. Its discussion of FDM layers connects manufacturing to appearance. | For the trophies, write about a visible, documented decision instead of listing software or generic claims of expertise. |
| [Nervous System: Kinematics Jewelry](https://n-e-r-v-o-u-s.com/projects/kinematics/kinematics-jewelry/) | A short explanation covers the nylon material, SLS process, integrated hinges and surface finish beside the object images. | Use this degree of technical clarity. The older visual layout is less relevant than the concise content. Their process and materials are not evidence about your work. |
| [Luca Toral: Archive](https://www.lucatoral.com/archive) | A dense collection of jewellery and related objects establishes breadth; the main site positions CAD, concept development and production support clearly. | Separate selected projects from a larger archive when your available work supports both. Keep jewellery as the leading discipline. |
| [Esha More](https://eshamore.link/) | A small selection of featured objects is separated from smaller explorations. Case studies reveal sketches, mockups and CAD. | Make the strongest work easy to choose. Shorten the initial story and let the reviewer choose to see the rest. |

Browser inspection covered the sites above. Phone-width inspection additionally covered LAYER, BLOND and Kyle Anthony. This review concerns their visible presentation, not independent verification of their project claims or a performance audit.

The strongest combination for this portfolio is **LAYER for browsing, BLOND for project storytelling, Sarah Eisman for image direction, and Kyle Anthony for CAD inspection**. Morrama and Nervous System supply the technical-content references for printed objects.

## How this fits the existing portfolio

- The main Work page remains the entry to the broader portfolio, with a prominent Jewellery Design link.
- Jewellery Design opens a compact collection of genuine jewellery projects. Amara leads. The available assets determine the number of cards; an incomplete collection should not be padded with invented projects.
- Printed Objects is a sibling area reached from the main Work page. Trophies and medals belong there, outside jewellery.
- CAD is evidence within the corresponding project. A drawings index may provide another route to it, but a drawing, a render and the finished concept should not be counted as three separate projects.

Keep the attached reference image's dark background, serif title and pale image field as a possible visual direction. Make the opening shorter and place project choices close to it. Large empty introductions, hover-only names and forced scroll sequences work against the agreed browsing goal.

## Project index and optional depth

An index card needs a strong final image, project name, one short description of the contribution, and a clear project link. Add a small stage label where it helps distinguish a design model from a manufactured object. The default view is always the final design.

Inside a project, the first screen should contain the strongest image and a brief description. A short navigation can lead directly to Design decisions, CAD and Specification. Sketches and wireframes can be exposed through simple view controls or links, so reviewers can inspect them without first reading the entire story.

For Amara, use the actual necklace photograph beside the companion-stud design. Label the necklace as the existing reference and the stud as the new design. The comparison shows how their forms relate; differently cropped photographs do not establish physical scale or fit. Reconstructing the pendant is unnecessary.

Drafts should explain decisions: what was considered, what changed, and why the selected direction was chosen. Use the existing drafts where available. Any drawing made after the finished model should be labelled as a retrospective form study, rather than presented as an original historical sketch. Do not invent rejected options or reasons the designer has not supplied.

For Zenith Cup, the supplied assets already support a genuine sketch / wireframe / final presentation: the award-design PDF contains sketches, preview6 and preview7 are wireframe views, and the numbered renders provide final and detail views. Exact sketch-to-model matches still need checking before publication. Rendered gold surfaces do not establish the physical material or finish.

Each trophy specification has only four fields: Dimensions, Materials, Printing process and Finish. Use **—** for information that cannot be verified from the supplied files. A Blender measurement needs confirmed units and scale before being presented as a physical dimension. Avoid adding mass, tolerances, production claims or manufacturing stories without evidence.

## Motion and mobile behaviour

Motion should help orientation while leaving browsing immediate. Text, images and project links remain visible. Use a brief image movement as a section enters view; avoid waiting for paragraphs to reveal in sequence. Do not introduce scroll capture, forced snapping or a pinned story the reviewer must finish.

Use two compact columns in the phone object index for quick comparison, with visible project names and direct taps. Individual projects use a single column and a larger image. The design should work with motion removed. This follows the approach described in the [W3C guidance on interaction animation](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions) and its [reduced-motion CSS technique](https://www.w3.org/WAI/WCAG22/Techniques/css/C39).

## First changes applied locally

The first pass removes the delayed, blurred text reveal. All browsing content is visible immediately; non-hero images have an optional 8 px movement over 240 ms, with reduced-motion styling. The reconstructed pendant has been removed from the jewellery landing page and Workbench. The generic printing illustration and sample trophy content have also been removed from jewellery; an actual Amara profile view now introduces the drawings.

The Amara case-study source and its approved assets remain intact. This first pass was followed by the implemented collection described below.

Validation: type checking and the production build passed. The live local preview was inspected at 1280 × 720 and 390 × 844. Jewellery overview, Amara and Workbench navigation, model-view switching, image loading and page widths were checked. The routes, model images, annotated drawings and specification PDF returned HTTP 200. No warnings or errors were recorded in the reviewed browser tab. The Amara case-study source retained its original SHA-256 hash. Reduced-motion behaviour was checked in the source; the operating-system preference was not changed for this review.

## Implemented collection — 30 September 2026

The jewellery landing page now presents Amara immediately, beside the actual necklace reference photograph on desktop. The existing case study provides optional depth; drawings and the technical sheet have direct links. Jewellery currently contains one independently verified project. The user has confirmed additional actual jewellery CAD and beauty renders; these should become jewellery projects when their source files are identified, rather than being folded into Printed Objects or represented by placeholders.

Printed Objects is a sibling collection at `/objects`, with ten projects, filters for awards and medals, individual project pages, 30 supplied model views, Zenith's two actual wireframes, and an optional section showing the original award drawings. The full original PDF remains available. Both collections are linked from the main Work page and the global navigation. Content is visible immediately, with restrained image movement; route changes start at the top and browser history restores the previous position.

Each printed-object specification has only Dimensions, Materials, Printing process and Finish. All four currently show “—”: the supplied renders and read-only Blender metadata do not establish the intended physical print dimensions, actual material, printing process or applied finish. Render shaders are not manufacturing evidence. The original models were not modified. File mapping and inspection evidence are recorded in `printed-objects-sources.json` and `printed-objects-model-audit.json`.

Final validation: type checking and the production build passed. Development and production previews were inspected at 1280 × 800 and 390 × 844. All ten project pages loaded in development; production gallery, project navigation, wireframe switching and jewellery navigation were checked. Award and medal filtering, original-sketch disclosure, Amara design anchor, drawing links and main-page collection entries were exercised. No horizontal overflow or browser warnings/errors appeared in the reviewed views. All 86 checked routes and image/document links returned HTTP 200. All 30 full-size render copies matched their source-file hashes. Amara's case-study source retained SHA-256 `A242121C5765DA5A4DF30EDECC5CAEA54638AAF8B757DF26E9533C65D58C3C96`. Screenshots are saved in `screenshots/collection`. Reduced-motion handling was reviewed in the source; the operating-system preference was not changed.

## Subsequent jewellery revision — 30 September 2026

The owner authorised a wider slideshow with AI placeholders while actual jewellery renders are being gathered. The landing page now has two labelled temporary concept images, followed by a separate Amara exploration. The placeholders are not presented as actual portfolio projects. Original images and the final generation prompts are recorded in `jewellery-showcase-placeholders.md`.

Amara's presentation was revised with the owner's approval: the opening question and necklace lead, followed by collection reasoning, the drop/classic/folded options, the selected actual model, CAD, specification and optional supplier planning. The fictional “Brief” was removed. The text now speaks in the owner's first person. Research is cited alongside the relevant reasoning; public bestseller merchandising is distinguished from private sales. Supplier progress and cost are described truthfully as unresolved next decisions. See `amara-collection-research.md`. Model files, actual CAD images, annotated drawings and the technical PDF remain unchanged; the earlier case-page source hash above applies to the prior implementation, not this authorised narrative revision.

The public printed-object note about “supplied files” was removed; all four unknown fields still use “—”. Final checks covered slideshow controls, keyboard navigation, direction selection, supplier disclosure, direct CAD anchors, model-view switching and specification links. Development and production pages rendered at desktop and phone widths with no horizontal overflow or recorded console warnings/errors. Type checking and the production build passed. The original technical PDF remains SHA-256 `AC58FE9736C96819A08C898C79E6E50B930D601AB03745F8DAEAFB372BACF6E7`. Reduced-motion behavior and touch-swipe handling were reviewed in source; the operating-system preference and a physical touch device were not used for these checks.
