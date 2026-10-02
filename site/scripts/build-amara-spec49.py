"""Versioned portfolio specification using real views from the supplied Amara49 model."""
from pathlib import Path
from io import BytesIO
import textwrap
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pypdfium2 as pdfium

root=Path(__file__).resolve().parents[1]
views=Path(r'C:\Users\Master\Documents\itura\portfolio-revision\views49')
out=root/'public/jewellery/amara-nest/Amara-Technical-Specification-Rev49.pdf'
pdfmetrics.registerFont(TTFont('Body',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Bold',r'C:\Windows\Fonts\arialbd.ttf'))
W,H=1190.55,841.89
ink=HexColor('#211e1a');muted=HexColor('#6e665c');gold=HexColor('#9c7443');paper=HexColor('#f5f1ea');white=HexColor('#ffffff');line=HexColor('#d8d0c3')
c=canvas.Canvas(str(out),pagesize=(W,H))
c.setTitle('Amara Nest - model and proposed specification - Rev 49')
c.setAuthor('Adesina Adebola')
def txt(x,y,text,size=11,bold=False,color=ink):
    c.setFillColor(color);c.setFont('Bold' if bold else 'Body',size);c.drawString(x,y,text)
def wrapped(x,y,text,width,size=11,color=ink,leading=17):
    words=text.split();row=''
    for word in words:
        proposed=(row+' '+word).strip()
        if pdfmetrics.stringWidth(proposed,'Body',size)>width:
            txt(x,y,row,size,color=color);y-=leading;row=word
        else:row=proposed
    if row:txt(x,y,row,size,color=color);y-=leading
    return y
def rule(x1,y,x2):
    c.setStrokeColor(line);c.setLineWidth(.6);c.line(x1,y,x2,y)
def begin(n,title,subtitle):
    c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(ink);c.rect(0,H-72,W,72,fill=1,stroke=0)
    txt(36,H-32,'AMARA NEST / DESIGN STUDY',19,True,white)
    txt(36,H-52,'Adesina Adebola - independent companion concept for ITURA',10,color=paper)
    txt(W-166,H-31,'MODEL REV 49',11,True,white)
    txt(W-166,H-51,f'SHEET {n} / 4',9,color=paper)
    txt(36,H-111,title,24,True)
    txt(36,H-134,subtitle,11,color=muted)
    rule(36,48,W-36)
    txt(36,29,'30 SEP 2026   /   mm   /   Not to scale   /   Digital study - supplier and sample pending',9,color=muted)
    txt(W-83,29,f'{n} / 4',10,True)
def view(name,x,y,w,h,crop=False):
    im=Image.open(views/f'{name}.png').convert('RGBA')
    if crop:
        box=im.getchannel('A').getbbox()
        if box:im=im.crop(box)
    c.drawImage(ImageReader(im),x,y,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
def dimension(x0,y0,x1,y1,label):
    c.setStrokeColor(gold);c.setLineWidth(.7);c.line(x0,y0,x1,y1)
    if y0==y1:
        c.line(x0,y0-5,x0,y0+5);c.line(x1,y1-5,x1,y1+5)
        txt((x0+x1)/2-pdfmetrics.stringWidth(label,'Bold',10)/2,y0-17,label,10,True,gold)
    else:
        c.line(x0-5,y0,x0+5,y0);c.line(x1-5,y1,x1+5,y1)
        c.saveState();c.translate(x0-13,(y0+y1)/2);c.rotate(90);txt(-pdfmetrics.stringWidth(label,'Bold',10)/2,0,label,10,True,gold);c.restoreState()

begin(1,'Model dimensions','Front, back and side views from the supplied Amara49 model, with the updated prongs.')
txt(100,671,'FRONT',11,True,gold);txt(590,671,'BACK',11,True,gold);txt(876,671,'SIDE',11,True,gold)
view('front-clay',100,238,425,420,True)
dimension(100,220,525,220,'9.04 mm width');dimension(78,238,78,658,'9.34 mm height')
view('rear-clay',565,439,250,219,True)
view('side-clay',841,457,302,201,True)
dimension(841,436,1143,436,'16.08 mm total depth')
rows=[('Head','9.04 W x 9.34 H x 5.58 D mm'),('Stone reference','6.00 W x 6.00 H x 3.55 D mm; CZ mesh'),('Post proposal','0.80 mm shaft; 10.50 mm exposed'),('Model post envelope','0.92 mm maximum across the rounded tip')]
for i,(label,value) in enumerate(rows):
    y=396-i*40;rule(565,y-14,1143);txt(565,y,label,11,True);txt(710,y,value,11)
wrapped(565,197,'Head and total depth are measured from the uncoated 3D model. Final dimensions and post/back fit need a supplier sample.',570,11,color=muted)
rule(36,140,W-36)
wrapped(36,118,'This is a digital design study. It is not a production release or proof of fit, setting strength or wear comfort.',1100,11,color=muted)
c.showPage()

begin(2,'Proposed specification','One pair: two studs, two stones and two matching backs. Supplier quotation and sample are still needed.')
txt(36,659,'PARTS AND FINISH',13,True,gold)
items=[('Head','925 sterling silver. Cast shell, stone seat, three prongs and rear attachment boss.'),('Stone','Clear heart-cut moissanite, one per stud. The model uses CZ reference geometry; supplier cut and dimensions are not confirmed.'),('Post and back','925 sterling silver post and butterfly back. Proposed shaft: 0.80 mm; exposed length: 10.50 mm. Confirm supplier parts and attachment.'),('Gold finish','Proposed 18K gold vermeil, with a 3.5 micrometre coating target from the earlier specification. Confirm the coating process and achievable thickness with the supplier.'),('Surface','Proposed satin outer fold, polished rim and prong tips, and a smooth skin-contact back.')]
y=630
for label,value in items:
    txt(36,y,label,12,True);end=wrapped(214,y,value,886,12,leading=19);y=end-23;rule(36,y+12,W-36)
txt(36,y-9,'BEFORE A SAMPLE',13,True,gold)
y=wrapped(36,y-34,'Confirm the actual stone, cut its seats, review prong contact, and check the post/back fit after finishing. Agree tolerances and coating checks with the supplier.',1090,12,leading=19)-22
txt(36,351,'SIZE TARGETS FOR THE FIRST SAMPLE',12,True,gold)
txt(36,326,'Head: 9.04 W x 9.34 H x 5.58 D mm, each +/- 0.20 mm. Post: 0.80 +/- 0.03 mm.',12)
txt(36,304,'Exposed post: 10.50 +/- 0.20 mm. These limits are proposed and need supplier agreement.',11,color=muted)
c.setFillColor(paper);c.rect(36,82,W-72,108,fill=1,stroke=0)
txt(56,166,'COST / QUANTITY / STATUS',11,True,gold)
txt(56,140,'Earlier planning target: NGN 15,000 per pair. No supplier quote yet.',13,True)
txt(56,116,'Minimum order quantity: not confirmed. Stage: digital model, before supplier sample.',11)
txt(56,95,'The cost target is a proposal from the earlier sheet, not a confirmed manufacturing cost.',10,color=muted)
c.showPage()

begin(3,'Parts in the model','The updated prongs, shell, seat and post shown in neutral clay.')
view('front-clay',280,185,560,467,True)
view('side-clay',846,455,299,166,True)
labels=[(36,624,'Outer fold',(428,577)),(36,482,'Reference stone',(589,452)),(36,293,'Lower prong',(605,251)),(928,374,'Post',(1030,565)),(915,262,'Upper prongs',(729,524))]
for x,y,label,(tx,ty) in labels:
    txt(x,y,label,12,True)
    c.setStrokeColor(gold);c.setLineWidth(.7)
    start=x+min(pdfmetrics.stringWidth(label,'Bold',12)+12,150)
    c.line(start,y-4,tx,ty);c.setFillColor(gold);c.circle(tx,ty,2,fill=1,stroke=0)
rule(36,136,W-36)
wrapped(36,113,'The shell and seat surround a CZ reference stone. Moissanite is the proposed production stone; its actual cut and dimensions need to be confirmed before setting.',1100,11,color=muted)
c.showPage()

begin(4,'Stone and seat','The same model, with the reference stone moved up to show the seat and prongs.')
view('exploded-clay',252,148,690,575,True)
for x,y,label,tx,ty in [(36,580,'Reference stone',609,604),(36,375,'Stone seat',540,346),(960,259,'Lower prong',594,196)]:
    txt(x,y,label,12,True);c.setStrokeColor(gold);c.line(x+110,y-4,tx,ty);c.setFillColor(gold);c.circle(tx,ty,2,fill=1,stroke=0)
c.setFillColor(paper);c.rect(36,71,W-72,68,fill=1,stroke=0)
txt(54,116,'STONE CHECK',11,True,gold)
wrapped(54,95,'Confirm the supplier stone’s girdle, pavilion and point before cutting the seats. This exploded view explains the assembly; it does not certify the setting.',1060,11,leading=16)
c.showPage();c.save()
doc=pdfium.PdfDocument(str(out))
for i,p in enumerate(doc):
    png=root/'screenshots/collection'/f'amara-spec49-page-{i+1}.png'
    im=p.render(scale=1).to_pil();im.save(png)
    if i in (0,3):
        im.save(root/'public/jewellery/amara-nest'/('spec49-overview.webp' if i==0 else 'spec49-exploded.webp'),'WEBP',quality=92,method=6)
print('PDF_CREATED',out,'pages',len(doc))
