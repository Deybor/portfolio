# Amara: requested copy, CZ and HTML specification

The user's final paragraph beginning “Amara already has a beautiful heart design” replaces the competitor prose. The starting-point line is now “I wanted to explore what made the heart one of the bestsellers.” The earlier annotated notes and complete section 06 are removed. Current case study and workbench copy use cubic zirconia (CZ).

The spec is now `public/jewellery/amara-nest/specification.html`, with responsive and print styles. Its gem, metal, finish and dimension table comes from `src/data/amara-spec.json`, also used by the inline React table. Materials/finishes remain proposed and unknown weight/cost are shown as em dashes. The earlier PDFs remain archival files; all current portfolio spec links open the HTML sheet.

`sketches49/amara-sketches.svg` is one front/side/back sheet. Its closed outlines are traced from actual orthographic object-colour masks, combined with visible model feature edges. It is labelled model-derived, not presented as a historical hand sketch. Projection data and part masks are retained under the Itura `portfolio-revision/sketch-projections49` folder, outside public assets.

The comparison now uses `oblique-render-hdri.webp`, exported from the newly saved scene with the original `ninomaru_teien_4k.exr` HDRI and Film transparency. Cycles used 128 samples and the same orthographic camera as the wire view. Alpha extrema are 0 and 255. The saved scene was read only; its SHA-256 before and after this export is `85314FD610597397320D2A560516F9E4B33E97584A9D016E72AFA2DFFAEDF055`. The older source hash in the previous revision note predates the user's lighting edit.

The central handle now captures pointer drags, supports keyboard arrows/Home/End and stays synchronised with the bottom range. Actual browser drags changed the desktop value from 50 to 64 and the phone value from 50 to 71. Keyboard Home/Right changed both controls to 1.

Typecheck and final production build passed. Browser checks covered desktop, 390 × 844 phone and 768 × 900 tablet views. The HTML sheet's images loaded and there was no horizontal overflow on phone/tablet. The HTML return link worked; the current case has no moissanite text, earlier notes or section 06. Production routes, HTML/CSS, HDRI image and composite SVG returned HTTP 200. Production browser error/warning logs were empty. Screenshots are saved under `screenshots/collection/`. The port 8080 development preview is retained; this change is local.
