# Printed object study exports

Beauty renders and existing Zenith wireframes are preserved. Each of the ten projects has an additional clay render and a mesh wireframe exported from a matching Blender assembly. Studio lights, backdrops, trees, curtains and unused alternate collections are excluded. Subdivision is disabled only in disposable wireframe staging copies; other construction modifiers remain. Native polygon edges are used, rather than a triangulating wire shader. No source .blend is saved.

Each wireframe gallery also includes an actual Blender 3D viewport export with the theme background, grid and axes retained. `scripts/capture-printed-viewports.py` runs in a separate Blender UI process and uses `render.opengl` with a VIEW_3D context. `printed-viewport-audit.json` records the capture method and source hash preservation. These snapshots supplement the original wireframes. The thumbnail label is Viewport and the caption is Blender viewport.

Named files do not always match the supplied beauty render. Verified source overrides are in `scripts/render-printed-studies.py`: World uses `new/lets upload/second.blend`; Top Campus Ministry uses `white back/throuphy upload/6.blend`; Top Zone uses `white back/untitled2.blend`; Projects & Programs uses `white back/throuphy upload/5.blend`. Other projects use the named files in `new/cad-3d print`.

`printed-study-<slug>.json` records the exact source path, SHA-256, selected assembly parts and source-preservation result. `printed-geometry-audit.json` records the initial named-file geometry and hashes.

## Dimensions

Seven of ten projects have dimensioned front/side silhouettes and downloadable drawings. These are measured model dimensions. Materials, printing method, finish and tolerances remain unconfirmed. Working scale varies between source files; no rescaling is applied to the measurements.

| Model | Width | Depth | Height |
| --- | --- | --- | --- |
| Zenith Cup | 214.6 mm | 224.2 mm | 576.1 mm |
| World | 2545.1 mm | 1426.0 mm | 2517.1 mm |
| Top Campus Ministry | 189.8 mm | 189.1 mm | 406.9 mm |
| Top Zone Trophy | 935.0 mm | 802.7 mm | 2038.2 mm |
| Bible Projects for Programs | 410.4 mm | 307.8 mm | 893.1 mm |
| Individual Category | 146.5 mm | 157.1 mm | 374.0 mm |
| Vit | 657.1 mm | 449.1 mm | 1601.4 mm |

Measurements are extents over all evaluated mesh vertices in the selected assembled model, including decorative details. Drawings use -Y for the front, with width X and depth Y. Individual Category uses +X for the front, with width Y and depth X. All use height Z. Blender unit scale is applied before conversion to millimetres. Drawing outlines are traced from transparent orthographic masks of the same evaluated geometry. The front and side views retain the same proportional model scale.

## Regeneration

Run `scripts/render-printed-studies.py` with Blender in background mode. An optional list of project slugs after `--` limits exports. Add `--dimensions-only` after `--` to preserve existing clay and wireframe exports while adding drawings. Then run `scripts/package-printed-studies.py` with Python plus Pillow and NumPy. This adds generated views without replacing beauty renders or the existing Zenith wireframes.

Full Blender workspace screenshots accompany every wireframe gallery. Captured directly with Blender screen.screenshot in a separate disposable session, with native toolbars, Outliner, timeline, grid and varied perspective angles. Source files were opened but never saved; source hashes are recorded in printed-workspace-audit.json.

References: seven visually matched designs cropped from the original award-designs.pdf. Tab order places References after Dimensions. Page numbers are preserved in captions; crop bounds and unchanged PDF hash are in printed-reference-audit.json. No reference was assigned to Zenith, World or Medal.

Tuff and Projects & Programs now have measured front/side dimension drawings, completing dimension coverage for all seven models with reference drawings. Original source geometry and all reference images preserved.
