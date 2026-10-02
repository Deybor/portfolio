from pathlib import Path
from PIL import Image,ImageDraw
from pypdf import PdfReader
import pypdfium2 as pdfium
import xml.etree.ElementTree as ET
import json,hashlib
root=Path(__file__).resolve().parents[1];folder=root/'public/jewellery/confluence'
reader=PdfReader(folder/'technical-specification.pdf')
assert len(reader.pages)==8
text='\n'.join(page.extract_text() for page in reader.pages)
assert 'SPEC B' in text and 'original casting' in text.lower()
assert 'Confluence-Straight-Prong-CAD.blend' not in text
assert 'Z19.65-22.75' not in text
for svg in sorted((folder/'technical').glob('[0-9][0-9]-*.svg')):
    document=ET.parse(svg)
    svg_text=' '.join(t.text or '' for t in document.getroot().iter('{http://www.w3.org/2000/svg}text'))
    assert 'SPEC B' in svg_text,svg
    assert 'New straight axes' not in svg_text,svg
audit=json.loads((root/'docs/ring-specification-cad-data.json').read_text())['confluence']
for path,expected in [(audit['source'],audit['source_sha256']),(audit['original_source'],audit['original_source_sha256'])]:
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected
doc=pdfium.PdfDocument(str(folder/'technical-specification.pdf'))
sheet=Image.new('RGB',(1200,440),'#dedede')
for i in range(8):
    image=doc[i].render(scale=.65).to_pil().convert('RGB')
    image.thumbnail((296,210))
    sheet.paste(image,((i%4)*300,(i//4)*220))
sheet.save(root/'.qa/confluence-spec-b-all-pages.png')
for index in [1,7]:
    doc[index].render(scale=1.2).to_pil().save(root/'.qa'/f'confluence-spec-b-page-{index+1}.png')
doc.close()
print('Eight valid SPEC B sheets; source meshes preserved; PDF and SVG metadata consistent')
