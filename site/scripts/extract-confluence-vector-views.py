"""Extract visible silhouette and crease edges as true vector CAD linework."""
import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1]
register=root/'docs/ring-specification-cad-data.json'
all_data=json.loads(register.read_text());data=all_data['confluence']
source=Path(data['source']);before=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
obj=bpy.data.objects[data['source_object']];mesh=obj.data
points=[obj.matrix_world@v.co for v in mesh.vertices]
faces=[list(p.vertices) for p in mesh.polygons]
tree=BVHTree.FromPolygons(points,faces,epsilon=.000001)
edge_faces=[[] for _ in mesh.edges]
normals=[(obj.matrix_world.to_3x3().inverted().transposed()@p.normal).normalized() for p in mesh.polygons]
for polygon in mesh.polygons:
    for loop_index in polygon.loop_indices:edge_faces[mesh.loops[loop_index].edge_index].append(polygon.index)
vectors={}
for name in ['front','side','top','isometric','exploded','setting-detail']:
    view=data['views'][name];rot=view['rotation_inverse'];direction=Vector(rot[2]).normalized()
    centre=Vector(view['centre']);right=Vector(rot[0]);up=Vector(rot[1])
    candidates=[]
    for edge,adjacent in zip(mesh.edges,edge_faces):
        dots=[normals[i].dot(direction) for i in adjacent]
        silhouette=len(dots)<2 or min(dots)<=0<max(dots)
        sharp=len(adjacent)==2 and normals[adjacent[0]].dot(normals[adjacent[1]])<math.cos(math.radians(32))
        if silhouette or (sharp and max(dots)>0):candidates.append((edge,silhouette))
    segments=[];debug=[]
    def visible(point):
        hit,normal,index,distance=tree.ray_cast(point+direction*100,-direction,100.1)
        return hit is None or (hit-point).length<.025
    for edge,silhouette in candidates:
        a,b=[points[i] for i in edge.vertices]
        # Quarter-edge visibility samples suppress hidden rear outlines and
        # keep short visible portions where overlapping prongs meet.
        sample=[a.lerp(b,t) for t in [0,.25,.5,.75,1]]
        visibility=[visible(p) for p in sample]
        if name=='front' and len(debug)<8:
            p=sample[2];hit,normal,index,distance=tree.ray_cast(p+direction*100,-direction,100.1)
            debug.append({'point':list(p),'direction':list(direction),'distance':distance,'hit':list(hit) if hit else None,'visible':visibility,'faces':edge_faces[edge.index],'normals':[list(normals[i]) for i in edge_faces[edge.index]]})
        for i in range(4):
            if not(visibility[i] and visibility[i+1]):continue
            p,q=sample[i],sample[i+1]
            def project(v):
                delta=v-centre
                return [delta.dot(right),delta.dot(up)]
            segments.append({'points':[project(p),project(q)],'silhouette':silhouette})
    vectors[name]={'segments':segments,'ortho_scale':view['ortho_scale'],
        'pixel_size':view['pixel_size'],'candidate_edges':len(candidates)}
    print('VECTOR VIEW',name,'candidates',len(candidates),'visible segments',len(segments),flush=True)
    if debug:print('DEBUG FRONT',json.dumps(debug),flush=True)
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
data['vector_views']=vectors
register.write_text(json.dumps(all_data,indent=2),encoding='utf-8')
print('TRUE VECTOR LINEWORK EXTRACTED')
