"""Build traceable, model-led web/PDF specification packs from frozen ring data."""
from pathlib import Path
from io import BytesIO
import json, math, html, base64, hashlib, shutil, sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[1]
SRC=Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES')
DATA=json.loads((ROOT/'docs/ring-specification-cad-data.json').read_text())
VERIFY=json.loads((SRC/'Confluence_First_Ring/Approved_Model/Verification_Refined.json').read_text())
ICED=json.loads((SRC/'Ring_Iced_Out_03/Iced_Revision.json').read_text())
W,H=1190,842
INK='#202b32'; MUTED='#53646c'; ACCENT='#8b7250'; LINE='#ccd3d6'; PALE='#f1f4f4'
escape=html.escape
FONT=Path('C:/Windows/Fonts')
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Spec',str(FONT/'arial.ttf')))
pdfmetrics.registerFont(TTFont('SpecBold',str(FONT/'arialbd.ttf')))
pdfmetrics.registerFontFamily('Spec',normal='Spec',bold='SpecBold',italic='Spec',boldItalic='SpecBold')

class Pack:
    def __init__(self,slug,title,code,revision):
        self.slug=slug; self.title=title; self.code=code; self.rev=revision
        self.out=ROOT/'public/jewellery'/slug
        self.pdf=canvas.Canvas(str(self.out/'technical-specification.pdf'),pagesize=(W,H))
        self.pdf.setTitle(title+' - technical specification'); self.pdf.setAuthor('Adesina Adebola')
        self.page=0; self.web=[]; self.svg=[]; self.records=[]
    def line(self,x,y,x2,y2,color=LINE,width=0.8,dash=False):
        self.pdf.setStrokeColor(color); self.pdf.setLineWidth(width); self.pdf.setDash([4,3] if dash else [])
        self.pdf.line(x,H-y,x2,H-y2); self.pdf.setDash([])
        self.svg.append(f'<path d="M{x} {y} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="4 3"' if dash else '')+'/>')
    def rect(self,x,y,w,h,fill=PALE):
        self.pdf.setFillColor(fill); self.pdf.rect(x,H-y-h,w,h,fill=1,stroke=0)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')
    def text(self,x,y,t,size=11,bold=False,color=INK,anchor='start'):
        self.pdf.setFillColor(color); self.pdf.setFont('SpecBold' if bold else 'Spec',size)
        if anchor=='middle': self.pdf.drawCentredString(x,H-y,t)
        elif anchor=='end': self.pdf.drawRightString(x,H-y,t)
        else: self.pdf.drawString(x,H-y,t)
        self.svg.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" text-anchor="{anchor}">{escape(t)}</text>')
    def para(self,x,y,w,t,size=11,color=INK,bold=False):
        style=ParagraphStyle('p',fontName='SpecBold' if bold else 'Spec',fontSize=size,leading=size*1.43,textColor=color)
        p=Paragraph(escape(t),style); pw,ph=p.wrap(w,H)
        p.drawOn(self.pdf,x,H-y-ph)
        # Use Paragraph's own wrapping for identical SVG line breaks.
        for n,line in enumerate(p.blPara.lines):
            self.text_svg(x,y+size+n*size*1.43,' '.join(line[1]),size,bold,color)
        return ph
    def text_svg(self,x,y,t,size,bold=False,color=INK):
        self.svg.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(t)}</text>')
    def start(self,title,subtitle):
        self.page+=1; self.current=title
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="max-width:100%;height:auto"><title>{escape(self.title+" / "+title)}</title><rect width="{W}" height="{H}" fill="white"/>']
        self.rect(0,0,W,62,INK); self.text(36,27,self.title.upper()+' / TECHNICAL SPECIFICATION',16,True,'#ffffff')
        self.text(36,47,'Adesina Adebola / independent jewellery design study',10,False,'#ffffff')
        self.text(W-36,27,f'{self.code} / {self.rev}',11,True,'#ffffff','end')
        self.text(W-36,47,f'SHEET {self.page:02d} / 08',10,False,'#ffffff','end')
        self.text(36,104,title,25,True); self.para(36,119,1118,subtitle,11,MUTED)
        self.records.append({'title':title,'subtitle':subtitle,'tables':[],'notes':[]})
    def table(self,x,y,width,headers,rows,ratios=None,size=11):
        ratios=ratios or [1/len(headers)]*len(headers); widths=[width*r for r in ratios]
        self.rect(x,y,width,30,INK); xx=x
        for col,w in zip(headers,widths): self.text(xx+10,y+20,col,size,True,'#ffffff'); xx+=w
        yy=y+30
        for n,row in enumerate(rows):
            hs=[]
            for t,w in zip(row,widths):
                style=ParagraphStyle('m',fontName='Spec',fontSize=size,leading=size*1.43)
                p=Paragraph(escape(str(t)),style); hs.append(p.wrap(w-20,H)[1])
            height=max(hs)+18
            if yy+height>770: raise ValueError(f'Overflow {self.slug} page {self.page}: {yy+height}')
            if n%2==0:self.rect(x,yy,width,height,PALE)
            xx=x
            for i,(t,w) in enumerate(zip(row,widths)):
                self.para(xx+10,yy+9,w-20,str(t),size,bold=(i==0)); xx+=w
            self.line(x,yy+height,x+width,yy+height); yy+=height
        self.records[-1]['tables'].append({'headers':headers,'rows':rows})
        return yy
    def note(self,x,y,w,t):
        self.para(x,y,w,t,11,MUTED); self.records[-1]['notes'].append(t)
    def image(self,path,x,y,w,h,tight=False,opacity=1,model_view=False):
        if not model_view and self.slug=='confluence' and path.stem in DATA[self.slug].get('vector_views',{}):
            return self.vector_view(path.stem,x,y,w,h,tight=tight)
        image=Image.open(path).convert('RGBA')
        if opacity<1:
            image.putalpha(image.getchannel('A').point(lambda value:round(value*opacity)))
        if tight and image.getchannel('A').getextrema()[0]<255:
            image=image.crop(image.getchannel('A').point(lambda v:255 if v>10 else 0).getbbox())
        iw,ih=image.size; scale=min(w/iw,h/ih); dw,dh=iw*scale,ih*scale; xx=x+(w-dw)/2; yy=y+(h-dh)/2
        buf=BytesIO(); image.save(buf,format='PNG'); raw=buf.getvalue()
        self.pdf.drawImage(ImageReader(BytesIO(raw)),xx,H-yy-dh,dw,dh,mask='auto')
        self.svg.append(f'<image x="{xx}" y="{yy}" width="{dw}" height="{dh}" href="data:image/png;base64,{base64.b64encode(raw).decode()}"/>')
        return xx,yy,dw,dh
    def vector_view(self,name,x,y,w,h,tight=False,color=INK,width=1.2,silhouette_only=False):
        view=DATA[self.slug]['vector_views'][name]
        segments=view['segments'];scale_width=view['ortho_scale']
        lo=[-scale_width/2,-scale_width*view['pixel_size'][1]/view['pixel_size'][0]/2]
        hi=[-lo[0],-lo[1]]
        if tight:
            points=[point for segment in segments for point in segment['points']]
            lo=[min(point[i] for point in points) for i in range(2)]
            hi=[max(point[i] for point in points) for i in range(2)]
        scale=min(w/(hi[0]-lo[0]),h/(hi[1]-lo[1]))
        dw=(hi[0]-lo[0])*scale;dh=(hi[1]-lo[1])*scale
        xx=x+(w-dw)/2;yy=y+(h-dh)/2
        for silhouette in [False,True]:
            if silhouette_only and not silhouette:continue
            pdfpath=self.pdf.beginPath();svgpath=[]
            for segment in segments:
                if segment['silhouette']!=silhouette:continue
                a,b=[(xx+(point[0]-lo[0])*scale,yy+(hi[1]-point[1])*scale) for point in segment['points']]
                pdfpath.moveTo(a[0],H-a[1]);pdfpath.lineTo(b[0],H-b[1])
                svgpath.append(f'M{a[0]:.3f} {a[1]:.3f}L{b[0]:.3f} {b[1]:.3f}')
            # Keep true visible contour/crease geometry legible when a full
            # sheet is fitted to a laptop or phone; previous .7/.49 pt strokes
            # became subpixel at the normal gallery display scale.
            stroke=round(width if silhouette else width*.75,3)
            self.pdf.setStrokeColor(color);self.pdf.setLineWidth(stroke);self.pdf.drawPath(pdfpath)
            self.svg.append(f'<path d="{" ".join(svgpath)}" fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round"/>')
        return xx,yy,dw,dh
    def arrow(self,x,y,dx,dy):
        pts=[(x,y),(x+dx*7-dy*2.5,y+dy*7+dx*2.5),(x+dx*7+dy*2.5,y+dy*7-dx*2.5)]
        p=self.pdf.beginPath();p.moveTo(pts[0][0],H-pts[0][1])
        for px,py in pts[1:]:p.lineTo(px,H-py)
        p.close(); self.pdf.setFillColor(ACCENT);self.pdf.drawPath(p,fill=1,stroke=0)
        self.svg.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in pts)+f'" fill="{ACCENT}"/>')
    def hdim(self,x1,x2,edge,y,label):
        for x in [x1,x2]:self.line(x,edge,x,y+6,ACCENT)
        self.line(x1,y,x2,y,ACCENT);self.arrow(x1,y,1,0);self.arrow(x2,y,-1,0)
        self.rect((x1+x2)/2-38,y-15,76,15,'white');self.text((x1+x2)/2,y-4,label,11,True,ACCENT,'middle')
    def vdim(self,y1,y2,edge,x,label):
        for y in [y1,y2]:self.line(edge,y,x+6,y,ACCENT)
        self.line(x,y1,x,y2,ACCENT);self.arrow(x,y1,0,1);self.arrow(x,y2,0,-1)
        self.text(x+8,(y1+y2)/2+4,label,11,True,ACCENT)
    def ortho(self,name,x,y,w,h,dim_labels=None):
        v=DATA[self.slug]['views'][name];self.image(self.out/'technical'/v['file'],x,y,w,h)
        if not dim_labels:return
        # Camera orthographic scale is horizontal width for the rendered image.
        scale=w/v['ortho_scale']; centre=v['centre']; rot=v['rotation_inverse']
        b=DATA[self.slug]['assembly']; corners=[]
        for a in [b['min'][0],b['max'][0]]:
            for c in [b['min'][1],b['max'][1]]:
                for d in [b['min'][2],b['max'][2]]:
                    delta=[a-centre[0],c-centre[1],d-centre[2]]
                    p=[sum(rot[i][j]*delta[j] for j in range(3)) for i in range(2)]
                    corners.append((x+w/2+p[0]*scale,y+h/2-p[1]*scale))
        lo=[min(p[i] for p in corners) for i in range(2)];hi=[max(p[i] for p in corners) for i in range(2)]
        if dim_labels[0]: self.hdim(lo[0],hi[0],hi[1],hi[1]+23,dim_labels[0])
        if dim_labels[1]: self.vdim(lo[1],hi[1],hi[0],hi[0]+18,dim_labels[1])
        return lo,hi
    def section(self,x,y,w,h):
        if self.slug=='confluence':
            # One visible front projection of the frozen refined mesh. A Y=0
            # cut misses the prong axes and cannot describe their full profile.
            data=DATA[self.slug];view=data['views']['front']
            points=[point for segment in data['vector_views']['front']['segments'] if segment['silhouette'] for point in segment['points']]
            lo=[min(point[i] for point in points) for i in range(2)]
            hi=[max(point[i] for point in points) for i in range(2)]
            scale=min(w/(hi[0]-lo[0]),h/(hi[1]-lo[1]))
            xx,yy,dw,dh=self.vector_view('front',x,y,w,h,tight=True,silhouette_only=True,width=1.2)
            self.svg[-1]=self.svg[-1].replace('<path ','<path id="front-elevation-contour" ',1)
            def project(world):
                delta=[world[i]-view['centre'][i] for i in range(3)]
                p=[sum(delta[i]*view['rotation_inverse'][j][i] for i in range(3)) for j in [0,1]]
                return xx+(p[0]-lo[0])*scale,yy+(hi[1]-p[1])*scale
            centre_x,bore_y=project([0,0,10.4])
            self.line(centre_x,yy-10,centre_x,yy+dh+10,MUTED,.6,True)
            left,_=project([-9,0,10.4]);right,_=project([9,0,10.4])
            self.hdim(left,right,bore_y,bore_y,'18.00 NOM.')
            self.text(x,y+h+30,'FRONT ELEVATION',11,True)
            self.text(x,y+h+45,'Pre-setting metal body.',9,False,MUTED)
            return
        data=DATA[self.slug]; axes=(0,2); segs=data['section_segments'];pts=[p for s in segs for p in s]
        lo=[min(p[a] for p in pts) for a in axes];hi=[max(p[a] for p in pts) for a in axes]
        scale=min(w/(hi[0]-lo[0]),h/(hi[1]-lo[1])); xx=x+(w-(hi[0]-lo[0])*scale)/2; yy=y+(h-(hi[1]-lo[1])*scale)/2
        project=lambda p:(xx+(p[0]-lo[0])*scale,yy+(hi[1]-p[2])*scale)
        # Batch section line segments in a single vector path.
        path=self.pdf.beginPath(); svg=[]
        for s in segs:
            a,b=map(project,s); path.moveTo(a[0],H-a[1]);path.lineTo(b[0],H-b[1]);svg.append(f'M{a[0]:.3f} {a[1]:.3f}L{b[0]:.3f} {b[1]:.3f}')
        self.pdf.setStrokeColor(INK);self.pdf.setLineWidth(.65);self.pdf.drawPath(path)
        self.svg.append(f'<path id="section-aa-cut" d="{" ".join(svg)}" fill="none" stroke="{INK}" stroke-width=".65"/>')
        centre_x=xx+(hi[0]-lo[0])*scale/2
        self.line(centre_x,yy-10,centre_x,yy+h+10,MUTED,.6,True)
        if self.slug=='confluence':
            bore_y=yy+(hi[1]-10.4)*scale
            self.hdim(xx+(-9-lo[0])*scale,xx+(9-lo[0])*scale,bore_y,bore_y,'18.00 NOM.')
        else:
            self.text(x,y+h+12,'Bore size: see measured sampling register',10,False,MUTED)
        if self.slug=='confluence':
            self.text(x,y+h+30,'SECTION A-A / metal contour at Y = 0',11,True)
            self.text(x,y+h+45,'Cut contours only; model views show the full setting.',9,False,MUTED)
        else:
            self.text(x,y+h+30,'SECTION A-A / metal contour at Y = 0',11,True)
    def leader(self,start,end,label,num):
        self.line(*start,*end,ACCENT,1); self.rect(end[0]-8,end[1]-9,17,17,INK)
        self.text(end[0],end[1]+3,str(num),10,True,'#ffffff','middle')
        self.text(end[0]+17,end[1]+4,label,11,True)
    def end(self,caption='Dimensions in mm / not to scale'):
        self.line(36,789,W-36,789)
        self.text(36,810,'02 OCT 2026 / '+caption,9,False,MUTED)
        self.text(W-36,810,f'{self.code} / {self.rev} / {self.page:02d}',10,True,INK,'end')
        self.svg.append('</svg>');fname=f'{self.page:02d}-'+self.current.lower().replace(' & ','-').replace(' / ','-').replace(' ','-')+'.svg'
        if self.page==8:fname='08-release-checklist-source-control.svg'
        (self.out/'technical'/fname).write_text(''.join(self.svg),encoding='utf-8')
        self.records[-1]['drawing']='technical/'+fname
        self.pdf.showPage()
    def finish(self):
        self.pdf.save();assert len(PdfReader(self.out/'technical-specification.pdf').pages)==8
        (self.out/'technical/specification-register.json').write_text(json.dumps(self.records,indent=2),encoding='utf-8')
        create_html(self)
        dest=ROOT/'output/pdf';dest.mkdir(parents=True,exist_ok=True)
        shutil.copy2(self.out/'technical-specification.pdf',dest/(self.slug+'-technical-specification.pdf'))
        if self.slug in ['confluence','iced-out-ring']:
            writer=PdfWriter();writer.add_page(PdfReader(self.out/'technical-specification.pdf').pages[1])
            writer.write(str(self.out/'dimensions.pdf'))
            shutil.copy2(self.out/'technical/02-assembly-dimensions.svg',self.out/'dimensions.svg')
            doc=pdfium.PdfDocument(str(self.out/'dimensions.pdf'));pic=doc[0].render(scale=1.6).to_pil()
            pic.save(self.out/'dimensions-01.png');pic.thumbnail((1800,1800));pic.convert('RGB').save(self.out/'dimensions-01.webp',quality=95);doc.close()
        if self.slug=='confluence':
            for name in ['wireframe-01','wireframe-02']:
                shutil.copy2(self.out/'technical'/(name+'.png'),self.out/(name+'.png'))
                im=Image.open(self.out/(name+'.png')).convert('RGBA')
                bg=Image.new('RGBA',im.size,'#f1f4f4');bg.alpha_composite(im);bg.convert('RGB').save(self.out/(name+'.webp'),quality=95)

def create_html(p):
    summary=p.records[0]['tables'][0]
    table=lambda t:'<div class="table-scroll" tabindex="0"><table><thead><tr>'+''.join('<th scope="col">'+escape(x)+'</th>' for x in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join(('<th scope="row">' if i==0 else '<td>')+escape(str(v))+('</th>' if i==0 else '</td>') for i,v in enumerate(row))+'</tr>' for row in t['rows'])+'</tbody></table></div>'
    sections=[]
    for i,r in enumerate(p.records):
        drawing=r['drawing']
        # Fast display files are derived from the same SVGs by
        # build-confluence-previews.mjs. Every original SVG anchor stays
        # unchanged; a missing preview after regeneration falls back to it.
        preview='technical/previews/'+Path(drawing).stem+'.webp' if p.slug=='confluence' else drawing
        fallback=f' onerror="this.onerror=null;this.src=\'{escape(drawing)}\'"' if p.slug=='confluence' else ''
        sections.append(f'<section id="sheet-{i+1}"><div class="section-heading"><h2>{i+1:02d} / {escape(r["title"])}</h2><a href="{drawing}" aria-haspopup="dialog">View sheet ⤢</a></div><p>{escape(r["subtitle"])}</p>'+('<a class="sheet" href="'+drawing+'" aria-haspopup="dialog"><img src="'+preview+'"'+fallback+' alt="'+escape(r['title']+' - dimensioned 3D model views and specification')+'" width="1190" height="842" loading="lazy"></a>' if i<3 else '')+''.join(table(t) for t in r['tables'])+''.join('<p class="note">'+escape(n)+'</p>' for n in r['notes'])+'</section>')
    doc=f'''<!doctype html><html lang="en"><head><link rel="icon" type="image/svg+xml" href="/favicon.svg"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(p.title)} - technical specification | Adesina Adebola</title><link rel="stylesheet" href="../ring-specification.css"><link rel="stylesheet" href="/image-viewer.css"><script src="/image-viewer.js" defer></script></head><body><header class="top"><a href="/jewellery/{p.slug}">← Back to {escape(p.title)}</a><a class="download" href="technical-specification.pdf" download>Download PDF ↓</a></header><main><div class="heading"><p>ADESINA ADEBOLA / INDEPENDENT DESIGN STUDY</p><h1>{escape(p.title)}</h1><p>Technical specification / {p.code} / {p.rev} / 02 October 2026</p><p class="status">Supplier review - not released for production</p></div><nav class="contents" aria-label="Specification sections">{''.join(f'<a href="#sheet-{i+1}">{i+1:02d} / {escape(r["title"])}</a>' for i,r in enumerate(p.records))}</nav>{''.join(sections)}<footer>Model dimensions = measurements from the 3D mesh. Proposed = design target. TBC = to be confirmed.</footer></main></body></html>'''
    (p.out/'specification.html').write_text(doc,encoding='utf-8')

def build(slug):
    con=slug=='confluence';title='Confluence' if con else 'Iced-out ring';code='CF-R01' if con else 'IO-R01'
    p=Pack(slug,title,code,'SPEC C' if con else 'SPEC A');d=DATA[slug]
    if con:
        shape=d['assembly']['size'];w,h,depth=shape[0],shape[2],shape[1]
    p.start('Design & specification overview','Design specification and proposed material schedule for first-sample review.')
    # The overview needs the shaded frozen body to make the open stock
    # settings clear. Keep the dimensioned orthographic sheets as vectors.
    p.image(p.out/'technical/isometric.png',36,166,515,480,tight=True,model_view=con)
    if con:p.text(36,668,'SOLID MODEL VIEW / PRE-SETTING METAL BODY',11,True)
    p.text(36,683,'PROPOSED MATERIAL ROUTE',11,True,ACCENT)
    p.note(36,697,490,'925 sterling silver, 18K yellow-gold electroplate at a 3.5 µm target, and round brilliant-cut moissanite. Proposed material route; sample approval required.')
    rows=[['Item / type',code+' / '+('bypass three-stone ring' if con else 'four-row full-eternity band'),'Defined'],
      ['Overall model body',(f'{w:.2f} W × {h:.2f} H × {depth:.2f} D' if con else '22.02 W × 22.02 H × 4.14 D'),'Model measured'],
      ['Ring bore',('18.00 nominal; sampled bore 18.012-18.020' if con else f'{d["bore_samples"]["minimum_sampled_clear_bore"]:.2f} minimum sampled; ring size TBC'),'Nominal / sampled'],
      ['Stone schedule',('1 × Ø5.00 + 2 × Ø2.50; 3 total' if con else 'Size, quantity and row allocation TBC'),('Nominal model' if con else 'TBC')],
      ['Metal / plating','925 silver / 18K gold; 3.5 µm target','Proposed'],
      ['Stone type / cut','Colourless moissanite / round brilliant','Proposed'],
      ['Findings',('12 stock prongs; integrated settings' if con else 'Integrated settings'),'Model / fit TBC'],
      ['Finish','High polish, rounded edges and prong tips','Proposed'],
      ['Target unit cost / MOQ','TBC / supplier quotation required','Open'],
      ['Release status','Digital study; physical sample approval pending','Not released']]
    p.table(586,166,568,['Field','Specification','Basis'],rows,[.26,.52,.22],10.5)
    p.end()

    p.start('Assembly dimensions','Orthographic dimensions of the pre-setting metal body. All stated dimensions are in millimetres.')
    if con:
        p.text(73,169,'FRONT / X-Z',11,True);p.ortho('front',55,182,350,311,[f'{w:.2f}',f'{h:.2f}'])
        p.text(500,169,'SIDE / Y-Z',11,True);p.ortho('side',455,182,240,213,[f'{depth:.2f}',None])
        p.text(815,169,'TOP / X-Y',11,True);p.ortho('top',785,182,330,293,[f'{w:.2f}',f'{depth:.2f}'])
        rows=[['D01','Model body W × H × D',f'{w:.2f} × {h:.2f} × {depth:.2f}','Pre-setting metal body'],['D02','Finished assembly envelope','21.42 × 23.28 × 6.00','Reference dimensions including stones'],['D03','Prong stock / count','Centre Ø0.95 / sides Ø0.80; 12 total','Curved centre stems; ~0.62 mm straight ends'],['D04','Bore / lower shank','18.00 nominal / 2.50 wide / 1.70 radial','Nominal bore; sampled shank dimensions']]
    else:
        p.text(66,169,'FRONT / X-Z',11,True);p.ortho('front',48,180,425,378,['22.02','22.02'])
        p.text(590,169,'TOP / X-Y',11,True);p.ortho('top',590,170,455,404,['22.02','4.14'])
        bore=d['bore_samples']['minimum_sampled_clear_bore']
        rows=[['D01','Model body W × H × D','22.02 × 22.02 × 4.14','Model units interpreted as mm; calibration TBC'],['D02','Model axes X × Y × Z','22.02 × 4.14 × 22.02','Ring axis along Y'],['D03','Stone schedule','Size, quantity and row allocation TBC','Specify purchased stones before seat cutting'],['D04','Minimum sampled bore',f'{bore:.2f}','Radial section samples; nominal ring size TBC']]
    p.table(36,590,1118,['ID','Feature','Value (mm)','Basis'],rows,[.07,.28,.30,.35],11)
    p.end()

    p.start('Construction & stone setting','Pre-setting construction, prong geometry and stone schedule.')
    p.section(47,177,350,365)
    p.image(p.out/'technical/exploded.png',450,169,354,350,tight=True,model_view=con)
    p.text(466,546,'PRE-SETTING BODY',11,True)
    p.image(p.out/'technical/setting-detail.png',841,172,302,320,tight=True,model_view=con)
    p.text(847,526,'SETTING DETAIL',11,True)
    if con:
        p.note(455,552,688,'Twelve stock prongs: four centre and eight side. Curved centre stems terminate in approximately 0.62 mm of straight stock for seat cutting and closing.')
        rows=[['S01','Centre stone / 1','Ø5.00 × 2.70 reference profile','Purchased-stone profile TBC'],['S02','Side stones / 2','Ø2.50 × 1.35 reference profiles','Purchased-stone profiles TBC'],['P01','Stock prongs / 12','Centre Ø0.95; sides Ø0.80 nominal','Final bearing geometry to suit purchased stones'],['G01','Gallery / lower shank','Gallery samples 0.63 / 0.55; shank 2.50 × 1.70','Sampled model values; finished minimums TBC']]
    else:
        rows=[['B01','Metal body / 1','22.02 W × 22.02 H × 4.14 D','Model dimensions; unit calibration TBC'],['G01','Galleries','Open passages below the settings','Finished wall thickness and polish access TBC'],['P01','Setting network','Integrated prongs and bearing features','Stock allowance and purchased-stone fit TBC'],['S01','Stones','Round brilliant moissanite proposed','Quantity, sizes and row allocation TBC']]
    p.table(36,610,1118,['ID','Part / quantity','Nominal geometry (mm)','Setting basis'],rows,[.07,.22,.32,.39],10)
    p.end('mm / '+('front elevation / pre-setting body' if con else 'section A-A at Y = 0 / pre-setting body')+' / not to scale')

    p.start('Materials, finish & bill of materials','Proposed alloy, stone, coating and surface specifications.')
    rows=[['M01 / body','925 sterling silver; one-piece investment casting','Proposed. Supplier alloy certificate and casting suitability required.'],
      ['M02 / gold layer','18K yellow-gold electroplate; 3.5 µm target','Proposed. Supplier to declare actual stack, process, local minimum and measurement uncertainty.'],
      ['M03 / underlayer','Composition and thickness TBC','Declare barrier/strike layers; no unapproved substitution. Confirm skin-contact requirements for destination market.'],
      ['S01 / stones',('1 × Ø5.00 round brilliant moissanite' if con else 'Round brilliant moissanite; size and quantity TBC'),'Proposed material; colourless matched lot. Grade, treatment, origin and profile TBC.'],
      ['S02 / stone matching',('2 × Ø2.50 round brilliant moissanite' if con else 'Row allocation and purchased-stone schedule TBC'),'Proposed material. Measure girdle, total depth, pavilion and diameter range before seats.'],
      ['F01 / findings','Integrated cast settings','Any solder/weld filler requires process approval.'],
      ['Finish / polish','High polish on exposed metal; rounded prong tips and contact edges','Maintain gallery access and local section sizes. Finish sample becomes visual master.'],
      ['Marking / packaging','Maker/material mark and location TBC; individually protected','Verify alloy before marking; include packaging in the quotation.']]
    y=p.table(36,165,1118,['BOM / field','Specification','Acceptance / status'],rows,[.20,.35,.45],11)
    p.text(36,y+32,'MATERIAL CHANGE CONTROL',12,True,ACCENT)
    p.note(36,y+45,1118,('Alternative route: solid 18K yellow gold, without plating; quote separately. ' if con else '')+'Material substitutions require review of casting, setting and finishing requirements.')
    p.end()

    p.start('Manufacturing route & tolerances','Proposed manufacturing stages and first-sample acceptance targets.')
    rows=[['1 / freeze','Confirm alloy, stone purchase profiles, ring size and source units','Designer + supplier; required before tooling'],
      ['2 / pattern','Approve a watertight casting master with seat and prong stock matched to purchased stones','Supplier to choose compensated scale, resin, orientation, supports and sprues'],
      ['3 / cast / prefinish','Investment cast and prefinish inaccessible galleries','Confirm fill, porosity, distortion and remaining section; no blocked cleaning access'],
      ['4 / stone set','Measure purchased stones; cut/finish bearings; set and close prongs','No glue as a substitute for mechanical retention; verify every seat'],
      ['5 / finish / plate','Final polish and coating sequence agreed with stone/chemistry compatibility','Supplier to document sequence and protect stones; no unapproved coating stack'],
      ['T01 / bore','Approved finished bore target ±0.05 mm',('Proposed; confirm the 18.00 mm nominal finished target.' if con else 'Proposed; nominal finished bore TBC.')+' Gauge at multiple angles and axial positions.'],
      ['T02 / overall envelope','Approved finished overall envelope ±0.10 mm','Proposed; finish allowance/stone height may require revised nominal.'],
      ['T03 / stone placement','Stone centre positions ±0.05 mm from approved setting master','Proposed; actual stone grading and setter capability must be checked.'],
      ['T04 / sections / seats','Minimum finished wall, gallery and prong thickness: TBC','Set by alloy, casting process and seat geometry.'],
      ['T05 / plating','3.5 µm target; local minimum/upper limit TBC after process trial','Proposed. Calibrated XRF method and measurement sites must be agreed.']]
    p.table(36,165,1118,['Stage / control','Requirement','Verification / responsibility'],rows,[.18,.40,.42],10.5)
    p.note(36,738,1118,'Tolerances apply only after a signed sample master exists. Do not shrink or enlarge the production file by an assumed universal percentage. Record tool compensation separately from design dimensions.')
    p.end()

    p.start('Sample review & quality control','First-article inspection criteria and records.')
    rows=[['Q01 / identity','Alloy and stone identity match approved BOM','Supplier certificates + suitable material/stone verification; coating can affect surface readings.','Reject substitution'],
      ['Q02 / size','Bore and envelopes within agreed finished targets','Calibrated gauges; multiple orientations; record measured values and equipment.','Major'],
      ['Q03 / setting',('All 3 stones present' if con else 'Approved BOM stone count present')+'; level seating; no movement or chipped girdles','Inspect every stone under magnification; retention test method/load TBC with setter.','Critical if loose/missing'],
      ['Q04 / prongs','Rounded consistent tips; contour-matched bearings; sufficient metal','Inspect every bearing, stone contact and prong tip under magnification.','Major'],
      ['Q05 / surface','No burrs, sharp points, visible pits or blocked galleries','Visual master comparison and snag check.','Major / minor by zone'],
      ['Q06 / coating','Approved thickness, colour and coverage on significant surfaces','Calibrated local XRF check at outer shank, inner bore and accessible setting; sites agreed with supplier.','Major'],
      ['Q07 / durability','Retention, finish wear and skin-contact performance validated','Supplier to propose quantified wear, sweat and adhesion protocols, limits and reports before testing.','Release gate'],
      ['Q08 / stacking','No stone-to-metal rubbing; comfortable fit and removal','Wear trial with selected partner rings; photograph clearances and record actual sizes.','Release gate'],
      ['Q09 / packaging','No transit abrasion; correct item/size/material labelling','Sample pack and transit handling check; stones protected independently.','Major']]
    y=p.table(36,165,1118,['Check','Acceptance criterion','Method / record','Classification'],rows,[.15,.31,.39,.15],10.5)
    p.note(36,y+22,1118,'Defect log fields: sample ID, date, sheet/feature ID, measured result, photograph, severity, cause, correction owner, due date and recheck result. Reject critical faults; batch sampling plan and major/minor acceptance limits remain TBC.')
    p.end()

    p.start('Costing, MOQ & supplier quotation','Quotation requirements and proposed order tiers.')
    rows=[['Target unit cost','TBC in NGN per complete ring','Confirm the design budget and supplier quotation.'],
      ['MOQ / size split','TBC per design / finish / size','Supplier to state minimum order, per-size minimum and mixed-size allowance.'],
      ['Quote tiers','50 / 100 / 250 rings requested for comparison','Inquiry quantities only. Separate prototype quantity and cost.'],
      ['Tooling / mold / 3D modelling fees','TBC; currency and ownership stated','Separate one-time charges, tooling life, correction charges and repeat-order rights.'],
      ['Metal / stones / setting','TBC, each separated','Declare metal weight basis, stone unit costs, setting labour and material wastage.'],
      ['Polish / coating / QC / packing','TBC, each separated','Declare coating stack and thickness, test/report costs and packing inclusion.'],
      ['Lead time','TBC: Model approval, tooling, sample, correction, production','State calendar days and the approval/payment trigger for each stage.'],
      ['Freight / taxes / payment','TBC; Incoterm and destination required','State quote currency, validity, exchange-rate basis, deposit and balance terms.'],
      ['Defect / rework terms','TBC; written before purchase order','Agree critical defect response, remake/rework costs and claim period.'],
      ['Model metal volume',f'{d["metal"]["signed_volume_mm3"]:.2f} mm³','Supplier to confirm finished metal weight and process yield.']]
    y=p.table(36,165,1118,['Commercial field','Required value','Supplier response detail'],rows,[.22,.33,.45],10.5)
    p.note(36,y+25,1118,'Landed unit cost = metal + stones + setting + finish/coating + QC + packing + allocated tooling + freight/taxes. Record quote date and currency. Compare suppliers only after material, size, stone count, coating and quality requirements match.')
    p.end()

    p.start('Sample approval & release','Open specifications and first-sample approval requirements.')
    rows=[['Drawing revision',f'{code} / {p.rev}','Approve the casting master and finished dimensions before tooling.'],
      ['Metal body',(f'{w:.2f} W × {h:.2f} H × {depth:.2f} D mm' if con else '22.02 W × 22.02 H × 4.14 D mm'),'Confirm finished wall, gallery and prong thicknesses.'],
      ['Ring size / units',('18.00 mm nominal bore' if con else f'{bore:.2f} sampled clear bore; Model unit calibration TBC'),'Confirm nominal ring size and check the finished bore with calibrated gauges.'],
      ['Materials / stones','925 silver / 18K plate / moissanite proposed','Approve alloy, coating stack, stone grades, profiles and dimensional range.'],
      ['Sample status','First article TBC','Approve setting, finish, fit and inspection results.'],
      ['Stack / collection role',('Three-stone focal ring; trial beside a plain slender band' if con else 'Full-eternity statement band; trial with a plain spacer or worn alone'),'Confirm partner-ring clearance and fit in a wear trial.'],
      ['Size range / resizing',('Size range TBC; evaluate lower-shank resizing with supplier' if con else 'Separate sized masters; resizing a full-eternity band requires supplier assessment'),'Do not scale stone geometry uniformly; retain purchased stone sizes and reassess settings.'],
      ['Release approval','Designer: TBC / supplier: TBC / sample ID: TBC','Production release requires signed sample approval.']]
    y=p.table(36,165,1118,['Item','Specification / status','Approval requirement'],rows,[.18,.40,.42],10.5)
    p.text(36,y+32,'APPROVAL RECORD',12,True,ACCENT)
    p.table(36,y+46,1118,['Sample ID','Inspection date','Designer approval','Supplier approval'],[['TBC','TBC','TBC','TBC']],size=10.5)
    p.end('Sample approval pending / NOT RELEASED FOR PRODUCTION')
    p.finish()

selected=sys.argv[1:] or ['confluence','iced-out-ring']
assert all(slug in DATA for slug in selected)
for slug in selected:build(slug)
audit={'date':'2026-10-03','pdf_pages_per_ring':8,'source_models_preserved':True,'method':'Saved mesh orthographic views and real triangle/plane sections; measurements retained with provenance; proposed supplier targets explicitly labelled',
 'outputs':[s+'/technical-specification.pdf' for s in selected],
 'models':{s:{'source':d['source'],'sha256':d['source_sha256']} for s,d in DATA.items()}}
for s,d in DATA.items():assert hashlib.sha256(Path(d['source']).read_bytes()).hexdigest()==d['source_sha256']
(ROOT/'docs/ring-specification-build.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('BUILT 8-PAGE MODEL-LED SPECIFICATION PACKS:',', '.join(selected))
