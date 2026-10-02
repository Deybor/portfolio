# Amara story refinement

Reviewed the three pages of `C:/Users/Master/Downloads/Untitled document.pdf`, including its screenshots, on 30 September 2026. The PDF is the user's design critique, not evidence of product sales or manufacture.

## Reviewer and visual-design decisions

- Keep the question, replace the opening with the owner's requested first-person description. Remove the two generic hero buttons. A quiet scroll cue establishes the sequence; the technical shortcut sits in the corner and the page navigation keeps drawings and specification available.
- Replace the duplicate collection commentary with one reason for choosing Amara and a specific competitor example. Mejuri's named gemstone studs and huggies are public merchandising signals; their combination informs a design hypothesis, not a claim about Itura customer behaviour. Retain validation detail on demand.
- Show Scaled miniature, Nest and A drop together. All descriptions remain visible, with gentle zoom on pointer hover or keyboard focus. The two unprovided alternatives use cropped, labelled retrospective concept illustrations; they are not actual CAD models or early sketches. The five newly supplied renders all depict Nest.
- Show Nest first, then move its render left to make space for the choice. The desktop sequence uses native scrolling over a short 155svh section and transform/opacity only. It does not intercept wheel or touch input. On phones, short screens and reduced-motion settings the image and text are presented in ordinary document flow. A motion control also stops the desktop effect without changing the section's height.
- Replace the old model-view-first section with three SVG line studies projected from actual evaluated CAD geometry. Show only existing dimensions. Keep detailed annotated cards behind a disclosure, and keep the original technical PDF and Workbench available.
- Use supplied Nest beauty renders for the finished-design presentation: 05 for the choice reveal and landing invitation, 03 for the overview slideshow and paired study, 04 for front/reverse, 02 for another view of the pair.

## References and application

[Apple AirPods Pro](https://www.apple.com/airpods-pro/) combines large product imagery, a closer inspection section and persistent access to specifications. Its live page's image resources were partially unavailable in this browser, so no frame-by-frame animation claim is made. The applicable lesson is image-led hierarchy and separate technical access.

[Lusion](https://lusion.co/) gives immersive imagery a distinct role while providing named project links. It was inspected in the browser. Applied here as visual pacing and restrained navigation; this portfolio does not need a WebGL world or custom scrolling.

[W3C C39](https://www.w3.org/WAI/WCAG22/Techniques/css/C39) supports enabling optional movement only for visitors who have not requested reduced motion. The page's default content remains readable without the effect, and mobile uses a simple stacked layout.

[Mejuri's best-selling earrings](https://mejuri.com/collections/best-selling-earrings) lists Gemstone Mini Studs and Lab Grown Sapphire Marquise Cut Studs alongside huggies. [Missoma's styling guide](https://us.missoma.com/blogs/the-chain/how-to-stack-style-your-earrings) provides stacking context. These sources were refreshed for this revision. No competitor sales numbers or Itura conversion rates are inferred.

## Asset provenance

Original beauty images: `C:/Users/Master/Documents/itura/amara stud images/1.png` through `5.png`. Web copies: `public/jewellery/amara-nest/beauty/01.webp` through `05.webp`. Original PNGs are unchanged.

The three direction cards now use the supplied `amara earing refrence 4.png` (Miniature Heart), `amara earing refrence 2.png` (Nest) and `amara earing refrence 5.png` (Unfurl) from `C:/Users/Master/Documents/itura`. Their WebP copies are in `public/jewellery/amara-nest/directions`. Full 3:2 compositions preserve both the product and wearing illustrations, with the existing hover effect and full-image links. These cards are labelled concept illustrations; the actual CAD beauty renders remain in the finished-design sections. The miniature description no longer mentions two beads, which this image does not show. Original files are unchanged.

Line-study source: `C:/Users/Master/Documents/itura/FINAL/absolute final.blend`. Exporter: `scripts/export-amara-line-studies.py`. The background export evaluates meshes, projects visible silhouette and crease edges, and writes SVGs only. It never saves or edits the Blender file. Dimensions come from the existing technical specification. These are retrospective CAD-derived drawings, not dated early design sketches or manufacturing certification.

Existing technical PDF, orthographic renders and annotated SVG cards are unchanged. Proposed finishes remain proposed; the beauty renders do not prove a manufactured satin finish.

## Verification

Typecheck, final production build and scoped formatting checks passed. Desktop (1280 × 800) and phone (390 × 844) were visually inspected in development and built previews. The desktop reveal was checked at two scroll positions (copy hidden before the shift, visible after it); turning motion off kept the section height unchanged. Phone used the static layout with no horizontal overflow. The drawing disclosure, page anchors, real-render/placeholder slideshow states and PDF target were checked. No warning or error console messages were recorded in those checks. All three routes, five WebP renders, three line-study SVGs and the specification returned HTTP 200 in the built preview.

The specification SHA-256 remains `AC58FE9736C96819A08C898C79E6E50B930D601AB03745F8DAEAFB372BACF6E7`. The Blender file SHA-256 was unchanged across the final export: `2611F21A79B654CC2D3034C433D32E2FA89AA115F4ED36637C7D52FD4E23325D`.

The replacement direction images passed a new typecheck and production build. All three WebP targets returned HTTP 200 with image/webp content type. The built preview was visually checked at 1280 × 800 and 390 × 844: all three compositions loaded, retained their 3:2 framing and caused no horizontal overflow. The preview recorded no browser warnings or errors. Desktop proof: `screenshots/collection/amara-directions-updated-desktop.jpg`.
