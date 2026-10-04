"""Check approved solid/line/section sheets and frozen source preservation."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image
root=Path(__file__).resolve().parents[1];folder=root/'public/jewellery/confluence'
reader=PdfReader(folder/'technical-specification.pdf')
assert len(reader.pages)==8
assert len(list(reader.pages[0].images))==1,'The overview must show the shaded frozen body'
assert len(list(reader.pages[1].images))==0,'Approved assembly dimensions must be native vector line drawings'
assert len(list(reader.pages[2].images))==4,'Construction must show the actual A-A slice, square-on cut, locator and setting detail'
for svg in sorted((folder/'technical').glob('[0-9][0-9]-*.svg')):
    document=ET.parse(svg).getroot()
    images=list(document.iter('{http://www.w3.org/2000/svg}image'))
    assert len(images)==(4 if svg.name.startswith('03-') else 1 if svg.name.startswith('01-') else 0),svg
    text=' '.join(element.text or '' for element in document.iter('{http://www.w3.org/2000/svg}text'))
    assert ('REVIEW 04' if svg.name.startswith('02-') else 'REVIEW 03' if svg.name.startswith(('01-','03-')) else 'SPEC C') in text,svg
    if svg.name.startswith('01-'):
        assert 'SOLID MODEL / PRE-SETTING METAL BODY' in text
    if svg.name.startswith('02-'):
        assert all(label in text for label in ['FRONT / X-Z','SIDE / Y-Z','TOP / X-Y'])
        assert {element.get('data-model-drawing') for element in document.iter('{http://www.w3.org/2000/svg}path') if element.get('data-model-drawing')}=={'front','side','top'}
        assert 'D-D / LOWER-SHANK DETAIL' in text
        assert '3.90 REF.' in text and 'horizontal X' in text and 'offsets.' in text
    if svg.name.startswith('03-'):
        assert 'A-A / SLICED 3D MODEL' in text
        assert 'A-A / CUT FACES + RETAINED BODY' in text
        assert 'SECTION LOCATION / WHOLE MODEL' in text
        assert '2.77 REF.' in text and 'Z20.00 REF.' in text
        assert 'Rail stock: Ø0.64 centre / Ø0.56 sides NOM.' in text
        assert any(element.get('fill')=='url(#cut-hatch)' for element in document.iter('{http://www.w3.org/2000/svg}path'))
data=json.loads((root/'docs/ring-specification-cad-data.json').read_text())['confluence']
refinement=data['centre_prong_refinement']
for path,expected in [(data['source'],data['source_sha256']),(refinement['source'],refinement['source_sha256']),
    (data['original_source'],data['original_source_sha256'])]:
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected
assert data['metal']['boundary_edges']==0 and data['metal']['nonmanifold_edges']==0
doc=pdfium.PdfDocument(str(folder/'technical-specification.pdf'))
sheet=Image.new('RGB',(1200,440),'#dedede')
for index in range(8):
    image=doc[index].render(scale=.65).to_pil().convert('RGB');image.thumbnail((296,210))
    sheet.paste(image,((index%4)*300,(index//4)*220))
sheet.save(root/'.qa/confluence-spec-c-all-pages.png')
for index in [1,2,7]:doc[index].render(scale=1.4).to_pil().save(root/'.qa'/f'confluence-spec-c-page-{index+1}.png')
doc.close()
print('Approved Confluence release: solid overview, vector assembly drawings, actual A-A section and setting details; eight-page PDF; source models preserved')
