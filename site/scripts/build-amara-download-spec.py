"""Complete specification PDF: shared table and three vector drawing sheets."""
from pathlib import Path
import json, re, math, xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import pypdfium2 as pdfium

root=Path(__file__).resolve().parents[1]
assets=root/'public/jewellery/amara-nest'
out=assets/'Amara-Nest-Spec-Sheet-Rev49.pdf'
qa=root/'tmp/pdfs/amara-spec-review';qa.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('Body',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Bold',r'C:\Windows\Fonts\arialbd.ttf'))
c=canvas.Canvas(str(out),pagesize=(420*mm,297*mm),pageCompression=1)
c.setTitle('Amara Nest - complete specification - revision 49')
c.setAuthor('Adesina Adebola')

def text(x,y,value,size=3,bold=False,anchor='start'):
    value=value.replace('⌀','Ø')
    c.saveState();c.translate(x,y);c.scale(1,-1)
    c.setFont('Bold' if bold else 'Body',size);c.setFillColor(HexColor('#202020'))
    offset=0 if anchor=='start' else -pdfmetrics.stringWidth(value,'Bold' if bold else 'Body',size)/(2 if anchor=='middle' else 1)
    c.drawString(offset,0,value);c.restoreState()

def wrap(x,y,value,width,size=3,leading=4.8):
    row=''
    for word in value.split():
        trial=(row+' '+word).strip()
        if pdfmetrics.stringWidth(trial,'Body',size)>width:
            text(x,y,row,size);y+=leading;row=word
        else:row=trial
    if row:text(x,y,row,size);y+=leading
    return y

def path(value):
    tokens=re.findall(r'[MLZ]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',value)
    p=c.beginPath();i=0;points=[]
    while i<len(tokens):
        command=tokens[i];i+=1
        if command=='Z':p.close();continue
        if command not in ['M','L']:raise ValueError('Unsupported SVG command')
        x,y=float(tokens[i]),float(tokens[i+1]);i+=2;points.append((x,y))
        (p.moveTo if command=='M' else p.lineTo)(x,y)
    return p,points

def arrow(tip,other):
    angle=math.atan2(tip[1]-other[1],tip[0]-other[0]);dx,dy=math.cos(angle),math.sin(angle)
    p=c.beginPath();p.moveTo(*tip)
    p.lineTo(tip[0]-2.5*dx+.9*dy,tip[1]-2.5*dy-.9*dx)
    p.lineTo(tip[0]-2.5*dx-.9*dy,tip[1]-2.5*dy+.9*dx);p.close()
    c.setFillColor(HexColor('#202020'));c.drawPath(p,stroke=0,fill=1)

def sheet(svgfile):
    # This controlled SVG subset uses M/L/Z paths, plain text, rectangles,
    # two arrow markers and clipped section hatching. All geometry stays vector.
    c.saveState();c.translate(0,297*mm);c.scale(mm,-mm)
    for e in ET.parse(svgfile).getroot():
        tag=e.tag.split('}')[-1];cls=e.get('class','')
        c.saveState();c.setStrokeColor(HexColor('#202020'));c.setLineWidth(.18)
        if tag=='rect':
            c.setLineWidth(.5 if cls=='border' else .18)
            colour=e.get('fill','#ffffff')
            if len(colour)==4:colour='#'+''.join(v*2 for v in colour[1:])
            c.setFillColor(HexColor(colour))
            c.rect(float(e.get('x',0)),float(e.get('y',0)),float(e.get('width')),float(e.get('height')),stroke=bool(cls),fill=not bool(cls))
        elif tag=='path':
            p,points=path(e.get('d',''))
            c.setLineWidth({'object':.35,'feature':.18,'centre':.15,'cut':.45,'section':.3}.get(cls,.18))
            if cls in ['centre','cut']:c.setDash([6 if cls=='centre' else 7,1.2,1.2,1.2])
            if cls=='feature':c.setStrokeColor(HexColor('#333333'))
            if cls=='centre':c.setStrokeColor(HexColor('#777777'))
            if cls=='section':
                c.saveState();c.clipPath(p,stroke=0,fill=0,fillMode=0)
                c.setStrokeColor(HexColor('#555555'));c.setLineWidth(.13)
                lo=min(q[0] for q in points);hi=max(q[0] for q in points)
                top=min(q[1] for q in points);bottom=max(q[1] for q in points)
                for k in range(math.floor((lo+top)/2),math.ceil((hi+bottom)/2)+1):
                    c.line(lo,2*k-lo,hi,2*k-hi)
                c.restoreState()
            c.drawPath(p,stroke=1,fill=0)
            if e.get('marker-start'):arrow(points[0],points[1])
            if e.get('marker-end'):arrow(points[-1],points[-2])
        elif tag=='text':
            if e.get('transform'):
                x,y,angle=map(float,re.findall(r'[-+]?\d*\.?\d+',e.get('transform')))
                c.translate(x,y);c.rotate(angle);x=y=0
            else:x,y=float(e.get('x',0)),float(e.get('y',0))
            if cls=='dimension':
                # Match SVG's white paint-order around dimension labels.
                value=(e.text or '').replace('⌀','Ø');size=float(e.get('font-size',3))
                width=pdfmetrics.stringWidth(value,'Body',size)
                c.setFillColor(HexColor('#ffffff'));c.rect(x-width/2-.3,y-size,width+.6,size+1,stroke=0,fill=1)
            text(x,y,e.text or '',float(e.get('font-size',3)),cls=='title',e.get('text-anchor','start'))
        c.restoreState()
    c.restoreState();c.showPage()

c.saveState();c.translate(0,297*mm);c.scale(mm,-mm)
c.setFillColor(HexColor('#ffffff'));c.rect(0,0,420,297,stroke=0,fill=1)
c.setLineWidth(.5);c.rect(10,10,400,277,stroke=1,fill=0)
text(18,24,'AMARA NEST / SPECIFICATION',7,True)
text(18,33,'ADESINA ADEBOLA / INDEPENDENT DESIGN STUDY / REV 49',3)
c.line(10,40,410,40)
text(18,52,'Model and construction',4,True)
text(202,52,'Gem, metal and dimensions',4,True)
image=Image.open(assets/'model49/oblique-clay.webp').convert('RGBA')
c.saveState();c.translate(23,70+158);c.scale(1,-1);c.drawImage(ImageReader(image),0,0,158,158,mask='auto');c.restoreState()
text(102,237,'3D model / one stud',3,anchor='middle')
y=59
for group in json.loads((root/'src/data/amara-spec.json').read_text(encoding='utf-8')):
    c.setFillColor(HexColor('#eee9e1'));c.rect(202,y,196,8,stroke=0,fill=1)
    text(206,y+5.5,group['heading'].upper(),3,True);y+=8
    for key,value in group['rows']:
        # Two fixed columns; calculate row height from wrapped content.
        c.setStrokeColor(HexColor('#c9c1b4'));c.setLineWidth(.18)
        left=wrap(206,y+5,key,74,2.7,4)
        right=wrap(286,y+5,value,107,2.7,4)
        height=max(left,right)-y+1
        c.rect(202,y,196,height,stroke=1,fill=0);c.line(282,y,282,y+height);y+=height
text(18,252,'Design study for sample review.',3.2,True)
wrap(18,260,'Model dimensions before finishing. Proposed metal and finish. Estimated weight in silver and CZ excludes backs. Sample approval required for CZ fit, post attachment and finishing.',182,3,4.6)
text(202,265,'Contents',3.2,True)
text(202,272,'Specification / Assembly / Post and shell / Seat and CZ',2.8)
text(202,281,'All dimensions in mm / drawing scales at A3',2.8)
c.restoreState();c.showPage()
for filename in ['01-assembly.svg','02-post-shell.svg','03-seat-cz.svg']:sheet(assets/'technical49'/filename)
c.save()
pdf=pdfium.PdfDocument(str(out))
for i in range(len(pdf)):pdf[i].render(scale=1.0).to_pil().save(qa/f'page-{i+1}.png')
print('COMPLETE_SPEC_PDF',len(pdf),'pages',str(out))
