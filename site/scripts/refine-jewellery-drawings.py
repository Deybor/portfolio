"""Build readable portfolio sheets from original orthographic CAD views and measurements."""
from pathlib import Path
from io import BytesIO
import base64, json, hashlib, xml.etree.ElementTree as ET
from html import escape
from PIL import Image, ImageChops
from pypdf import PdfReader
import pypdfium2 as pdfium
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES')
W, H = 1400, 1000
INK, LINE = '#20313b', '#56646a'

def tight(image):
    image = image.convert('RGBA')
    if image.getchannel('A').getextrema()[0] < 255:
        bounds = image.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    else:
        bounds = ImageChops.difference(image.convert('RGB'), Image.new('RGB', image.size, 'white')).convert('L').point(lambda v: 255 if v > 15 else 0).getbbox()
    return image.crop(bounds)

class Sheet:
    def __init__(self, slug, title, subtitle):
        self.out = ROOT / 'public/jewellery' / slug
        self.pdf = canvas.Canvas(str(self.out / 'dimensions.pdf'), pagesize=(W, H))
        self.pdf.setTitle(title + ' - CAD dimensions')
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" style="max-width:100%;height:auto;display:block" viewBox="0 0 {W} {H}"><title>{escape(title)} - CAD dimensions</title><rect width="100%" height="100%" fill="white"/>']
        self.text(52, 66, title.upper(), 34, True)
        self.text(52, 107, subtitle, 23)
        self.text(1170, 66, 'CAD / mm', 24, True)
        self.line(52, 132, 1348, 132)

    def text(self, x, y, text, size=24, bold=False, anchor='start'):
        self.pdf.setFillColor(INK)
        self.pdf.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
        if anchor == 'middle': self.pdf.drawCentredString(x, H-y, text)
        elif anchor == 'end': self.pdf.drawRightString(x, H-y, text)
        else: self.pdf.drawString(x, H-y, text)
        self.svg.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}" fill="{INK}">{escape(text)}</text>')

    def line(self, x1, y1, x2, y2, width=1.5):
        self.pdf.setStrokeColor(LINE); self.pdf.setLineWidth(width)
        self.pdf.line(x1, H-y1, x2, H-y2)
        self.svg.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{LINE}" stroke-width="{width}"/>')

    def arrow(self, x, y, dx, dy):
        pts = [(x,y),(x+dx*10-dy*4,y+dy*10+dx*4),(x+dx*10+dy*4,y+dy*10-dx*4)]
        self.pdf.setFillColor(LINE)
        p = self.pdf.beginPath(); p.moveTo(pts[0][0], H-pts[0][1])
        for px,py in pts[1:]: p.lineTo(px,H-py)
        p.close(); self.pdf.drawPath(p,fill=1,stroke=0)
        self.svg.append(f'<polygon points="{" ".join(f"{px},{py}" for px,py in pts)}" fill="{LINE}"/>')

    def hdim(self, x1, x2, edge_y, line_y, text):
        self.line(x1, edge_y, x1, line_y+8); self.line(x2, edge_y, x2, line_y+8)
        self.line(x1, line_y, x2, line_y)
        self.arrow(x1,line_y,1,0); self.arrow(x2,line_y,-1,0)
        self.text((x1+x2)/2,line_y+34,text,25,anchor='middle')

    def vdim(self, y1, y2, edge_x, line_x, text):
        self.line(edge_x,y1,line_x+8,y1); self.line(edge_x,y2,line_x+8,y2)
        self.line(line_x,y1,line_x,y2)
        self.arrow(line_x,y1,0,1); self.arrow(line_x,y2,0,-1)
        self.text(line_x+18,(y1+y2)/2+8,text,25)

    def image(self, image, x, y, w, h):
        data=BytesIO(); image.save(data,format='PNG'); data=data.getvalue()
        self.pdf.drawImage(ImageReader(BytesIO(data)),x,H-y-h,w,h,mask='auto')
        self.svg.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(data).decode()}"/>')

    def finish(self):
        self.pdf.showPage(); self.pdf.save()
        self.svg.append('</svg>')
        (self.out/'dimensions.svg').write_text(''.join(self.svg),encoding='utf-8')
        doc=pdfium.PdfDocument(str(self.out/'dimensions.pdf'))
        image=doc[0].render(scale=1.5).to_pil()
        image.save(self.out/'dimensions-01.png')
        image.thumbnail((1800,1800),Image.Resampling.LANCZOS)
        image.convert('RGB').save(self.out/'dimensions-01.webp',quality=94,method=6)
        doc.close()

original_pdf=SOURCE/'Confluence_First_Ring/Renders_and_Dimensions/Confluence_Specification.pdf'
images=[tight(item.image) for item in PdfReader(original_pdf).pages[0].images]
front=max(images,key=lambda i:i.width/i.height)
side=min(images,key=lambda i:i.width/i.height)
s=Sheet('confluence','Confluence','Front and side views / finished ring assembly')
scale=490/23.28
fw,sh=21.42*scale,23.28*scale
sw=6*scale
x,y=210,205
s.text(x,182,'FRONT',24,True)
s.image(front,x,y,fw,sh)
s.hdim(x,x+fw,y+sh,y+sh+40,'21.42')
s.vdim(y,y+sh,x+fw,x+fw+36,'23.28')
x2=1010
s.text(x2-10,182,'SIDE',24,True)
s.image(side,x2,y,sw,sh)
s.hdim(x2,x2+sw,y+sh,y+sh+40,'6.00')
s.line(52,802,1348,802)
s.text(52,843,'RING BORE',20,True); s.text(52,881,'18.00 nominal diameter',24)
s.text(510,843,'STONE DIAMETERS',20,True); s.text(510,881,'5.00 centre / 2 x 2.50 sides',24)
s.text(1020,843,'LOWER SHANK / SAMPLED',20,True); s.text(1020,881,'2.50 wide / 1.70 thick',24)
s.text(52,953,'Dimensions in mm. Overall assembly measured from CAD; stone sizes are nominal.',21)
s.finish()

original_svg=SOURCE/'Ring_Iced_Out_03/Ring_Base_CAD_Drawings.svg'
nodes=[n for n in ET.parse(original_svg).iter() if n.tag.endswith('image')]
images=[tight(Image.open(BytesIO(base64.b64decode(n.attrib['href'].split(',')[1])))) for n in nodes]
s=Sheet('iced-out-ring','Iced-out ring','Original base mesh / top, front and side views')
x,y,size=125,220,470
s.text(x,182,'TOP',24,True)
s.image(images[0],x,y,size,size)
s.hdim(x,x+size,y+size,y+size+40,'22.02')
s.vdim(y,y+size,x+size,x+size+34,'22.02')
x2,w=770,470
h=w*4.14/22.02
for image,yy,label in [(images[1],260,'FRONT'),(images[2],552,'SIDE')]:
    s.text(x2,yy-38,label,24,True)
    s.image(image,x2,yy,w,h)
    s.hdim(x2,x2+w,yy+h,yy+h+40,'22.02')
    s.vdim(yy,yy+h,x2+w,x2+w+30,'4.14')
s.line(52,812,1348,812)
s.text(52,854,'OVERALL BASE MESH',20,True); s.text(52,894,'22.02 x 22.02 x 4.14 mm',24)
s.text(760,854,'MINIMUM CLEAR BORE',20,True); s.text(760,894,'17.23 mm / sampled radial sections',24)
s.text(52,953,'Base mesh before beauty-setting refinements. Source units interpreted as mm; size unconfirmed.',21)
s.finish()

audit={'method':'Original orthographic source images; dimensions retained from supplied sheets; new vector labels and layout',
       'original_sources_preserved':True,
       'sources':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [original_pdf,original_svg]},
       'removed':'Revision labels, file paths, mesh counts, workflow history and process text unrelated to reading the drawing',
       'outputs':['confluence/dimensions.pdf','confluence/dimensions.svg','iced-out-ring/dimensions.pdf','iced-out-ring/dimensions.svg']}
(ROOT/'docs/jewellery-drawing-refinement.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('Refined both CAD sheets; source sheets preserved.')
