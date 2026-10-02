"""Self-contained model overview and labelled assembly sheets from saved CAD views."""
from pathlib import Path
from PIL import Image
import base64, html, json, runpy

root = Path(__file__).resolve().parents[1]
assets = root/'public/jewellery/amara-nest/model49'
source = Path(r'C:\Users\Master\Documents\itura\portfolio-revision\technical49')
# Reuse the geometry tracing used by the detailed drawings, including the true isometric projection.
cad = runpy.run_path(str(root/'scripts/build-amara-technical49.py'))
views = cad['views']

class Canvas:
    def __init__(self, width, height, title):
        self.w, self.h = width, height
        self.nodes = [f'<title>{html.escape(title)}</title><rect width="100%" height="100%" fill="#f5f1ea"/>']
    def text(self, x, y, value, size=28, bold=False):
        self.nodes.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{700 if bold else 400}">{html.escape(value)}</text>')
    def image(self, path, x, y, width, height):
        im = Image.open(path).convert('RGBA')
        bx, by, ex, ey = im.getchannel('A').getbbox()
        uri = 'data:image/'+('webp' if path.suffix == '.webp' else 'png')+';base64,'+base64.b64encode(path.read_bytes()).decode()
        self.nodes.append(f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="{bx} {by} {ex-bx} {ey-by}" overflow="hidden"><image width="{im.width}" height="{im.height}" href="{uri}"/></svg>')
        scale = min(width/(ex-bx), height/(ey-by))
        left = x+(width-(ex-bx)*scale)/2
        top = y+(height-(ey-by)*scale)/2
        return lambda px,py: (left+(px-bx)*scale, top+(py-by)*scale)
    def line(self, x, y, xx, yy):
        self.nodes.append(f'<path d="M{x},{y}L{xx},{yy}" stroke="#ae8559" stroke-width="1.5" fill="none"/>')
    def leader(self, x, y, label, point):
        self.text(x,y,label,30,True)
        self.line(x,y+14,*point)
        self.nodes.append(f'<circle cx="{point[0]}" cy="{point[1]}" r="4" fill="#ae8559"/>')
    def sketch(self, name, x, y, width, height):
        projection, outlines = views[name]
        features = projection['features']
        points = [p for loop in outlines for p in loop]
        xmin,xmax=min(p[0] for p in points),max(p[0] for p in points)
        ymin,ymax=min(p[1] for p in points),max(p[1] for p in points)
        scale=min(width/(xmax-xmin),height/(ymax-ymin))
        cx,cy=(xmin+xmax)/2,(ymin+ymax)/2
        def path(loops,close):
            return ''.join('M'+'L'.join(f'{x+width/2+(a-cx)*scale:.3f},{y+height/2-(b-cy)*scale:.3f}' for a,b in loop)+('Z' if close else '') for loop in loops)
        self.nodes.append(f'<path d="{path(outlines,True)}" fill="none" stroke="#25231f" stroke-width="2" stroke-linejoin="round"/>')
        self.nodes.append(f'<path d="{path(features,False)}" fill="none" stroke="#5e5951" stroke-width="1"/>')
        def point3(point):
            px=sum(a*b for a,b in zip(point,projection['right']))
            py=sum(a*b for a,b in zip(point,projection['up']))
            return x+width/2+(px-cx)*scale, y+height/2-(py-cy)*scale
        return point3
    def hdim(self, a, b, y, label):
        x1,y1=a; x2,y2=b
        for x,origin in [(x1,y1),(x2,y2)]:
            self.line(x,origin+5,x,y+10)
        self.nodes.append(f'<path d="M{x1},{y}H{x2}" class="dimension-line" marker-start="url(#dim-start)" marker-end="url(#dim-end)"/>')
        self.nodes.append(f'<text x="{(x1+x2)/2}" y="{y-15}" text-anchor="middle" font-size="34" class="dimension-text">{html.escape(label)}</text>')
    def vdim(self, a, b, x, label):
        x1,y1=a; x2,y2=b
        for origin,y in [(x1,y1),(x2,y2)]:
            self.line(origin-5,y,x-10,y)
        self.nodes.append(f'<path d="M{x},{min(y1,y2)}V{max(y1,y2)}" class="dimension-line" marker-start="url(#dim-start)" marker-end="url(#dim-end)"/>')
        self.nodes.append(f'<text transform="translate({x-22},{(y1+y2)/2}) rotate(-90)" text-anchor="middle" font-size="34" class="dimension-text">{html.escape(label)}</text>')
    def save(self, filename):
        defs='<defs><marker id="dim-start" markerWidth="10" markerHeight="8" refX="0" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M10,0L0,4L10,8Z" fill="#ae8559"/></marker><marker id="dim-end" markerWidth="10" markerHeight="8" refX="10" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0L10,4L0,8Z" fill="#ae8559"/></marker></defs>'
        (assets/filename).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img"><style>text{{font-family:Arial,sans-serif;fill:#25231f}}.dimension-line{{stroke:#ae8559;stroke-width:1.8;fill:none}}.dimension-text{{paint-order:stroke;stroke:#f5f1ea;stroke-width:6;stroke-linejoin:round}}</style>'+defs+''.join(self.nodes)+'</svg>',encoding='utf-8')

c=Canvas(1000,1400,'Amara Nest — model sketches')
c.text(48,67,'AMARA NEST',36,True)
c.text(48,110,'Model sketches · overall dimensions in mm',26)
c.line(48,138,952,138)
c.text(160,215,'Front',30,True)
c.text(540,215,'Side',30,True)
front=c.sketch('assembly-front',160,265,310,350)
side=c.sketch('assembly-side',540,265,410,350)
shell=cad['parts']['shell']; post=cad['parts']['post']
c.hdim(front([shell['min'][0],0,shell['min'][2]]),front([shell['max'][0],0,shell['min'][2]]),680,f"{shell['size'][0]:.2f} mm")
c.vdim(front([shell['min'][0],0,shell['min'][2]]),front([shell['min'][0],0,shell['max'][2]]),95,f"{shell['size'][2]:.2f} mm")
c.hdim(side([0,shell['min'][1],shell['min'][2]]),side([0,post['max'][1],cad['post_axis'][1]]),680,f"{post['max'][1]-shell['min'][1]:.2f} mm")
c.text(540,732,'Overall depth · including post',26)
c.text(280,815,'Isometric',30,True)
c.sketch('assembly-iso',280,855,540,430)
c.text(48,1370,'Dimensions before finishing.',26)
c.save('model-overview.svg')

c=Canvas(1400,820,'Amara Nest — labelled parts of the assembled model')
c.text(48,65,'Parts of the stud',38,True)
front=c.image(assets/'front-clay.webp',320,120,580,635)
side=c.image(assets/'side-clay.webp',925,175,420,320)
c.leader(48,210,'Outer shell',front(320,220))
c.leader(48,410,'Heart-cut CZ',front(645,480))
c.leader(48,650,'Lower prong',front(655,825))
c.leader(930,700,'Upper prongs',front(915,290))
c.leader(1090,130,'Post',side(750,423))
c.leader(1060,540,'Attachment boss',side(423,423))
c.save('parts-assembled.svg')

c=Canvas(1400,920,'Amara Nest — labelled exploded view of the CZ, seat and prongs')
c.text(48,65,'Stone and seat',38,True)
exploded=c.image(assets/'exploded-clay.webp',520,105,520,720)
c.leader(48,245,'Heart-cut CZ',exploded(575,270))
c.leader(48,545,'Stone seat',exploded(500,590))
c.leader(48,785,'Lower prong',exploded(580,874))
c.leader(1080,490,'Upper prongs',exploded(745,592))
c.text(48,882,'CZ lifted to show the seat and three prongs.',27)
c.save('parts-exploded.svg')
print('Built model overview and two labelled model sheets.')
