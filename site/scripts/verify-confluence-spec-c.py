"""Check the vector section, shaded model views and frozen CAD preservation."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image
root=Path(__file__).resolve().parents[1];folder=root/'public/jewellery/confluence'
reader=PdfReader(folder/'technical-specification.pdf')
assert len(reader.pages)==8
for index in range(2):assert len(list(reader.pages[index].images))==0
assert len(list(reader.pages[2].images))==2,'The two setting model views must remain shaded'
for svg in sorted((folder/'technical').glob('[0-9][0-9]-*.svg')):
    document=ET.parse(svg).getroot()
    images=list(document.iter('{http://www.w3.org/2000/svg}image'))
    assert len(images)==(2 if svg.name.startswith('03-') else 0),svg
    text=' '.join(element.text or '' for element in document.iter('{http://www.w3.org/2000/svg}text'))
    assert 'SPEC C' in text,svg
    if svg.name.startswith('03-'):
        assert 'FRONT ELEVATION' in text
        assert 'SECTION A-A' not in text
        assert 'front outline' not in text
        assert len([element for element in document.iter() if element.get('id')=='front-elevation-contour'])==1
        assert all(float(element.get('x'))>=450 for element in images)
        assert not any(element.get('stroke')=='#87959c' for element in document.iter())
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
print('SPEC C: one vector front elevation, two shaded setting views; eight-page PDF; source models preserved')
