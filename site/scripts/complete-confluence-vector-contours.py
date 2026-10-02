"""Convert controlled CAD-view silhouettes into closed SVG contour paths.

Silhouette sampling is at the saved 1800px camera resolution, simplified by
at most 0.35px. No shaded image is embedded in the drawing.
"""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[1]
register=root/'docs/ring-specification-cad-data.json'
all_data=json.loads(register.read_text());data=all_data['confluence']
def simplify(points,tolerance=.35):
    if len(points)<3:return points
    a,b=np.array(points[0]),np.array(points[-1]);delta=b-a
    coords=np.array(points);length=float(delta@delta)
    if length:
        t=np.clip(((coords-a)@delta)/length,0,1)
        distances=np.linalg.norm(coords-a-t[:,None]*delta,axis=1)
    else:distances=np.linalg.norm(coords-a,axis=1)
    index=int(np.argmax(distances))
    if distances[index]<=tolerance:return [points[0],points[-1]]
    return simplify(points[:index+1],tolerance)[:-1]+simplify(points[index:],tolerance)
for name,view in data['vector_views'].items():
    image=Image.open(root/'public/jewellery/confluence/technical'/data['views'][name]['file']).convert('RGBA')
    mask=np.asarray(image)[:,:,3]>127;edges={}
    above=np.pad(mask[:-1,:],((1,0),(0,0)))
    below=np.pad(mask[1:,:],((0,1),(0,0)))
    left=np.pad(mask[:,:-1],((0,0),(1,0)))
    right=np.pad(mask[:,1:],((0,0),(0,1)))
    for y,x in np.argwhere(mask&~above):edges[(int(x),int(y))]=(int(x+1),int(y))
    for y,x in np.argwhere(mask&~right):edges[(int(x+1),int(y))]=(int(x+1),int(y+1))
    for y,x in np.argwhere(mask&~below):edges[(int(x+1),int(y+1))]=(int(x),int(y+1))
    for y,x in np.argwhere(mask&~left):edges[(int(x),int(y+1))]=(int(x),int(y))
    contours=[]
    while edges:
        start=next(iter(edges));point=start;loop=[start]
        while point in edges:
            point=edges.pop(point);loop.append(point)
            if point==start:break
        if len(loop)<12 or loop[-1]!=start:continue
        pivot=len(loop)//2
        simplified=simplify(loop[:pivot+1])[:-1]+simplify(loop[pivot:])
        contours.append(simplified)
    pixel_to_mm=view['ortho_scale']/image.width
    projected=[]
    for contour in contours:
        points=[[(x-image.width/2)*pixel_to_mm,(image.height/2-y)*pixel_to_mm] for x,y in contour]
        projected.extend({'points':[a,b],'silhouette':True} for a,b in zip(points,points[1:]))
    # Resolve visible rim/cavity boundaries from the same controlled CAD view.
    # These are encoded as paths, never as an embedded shaded bitmap.
    rgb=np.asarray(image)[:,:,:3].astype(float)
    grey=rgb.mean(axis=2);gx=np.zeros_like(grey);gy=np.zeros_like(grey)
    gx[:,1:-1]=(grey[:,2:]-grey[:,:-2])/2
    gy[1:-1,:]=(grey[2:,:]-grey[:-2,:])/2
    magnitude=np.hypot(gx,gy);angle=(np.degrees(np.arctan2(gy,gx))+180)%180
    inside=mask.copy()
    for dy,dx in [(0,-2),(0,2),(-2,0),(2,0),(-2,-2),(2,2),(-2,2),(2,-2)]:
        inside &= np.roll(mask,(dy,dx),(0,1))
    thin=np.zeros_like(mask)
    for direction,selection,offset in [
        (0,(angle<22.5)|(angle>=157.5),(0,1)),
        (1,(angle>=22.5)&(angle<67.5),(1,1)),
        (2,(angle>=67.5)&(angle<112.5),(1,0)),
        (3,(angle>=112.5)&(angle<157.5),(1,-1))]:
        thin |= selection & (magnitude>=np.roll(magnitude,offset,(0,1))) & (magnitude>np.roll(magnitude,(-offset[0],-offset[1]),(0,1)))
    pixels={tuple(map(int,point)) for point in np.argwhere(thin&inside&(magnitude>13))}
    neighbors={p:[(p[0]+dy,p[1]+dx) for dy in [-1,0,1] for dx in [-1,0,1]
        if (dy or dx) and (p[0]+dy,p[1]+dx) in pixels] for p in pixels}
    visited=set();detail_count=0
    for start in sorted(pixels,key=lambda p:len(neighbors[p])):
        for next_point in neighbors[start]:
            edge=tuple(sorted([start,next_point]))
            if edge in visited:continue
            path=[start,next_point];visited.add(edge);previous=start;current=next_point
            while len(neighbors[current])==2:
                following=next(p for p in neighbors[current] if p!=previous)
                edge=tuple(sorted([current,following]))
                if edge in visited:break
                visited.add(edge);path.append(following);previous,current=current,following
            if len(path)<14:continue
            line=simplify([(x,y) for y,x in path],.5)
            points=[[(x-image.width/2)*pixel_to_mm,(image.height/2-y)*pixel_to_mm] for x,y in line]
            projected.extend({'points':[a,b],'silhouette':False} for a,b in zip(points,points[1:]))
            detail_count+=1
    view['segments']=projected
    view['contour_method']='Closed silhouette and visible rim/cavity paths sampled from controlled CAD camera; 0.35px silhouette / 0.5px internal contour simplification; no raster embedded'
    view['silhouette_contours']=len(contours)
    print(name,'closed outlines',len(contours),'detail paths',detail_count,'vector segments',len(projected))
register.write_text(json.dumps(all_data,indent=2),encoding='utf-8')
