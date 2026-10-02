"""Trace closed silhouettes of projected mesh faces and retain visible model detail."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, re, math
import numpy as np
from xml.etree import ElementTree as ET

root=Path(__file__).resolve().parents[1]
folder=root/'public/jewellery/amara-nest/sketches49'
projection_folder=Path(r'C:\Users\Master\Documents\itura\portfolio-revision\sketch-projections49')
ns={'s':'http://www.w3.org/2000/svg'}

def simplify(points, epsilon=.65):
    if len(points)<3:return points
    a,b=points[0],points[-1]
    dx,dy=b[0]-a[0],b[1]-a[1]
    den=math.hypot(dx,dy)
    ds=[abs(dy*(p[0]-a[0])-dx*(p[1]-a[1]))/den if den else math.dist(p,a) for p in points]
    i=max(range(len(ds)),key=ds.__getitem__)
    if ds[i]>epsilon:return simplify(points[:i+1],epsilon)[:-1]+simplify(points[i:],epsilon)
    return [a,b]

def trace_mask(mask):
    padded=np.pad(mask,1)
    adjacent={}
    for edge_kind,other in enumerate([padded[:-2,1:-1],padded[1:-1,2:],padded[2:,1:-1],padded[1:-1,:-2]]):
        ys,xs=np.where(mask & ~other)
        for x,y in zip(xs.tolist(),ys.tolist()):
            a,b=[((x,y),(x+1,y)),((x+1,y),(x+1,y+1)),((x+1,y+1),(x,y+1)),((x,y+1),(x,y))][edge_kind]
            adjacent.setdefault(a,[]).append(b)
    contours=[]
    while adjacent:
        start=next(iter(adjacent));a=start;line=[a]
        while a in adjacent:
            b=adjacent[a].pop()
            if not adjacent[a]:del adjacent[a]
            line.append(b);a=b
            if a==start:break
        if len(line)>30:
            points=[(x/2,y/2) for x,y in line]
            mid=len(points)//2
            points=simplify(points[:mid+1])+simplify(points[mid:])[1:]
            contours.append('M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in points)+'Z')
    return contours

panels=[]
for index,(file,label) in enumerate([('01-front','Front'),('03-profile','Side'),('04-rear','Back')]):
    rgba=np.array(Image.open(projection_folder/f'{file}-parts.png').convert('RGBA'))
    mask=rgba[:,:,3]>127
    levels=np.array([89,124,149,170,188,203,218,231],dtype=np.int16)
    part_ids=np.argmin(abs(rgba[:,:,0].astype(np.int16)[:,:,None]-levels),axis=-1)
    contours=[]
    for part_id in range(len(levels)):
        part_mask=mask & (part_ids==part_id)
        if part_mask.sum()>100:contours.extend(trace_mask(part_mask))
    # Visible feature edges from the ray-cast projection; avoid doubling the traced perimeter.
    svg=ET.parse(folder/f'{file}.svg').getroot()
    paths=svg.findall('s:path',ns)
    details=[]
    edge_data=paths[0].attrib['d']
    for x,y,xx,yy in re.findall(r'M([\d.-]+),([\d.-]+)L([\d.-]+),([\d.-]+)',edge_data):
        x,y,xx,yy=map(float,(x,y,xx,yy));mx,my=round(x+xx),round(y+yy)
        patch=mask[max(0,my-3):my+4,max(0,mx-3):mx+4]
        if patch.size and patch.all():details.append(f'M{x},{y}L{xx},{yy}')
    dimensions=''
    if index==0:
        dimensions=''.join(ET.tostring(p,encoding='unicode') for p in paths[1:])
        dimensions+=''.join(ET.tostring(t,encoding='unicode') for t in svg.findall('s:text',ns)[:2])
    elif index==1:
        py,px=np.where(mask)
        x0,x1,y=max(0,float(px.min())/2),float(px.max()+1)/2,float(py.max()+1)/2+32
        dimensions=f'<path class="dim" d="M{x0} {y}H{x1}M{x0} {y-8}V{y+8}M{x1} {y-8}V{y+8}"/><text x="{(x0+x1)/2}" y="{y+28}" text-anchor="middle">16.08 mm total depth</text>'
    panels.append(f'<g transform="translate({index*600},65) scale(.857)"><path d="'+''.join(contours)+'"/><path class="detail" d="'+''.join(details)+'"/>'+dimensions+'</g>'+f'<text class="label" x="{index*600+36}" y="44">{label}</text>')
doc='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 780" role="img" aria-labelledby="title desc"><title id="title">Amara Nest sketches</title><desc id="desc">Front, side and back. Closed silhouettes traced from the actual projected mesh, with visible model edges.</desc><style>path{fill:none;stroke:#25231f;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}.detail{stroke-width:1.2}.dim{stroke:#a17c4c}text{font:20px Arial;fill:#746b5e}.label{font:28px Georgia;fill:#25231f}</style><rect width="1800" height="780" fill="#f5f1ea"/>'+''.join(panels)+'<path d="M600 32V696M1200 32V696" style="stroke:#ddd5c8;stroke-width:1"/><text x="36" y="746" style="font-size:18px">AMARA NEST / MODEL-DERIVED SKETCHES</text></svg>'
(folder/'amara-sketches.svg').write_text(doc,encoding='utf-8')
# Raster proof from the same masks is generated separately by the browser SVG renderer.
print('BUILT_SINGLE_TRACED_SKETCH_SHEET')
