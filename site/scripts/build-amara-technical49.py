"""Measured SVG drawing sheets from evaluated model geometry, masks and real sections."""
from pathlib import Path
from PIL import Image
import numpy as np
import json, math, html, hashlib

root=Path(__file__).resolve().parents[1]
source=Path(r'C:\Users\Master\Documents\itura\portfolio-revision\technical49')
out=root/'public/jewellery/amara-nest/technical49'
out.mkdir(parents=True,exist_ok=True)
data=json.loads((source/'measurements.json').read_text())
parts=data['parts'];post_axis=data['post_axis_xz']
def fmt(v):return f'{v:.2f}'

def simplify(points,epsilon):
    if len(points)<3:return points
    a,b=points[0],points[-1];dx,dy=b[0]-a[0],b[1]-a[1];den=math.hypot(dx,dy)
    dist=[abs(dy*(p[0]-a[0])-dx*(p[1]-a[1]))/den if den else math.dist(p,a) for p in points]
    i=max(range(len(dist)),key=dist.__getitem__)
    if dist[i]>epsilon:return simplify(points[:i+1],epsilon)[:-1]+simplify(points[i:],epsilon)
    return [a,b]

def trace(mask,projection):
    pad=np.pad(mask,1);adj={}
    for direction,other in enumerate([pad[:-2,1:-1],pad[1:-1,2:],pad[2:,1:-1],pad[1:-1,:-2]]):
        ys,xs=np.where(mask & ~other)
        for x,y in zip(xs.tolist(),ys.tolist()):
            a,b=[((x,y),(x+1,y)),((x+1,y),(x+1,y+1)),((x+1,y+1),(x,y+1)),((x,y+1),(x,y))][direction]
            adj.setdefault(a,[]).append(b)
    paths=[];cx,cy=projection['centre'];scale=projection['scale']
    while adj:
        start=next(iter(adj));a=start;line=[a]
        while a in adj:
            b=adj[a].pop()
            if not adj[a]:del adj[a]
            line.append(b);a=b
            if a==start:break
        if len(line)<30:continue
        pts=[(cx+(x-800)*scale/1600,cy-(y-800)*scale/1600) for x,y in line]
        mid=len(pts)//2;pts=simplify(pts[:mid+1],.0075)+simplify(pts[mid:],.0075)[1:]
        paths.append(pts)
    return paths

views={}
for projection_file in source.glob('*-projection.json'):
    projection=json.loads(projection_file.read_text());name=projection['name']
    rgba=np.array(Image.open(source/f'{name}-parts.png').convert('RGBA'))
    mask=rgba[:,:,3]>127
    levels=np.array([89,124,149,170,188,203,218,231],dtype=np.int16)
    ids=np.argmin(abs(rgba[:,:,0].astype(np.int16)[:,:,None]-levels),axis=-1)
    outlines=[]
    for i in range(len(levels)):
        region=mask & (ids==i)
        if region.sum()>100:outlines.extend(trace(region,projection))
    views[name]=(projection,outlines)

class Sheet:
    def __init__(self,number,title,scales):
        self.number=number;self.nodes=[];self.scales=scales
        self.rect(10,10,400,277,'border')
        self.text(16,23,'AMARA NEST / '+title,5,'title')
        self.text(16,31,'DIMENSIONS IN mm · BEFORE FINISHING',2.8,'small')
        self.line(10,36,410,36,'thin')
    def text(self,x,y,text,size=3,cls='',anchor='start'):
        self.nodes.append(f'<text x="{x:.4f}" y="{y:.4f}" font-size="{size}" class="{cls}" text-anchor="{anchor}">{html.escape(text)}</text>')
    def line(self,x,y,xx,yy,cls='dim',arrows=False):
        self.nodes.append(f'<path class="{cls}" d="M{x:.4f},{y:.4f}L{xx:.4f},{yy:.4f}"'+(' marker-start="url(#arrow-start)" marker-end="url(#arrow-end)"' if arrows else '')+'/>')
    def rect(self,x,y,w,h,cls):self.nodes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{cls}"/>')
    def view(self,name,x,y,scale):
        projection,outlines=views[name];cx,cy=projection['centre']
        def project(point):return (x+(point[0]-cx)*scale,y-(point[1]-cy)*scale)
        d=''.join('M'+'L'.join(f'{a:.4f},{b:.4f}' for a,b in map(project,loop))+'Z' for loop in outlines)
        self.nodes.append(f'<path class="object" d="{d}"/>')
        d=''.join('M'+'L'.join(f'{a:.4f},{b:.4f}' for a,b in map(project,segment)) for segment in projection['features'])
        self.nodes.append(f'<path class="feature" d="{d}"/>')
        def point3(point):
            return project([sum(a*b for a,b in zip(point,projection['right'])),sum(a*b for a,b in zip(point,projection['up']))])
        return point3,project
    def hdim(self,a,b,y,label):
        x0,y0=a;x1,y1=b
        if x1<x0:x0,y0,x1,y1=x1,y1,x0,y0
        for x,origin in [(x0,y0),(x1,y1)]:
            sign=1 if y>origin else -1;self.line(x,origin+sign*.8,x,y+sign*2,'thin')
        self.line(x0,y,x1,y,arrows=True);self.text((x0+x1)/2,y-1.3,label,3,'dimension','middle')
    def vdim(self,a,b,x,label):
        x0,y0=a;x1,y1=b
        if y1<y0:x0,y0,x1,y1=x1,y1,x0,y0
        for y,origin in [(y0,x0),(y1,x1)]:
            sign=1 if x>origin else -1;self.line(origin+sign*.8,y,x+sign*2,y,'thin')
        self.line(x,y0,x,y1,arrows=True)
        mid=(y0+y1)/2
        self.nodes.append(f'<text class="dimension" font-size="3" text-anchor="middle" transform="translate({x-1.3},{mid}) rotate(-90)">{html.escape(label)}</text>')
    def leader(self,point,elbow,textpoint,label):
        self.line(*elbow,*point,'dim')
        self.nodes[-1]=self.nodes[-1][:-2]+' marker-end="url(#arrow-end)"/>'
        self.line(*elbow,*textpoint,'thin');self.text(textpoint[0],textpoint[1]-1.5,label,2.8)
    def center(self,x,y,r=5):
        self.line(x-r,y,x+r,y,'centre');self.line(x,y-r,x,y+r,'centre')
    def reference(self,x,y,label):
        self.rect(x-2.5,y-2.5,5,5,'thin');self.text(x,y+1.05,label,3,'title','middle')
    def section(self,section,right,up,x,y,scale):
        # Join actual plane/mesh intersections. Close only loops with coincident endpoints.
        adj={};coords={}
        for segment in section['segments']:
            points=[(sum(a*b for a,b in zip(p,right)),sum(a*b for a,b in zip(p,up))) for p in segment]
            a,b=[tuple(round(v,5) for v in p) for p in points]
            if a==b:continue
            coords[a]=points[0];coords[b]=points[1]
            adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
        ps=list(coords.values());cx=(min(p[0] for p in ps)+max(p[0] for p in ps))/2;cy=(min(p[1] for p in ps)+max(p[1] for p in ps))/2
        def project(p):return(x+(p[0]-cx)*scale,y-(p[1]-cy)*scale)
        loops=[]
        while adj:
            start=next(iter(adj));a=start;path=[a]
            while a in adj:
                b=adj[a].pop()
                if not adj[a]:del adj[a]
                if b in adj and a in adj[b]:
                    adj[b].remove(a)
                    if not adj[b]:del adj[b]
                path.append(b);a=b
                if a==start:break
            if len(path)>2:
                closed=path[0]==path[-1]
                if not closed:raise RuntimeError('Open CAD section boundary: '+str(section['plane_value']))
                loops.append('M'+'L'.join(f'{a:.4f},{b:.4f}' for a,b in map(project,[coords[k] for k in path]))+'Z')
        self.nodes.append('<path class="section" fill-rule="evenodd" d="'+''.join(loops)+'"/>')
        return project
    def finish(self,filename,notes):
        self.line(10,254,410,254,'thin')
        for i,note in enumerate(notes):self.text(16,261+i*5,note,2.7)
        self.rect(218,254,192,33,'thin')
        self.line(218,270,410,270,'thin');self.line(320,254,320,287,'thin')
        self.text(222,259,'DRAWING',2.2,'small');self.text(222,266,f'AN-49-{self.number:02d}',4,'title')
        self.text(324,259,'STATUS',2.2,'small');self.text(324,266,'MODEL DIMENSION STUDY',3,'title')
        self.text(222,275,'SCALE AT A3',2.2,'small');self.text(222,283,self.scales,3)
        self.text(324,275,'ADESINA ADEBOLA / mm',2.5);self.text(324,283,f'SHEET {self.number} / 3',3)
        defs='''<defs><marker id="arrow-end" markerWidth="2.5" markerHeight="1.8" refX="2.5" refY=".9" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0L2.5,.9L0,1.8Z" fill="#202020" stroke="none"/></marker><marker id="arrow-start" markerWidth="2.5" markerHeight="1.8" refX="0" refY=".9" orient="auto" markerUnits="userSpaceOnUse"><path d="M2.5,0L0,.9L2.5,1.8Z" fill="#202020" stroke="none"/></marker><pattern id="hatch" width="2" height="2" patternUnits="userSpaceOnUse"><path d="M-1,1L1,-1M0,2L2,0M1,3L3,1" stroke="#555" stroke-width=".13"/></pattern></defs>'''
        style='''<style>text{font-family:Arial,sans-serif;fill:#202020}.title{font-weight:700}.small{fill:#555}.object{stroke:#202020;stroke-width:.35;fill:none;stroke-linejoin:round}.feature{stroke:#333;stroke-width:.18;fill:none}.dim,.thin{stroke:#202020;stroke-width:.18;fill:none}.centre{stroke:#777;stroke-width:.15;stroke-dasharray:6 1.2 1.2 1.2;fill:none}.cut{stroke:#202020;stroke-width:.45;stroke-dasharray:7 1.2 1.2 1.2;fill:none}.section{stroke:#202020;stroke-width:.3;fill:url(#hatch);stroke-linejoin:round}.border{fill:none;stroke:#202020;stroke-width:.5}.dimension{paint-order:stroke;stroke:#fff;stroke-width:1.2;stroke-linejoin:round}</style>'''
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297" role="img" aria-labelledby="title desc"><title id="title">Amara Nest technical drawing {self.number}</title><desc id="desc">Measured model geometry, millimetres. {html.escape(filename)}</desc><rect width="420" height="297" fill="#fff"/>'+defs+style+''.join(self.nodes)+'</svg>'
        (out/filename).write_text(svg,encoding='utf-8')

shell=parts['shell'];boss=parts['boss'];post=parts['post'];seat=parts['seat'];stone=parts['stone']
head_min_y=shell['min'][1];A=boss['max'][1]
clear=post['max'][1]-A
shaft=data['post_sections'][2]['diameter_x']

s=Sheet(1,'ASSEMBLY DIMENSIONS','5:1 · rear 5:1')
front,_=s.view('assembly-front',74,178,5)
side,_=s.view('assembly-side',192,178,5)
top,_=s.view('assembly-top',74,85,5)
rear,_=s.view('assembly-rear',334,178,5)
s.text(74,140,'FRONT',3,'title','middle');s.text(192,140,'RIGHT SIDE',3,'title','middle');s.text(74,42,'TOP',3,'title','middle');s.text(334,140,'REAR',3,'title','middle')
s.hdim(front([shell['min'][0],0,shell['min'][2]]),front([shell['max'][0],0,shell['min'][2]]),212,fmt(shell['size'][0]))
s.vdim(front([shell['min'][0],0,shell['min'][2]]),front([shell['min'][0],0,shell['max'][2]]),38,fmt(shell['size'][2]))
s.hdim(side([0,head_min_y,shell['min'][2]]),side([0,A,shell['min'][2]]),212,fmt(A-head_min_y)+' head incl. boss')
s.hdim(side([0,A,post_axis[1]]),side([0,post['max'][1],post_axis[1]]),226,fmt(clear)+' clear post')
s.hdim(side([0,head_min_y,shell['min'][2]]),side([0,post['max'][1],post_axis[1]]),240,'('+fmt(post['max'][1]-head_min_y)+') overall')
axis_side=side([post_axis[0],A,post_axis[1]]);end_side=side([post_axis[0],post['max'][1],post_axis[1]])
s.line(axis_side[0]-8,axis_side[1],end_side[0]+5,end_side[1],'centre')
center=rear([post_axis[0],0,post_axis[1]]);s.center(*center,8)
s.leader(rear([post_axis[0]+boss['size'][0]/2,0,post_axis[1]]),(370,154),(381,154),'⌀'+fmt(boss['size'][0])+' boss')
prong=parts['upper_right'];point=front([(prong['min'][0]+prong['max'][0])/2,0,prong['max'][2]])
s.leader(point,(103,147),(112,147),'3× ⌀0.87 tip envelope')
s.text(150,50,'Third-angle arrangement:',2.7);s.text(150,55,'top above front, right side to its right.',2.7)
s.text(150,65,'Rear view shown separately.',2.7)
s.finish('01-assembly.svg',['One stud shown. Dimensions in mm, before finishing.','Dimensions in parentheses are reference dimensions.','Sample review: tolerances and finishing allowances to be agreed.'])

s=Sheet(2,'POST LOCATION & HEART SHELL','10:1 · shell / section 7.5:1')
rear,_=s.view('assembly-rear',82,100,10)
post_view,_=s.view('post-side',289,91,10)
shell_view,_=s.view('shell-side',70,208,7.5)
s.text(82,45,'REAR / POST POSITION',3,'title','middle');s.text(289,45,'POST & ATTACHMENT BOSS',3,'title','middle')
post_xy=rear([post_axis[0],0,post_axis[1]])
Bxy=rear([shell['min'][0],0,shell['min'][2]])
Cxy=rear([post_axis[0],0,shell['min'][2]])
s.center(*post_xy,12)
s.hdim(Cxy,Bxy,159,fmt(data['post_offset_from_shell_left'])+' from B')
s.vdim(Cxy,post_xy,146,fmt(data['post_height_from_shell_bottom'])+' from C')
s.reference(Bxy[0]+8,Bxy[1],'B');s.reference(Cxy[0],Cxy[1]+8,'C')
s.line(post_xy[0],52,post_xy[0],151,'cut')
for yy in [52,151]:
    s.line(post_xy[0]-3,yy,post_xy[0]+5,yy,'dim',True)
    s.nodes[-1]=s.nodes[-1].replace(' marker-start="url(#arrow-start)"','')
    s.text(post_xy[0]+6,yy+1,'S',3,'title')
pxA,py=post_view([post_axis[0],A,post_axis[1]])
pstart=post_view([post_axis[0],post['min'][1],post_axis[1]])
pend=post_view([post_axis[0],post['max'][1],post_axis[1]])
s.line(pstart[0]-9,py,pend[0]+6,py,'centre')
s.hdim((pxA,py+4),pend,119,fmt(clear)+' clear from A')
s.hdim(pstart,pend,63,'('+fmt(post['size'][1])+') component length')
s.reference(pxA,py+17,'A');s.line(pxA,py+10.5,pxA,py+14.5,'thin')
shaftpoint=post_view([post_axis[0],data['post_sections'][2]['plane_value'],post_axis[1]-shaft/2])
s.leader(shaftpoint,(289,135),(307,135),'⌀'+fmt(shaft)+' shaft')
collarpoint=post_view([post_axis[0],post['min'][1],post_axis[1]+post['size'][2]/2])
s.leader(collarpoint,(241,74),(253,74),'⌀'+fmt(post['size'][2])+' base collar')
s.text(200,151,'A = rear plane of the attachment boss.',2.8)
s.text(200,156,'B = left edge of shell in the front view.',2.8)
s.text(200,161,'C = lowest point of the shell.',2.8)
s.text(70,170,'SHELL ALONE / RIGHT SIDE',3,'title','middle')
s.hdim(shell_view([0,shell['min'][1],shell['min'][2]]),shell_view([0,shell['max'][1],shell['min'][2]]),250,fmt(shell['size'][1])+' shell only')
section=data['shell_section_at_post_x']
section_view=s.section(section,[0,1,0],[0,0,1],207,215,7.5)
s.text(207,175,'SECTION S–S / THROUGH POST AXIS',3,'title','middle')
z=data['seat_section_midheight']['plane_value'];ys=[]
for a,b in section['segments']:
    if min(a[2],b[2])<z<max(a[2],b[2]):ys.append(a[1]+(b[1]-a[1])*(z-a[2])/(b[2]-a[2]))
ys=sorted(set(round(v,6) for v in ys))
wall=ys[-1]-ys[-2]
q0,q1=section_view([ys[-2],z]),section_view([ys[-1],z])
s.leader(((q0[0]+q1[0])/2,q0[1]),(238,207),(250,207),fmt(wall)+' local back wall')
s.line(q0[0]-8,q0[1],q1[0]+5,q1[1],'centre')
s.text(253,215,fmt(z-shell['min'][2])+' above C',2.7);s.text(253,220,'Wall thickness at this point only.',2.7)
s.finish('02-post-shell.svg',['Post position is measured from shell outline references B and C.','S–S passes through the post centreline.','0.81 is the local back-wall thickness at the indicated height.'])

s=Sheet(3,'SEAT & CZ GEOMETRY','10:1 · all views / section')
sf,_=s.view('seat-front',73,99,10);ss,_=s.view('seat-side',207,99,10);st,_=s.view('seat-top',73,213,10)
gf,_=s.view('stone-front',343,99,10);gs,_=s.view('stone-side',343,213,10)
for x,label in [(73,'SEAT / FRONT'),(207,'SEAT / RIGHT SIDE'),(343,'CZ / FRONT')]:s.text(x,45,label,3,'title','middle')
s.hdim(sf([seat['min'][0],0,seat['min'][2]]),sf([seat['max'][0],0,seat['min'][2]]),143,fmt(seat['size'][0]))
s.vdim(sf([seat['min'][0],0,seat['min'][2]]),sf([seat['min'][0],0,seat['max'][2]]),28,fmt(seat['size'][2]))
s.hdim(ss([0,seat['min'][1],seat['max'][2]]),ss([0,seat['max'][1],seat['max'][2]]),58,fmt(seat['size'][1])+' depth')
s.hdim(gf([stone['min'][0],0,stone['min'][2]]),gf([stone['max'][0],0,stone['min'][2]]),141,fmt(stone['size'][0]))
s.vdim(gf([stone['max'][0],0,stone['min'][2]]),gf([stone['max'][0],0,stone['max'][2]]),388,fmt(stone['size'][2]))
for x,label in [(73,'SEAT / TOP'),(207,'SECTION T–T'),(343,'CZ / RIGHT SIDE')]:s.text(x,172,label,3,'title','middle')
s.hdim(st([seat['min'][0],seat['min'][1],0]),st([seat['max'][0],seat['min'][1],0]),245,fmt(seat['size'][0]))
mid=data['seat_section_midheight'];midview=s.section(mid,[1,0,0],[0,1,0],207,213,10)
sy=data['seat_sections_y'][1]['plane_value'];cross=[]
for a,b in mid['segments']:
    if min(a[1],b[1])<sy<max(a[1],b[1]):cross.append(a[0]+(b[0]-a[0])*(sy-a[1])/(b[1]-a[1]))
cross=sorted(set(round(v,6) for v in cross))
if len(cross)!=4:raise RuntimeError('Unexpected seat section crossing count')
opening=cross[2]-cross[1];left_span=cross[1]-cross[0];right_span=cross[3]-cross[2]
s.hdim(midview([cross[1],sy]),midview([cross[2],sy]),239,fmt(opening)+' opening at section line')
s.hdim(midview([cross[0],sy]),midview([cross[1],sy]),189,fmt(left_span))
s.hdim(midview([cross[2],sy]),midview([cross[3],sy]),189,fmt(right_span))
ll=midview([cross[0]-.3,sy]);rr=midview([cross[3]+.3,sy]);s.line(*ll,*rr,'centre')
s.text(207,248,'Widths measured at the mid-depth centreline.',2.5,'','middle')
cut_y=sf([0,0,z])[1]
s.line(34,cut_y,112,cut_y,'cut')
s.vdim(sf([seat['max'][0],0,seat['min'][2]]),sf([seat['max'][0],0,z]),125,fmt(z-seat['min'][2])+' to T–T')
for xx in [34,112]:
    s.line(xx,cut_y-3,xx,cut_y+5,'dim',True)
    s.nodes[-1]=s.nodes[-1].replace(' marker-start="url(#arrow-start)"','')
    s.text(xx+2,cut_y-3,'T',3,'title')
s.hdim(gs([0,stone['min'][1],stone['min'][2]]),gs([0,stone['max'][1],stone['min'][2]]),250,fmt(stone['size'][1])+' CZ depth')
s.finish('03-seat-cz.svg',['Seat width, height and depth include its end supports.','T–T shows local seat widths and opening, not stone-fit clearance.','CZ cut, seat contact and prong fit to be checked on a sample.'])

register=[['Post shaft diameter',fmt(shaft)+' mm'],['Post base collar diameter',fmt(post['size'][2])+' mm'],['Clear post from boss rear face A',fmt(clear)+' mm'],['Post centre from front-view left shell edge B',fmt(data['post_offset_from_shell_left'])+' mm'],['Post centre above lowest shell point C',fmt(data['post_height_from_shell_bottom'])+' mm'],['Shell alone: depth',fmt(shell['size'][1])+' mm'],['Seat: W × H × D',' × '.join(fmt(seat['size'][i]) for i in [0,2,1])+' mm'],['Local back wall at S–S, '+fmt(z-shell['min'][2])+' mm above C',fmt(wall)+' mm'],['Seat opening at T–T, measured at mid-depth',fmt(opening)+' mm']]
audit={'source':data['source'],'source_sha256':hashlib.sha256(Path(data['source']).read_bytes()).hexdigest(),'register':register,'shaft_diameter':shaft,'clear_post_length':clear,'shell_only_depth':shell['size'][1],'seat_dimensions_whd':[seat['size'][i] for i in [0,2,1]],'local_shell_wall':wall,'seat_section_opening':opening,'seat_section_spans':[left_span,right_span]}
(out/'dimension-register.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('BUILT_THREE_MEASURED_SVG_SHEETS',json.dumps(register),flush=True)
