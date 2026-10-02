"""Build the HTML spec from the shared table data."""
import json, html
from pathlib import Path
root = Path(__file__).resolve().parents[1]
groups = json.loads((root/'src/data/amara-spec.json').read_text(encoding='utf-8'))
table = ''.join('<tr class="group"><th colspan="2">'+html.escape(g['heading'])+'</th></tr>'+''.join('<tr><th scope="row">'+html.escape(k)+'</th><td>'+html.escape(v)+'</td></tr>' for k,v in g['rows']) for g in groups)
technical = json.loads((root/'public/jewellery/amara-nest/technical49/dimension-register.json').read_text(encoding='utf-8'))
dimension_rows = ''.join('<tr><th scope="row">'+html.escape(name)+'</th><td>'+html.escape(value)+'</td></tr>' for name,value in technical['register'])
drawing_sheets = ''.join('<article class="drawing-sheet" id="'+slug+'"><div class="drawing-heading"><h3>'+label+'</h3><div><a href="technical49/'+file+'" aria-haspopup="dialog" aria-label="View '+label.split(' / ')[1]+' drawing">View drawing ⤢</a><a href="technical49/'+file+'" download aria-label="Download '+label.split(' / ')[1]+' drawing">Download</a></div></div><div class="drawing-window"><a href="technical49/'+file+'" aria-haspopup="dialog"><img src="technical49/'+file+'" alt="'+description+'" loading="lazy"></a></div></article>' for slug,label,file,description in [
    ('assembly-drawing','01 / Assembly','01-assembly.svg','Dimensioned front, top, side and rear views, including overall size, head depth, clear post length and boss diameter'),
    ('post-drawing','02 / Post location and heart shell','02-post-shell.svg','Rear post position from references B and C, shaft and collar diameters, shell-only depth and hatched section through the post axis'),
    ('seat-drawing','03 / Seat and CZ','03-seat-cz.svg','Isolated seat and heart CZ views with width, height and depth dimensions, plus a measured seat section')])
labelled = ''.join('<article class="labelled-model"><div class="drawing-heading"><h3>'+label+'</h3><a href="model49/'+file+'" aria-haspopup="dialog" aria-label="View '+aria+'">View full size ⤢</a></div><div class="labelled-window" tabindex="0" role="region" aria-label="'+label+' — scroll to inspect"><img src="model49/'+file+'" width="1400" height="'+height+'" loading="lazy" alt="'+alt+'"></div></article>' for label,file,height,aria,alt in [
    ('Parts of the stud','parts-assembled.svg','820','labelled assembled model','Assembled front and side views, labelled outer shell, heart-cut CZ, upper and lower prongs, post and attachment boss'),
    ('Stone and seat','parts-exploded.svg','920','labelled stone and seat','Exploded view labelled heart-cut CZ, stone seat and upper and lower prongs')])

doc = '''<!doctype html>
<html lang="en"><head><link rel="icon" type="image/svg+xml" href="/favicon.svg"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Amara Nest — specification | Adesina Adebola</title><link rel="stylesheet" href="specification.css"><link rel="stylesheet" href="/image-viewer.css"><script src="/image-viewer.js" defer></script></head>
<body><header class="top"><a href="/jewellery/amara#specification">← Back to Amara</a><a class="spec-download" href="Amara-Nest-Spec-Sheet-Rev49.pdf" download>Download PDF</a><button type="button" id="print-sheet">Print</button></header>
<main><div class="heading"><p>ADESINA ADEBOLA / INDEPENDENT DESIGN STUDY</p><h1>Amara Nest</h1><p class="subtitle">Specification</p></div>
<section class="overview" aria-label="Model and specification"><figure class="model"><a href="model49/model-overview.svg" aria-haspopup="dialog"><img src="model49/model-overview.svg" width="1000" height="1400" alt="Front and side sketches with overall width, height and depth dimensions, plus an isometric view"></a><figcaption>Model sketches · <a href="model49/model-overview.svg" aria-haspopup="dialog">View full size ⤢</a></figcaption></figure><table><caption>Gem, metal and model dimensions</caption><tbody>TABLE</tbody></table></section>
<p class="note">Model dimensions before finishing. Proposed metal and finish. Estimated weight in silver and CZ excludes backs. Unit cost is a planning target; sample approval pending.</p>
<section class="technical-drawings" id="technical-drawings"><h2>Technical drawings</h2><p class="drawing-intro">Assembly, post position, shell and stone seat. All dimensions are in millimetres. </p><nav class="drawing-links" aria-label="Technical drawing sheets"><a href="#assembly-drawing">Assembly</a><a href="#post-drawing">Post &amp; shell</a><a href="#seat-drawing">Seat &amp; CZ</a></nav>SHEETS<details class="dimension-register"><summary>Dimension index</summary><table><caption>Key dimensions</caption><tbody>DIMENSION_ROWS</tbody></table></details></section>
<section class="model-parts" id="model-parts" aria-label="Labelled model views"><h2>Parts and assembly</h2><p>The shell, stone, seat and post, shown together and with the CZ lifted out.</p>LABELLED</section>
<footer>Amara Nest · Adesina Adebola · Independent companion concept for the ÌTURA Amara necklace</footer></main>
<script>document.getElementById('print-sheet').addEventListener('click',function(){window.print()});</script></body></html>'''.replace('TABLE',table).replace('SHEETS',drawing_sheets).replace('DIMENSION_ROWS',dimension_rows).replace('LABELLED',labelled)
out = root/'public/jewellery/amara-nest'
(out/'specification.html').write_text(doc,encoding='utf-8')
print('UPDATED_CASE_AND_HTML_SPECIFICATION')

