"""Read-only SVG projection of the supplied model. Never saves a Blender file."""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

out = Path(r'C:\Users\Master\Documents\portfolio\porfolio update\public\jewellery\amara-nest\sketches49')
out.mkdir(parents=True,exist_ok=True)
projection_out = Path(r'C:\Users\Master\Documents\itura\portfolio-revision\sketch-projections49')
projection_out.mkdir(parents=True,exist_ok=True)
keep = {'Amara - continuous rounded shell', 'CZ - heart 6.00 x 6.00 x 3.55 mm',
    'Cylinder', 'Cylinder.001', 'Cylinder.002',
    'Seat space - 0.50 mm rail envelope.001', '40 Cast attachment boss',
    '40 Post - provisional 0.80 x 10.50 mm.001'}
deps = bpy.context.evaluated_depsgraph_get()
objects=[]
for obj in bpy.data.objects:
    if obj.name not in keep or obj.hide_render: continue
    evaluated=obj.evaluated_get(deps); mesh=evaluated.to_mesh()
    mesh.calc_loop_triangles()
    verts=[evaluated.matrix_world @ v.co for v in mesh.vertices]
    faces=[tuple(p.vertices) for p in mesh.polygons]
    normal_matrix=evaluated.matrix_world.to_3x3().inverted().transposed()
    normals=[(normal_matrix @ p.normal).normalized() for p in mesh.polygons]
    edges={}
    for i,p in enumerate(mesh.polygons):
        for edge in p.edge_keys: edges.setdefault(tuple(sorted(edge)),[]).append(i)
    objects.append((obj.name,verts,faces,normals,edges))
    evaluated.to_mesh_clear()

for file,label,view,scale,post in [('01-front','Front',Vector((0,-1,0)),12.5,False),
    ('03-profile','Profile',Vector((1,0,0)),20,True),('04-rear','Reverse',Vector((0,1,0)),13.5,False)]:
    selected=objects
    allv=[]; allf=[]
    for name,verts,faces,normals,edges in selected:
        n=len(allv); allv.extend(verts); allf.extend(tuple(i+n for i in f) for f in faces)
    tree=BVHTree.FromPolygons(allv,allf)
    right=Vector((1,0,0)) if label=='Front' else (Vector((0,1,0)) if label=='Profile' else Vector((-1,0,0)))
    up=Vector((0,0,1)); center=Vector((-.53,6.2 if post else .8,4.5)); factor=550/scale
    paths=[]
    projected_faces=[]
    def project(p):
        delta=p-center
        return (350+delta.dot(right)*factor,320-delta.dot(up)*factor)
    for name,verts,faces,normals,edges in selected:
        projected_faces.extend([[project(verts[i]) for i in face] for face in faces])
        before=len(paths)
        for edge,adj in edges.items():
            front=[normals[i].dot(view)>0 for i in adj]
            silhouette=len(adj)==1 or (any(front) and not all(front))
            sharp=len(adj)==2 and any(front) and normals[adj[0]].dot(normals[adj[1]]) < math.cos(math.radians(12 if 'CZ -' in name else 38))
            if not silhouette and not sharp: continue
            a,b=(verts[i] for i in edge); mid=(a+b)/2
            hit,normal,index,distance=tree.ray_cast(mid+view*100,-view,101)
            if distance is not None and distance<99.94: continue
            x,y=project(a); xx,yy=project(b)
            if (x-xx)**2+(y-yy)**2<.02: continue
            paths.append(f'M{x:.2f},{y:.2f}L{xx:.2f},{yy:.2f}')
        print('PART',label,name,len(paths)-before,flush=True)
    measure=''
    if label=='Front':
        shell=next(o for o in selected if o[0]=='Amara - continuous rounded shell')[1]
        xs=[350+(p-center).dot(right)*factor for p in shell]; ys=[320-(p-center).dot(up)*factor for p in shell]
        x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
        measure=f'<path class="dim" d="M{x0:.1f} {y1+32:.1f}H{x1:.1f}M{x0:.1f} {y1+24:.1f}V{y1+40:.1f}M{x1:.1f} {y1+24:.1f}V{y1+40:.1f}M{x1+32:.1f} {y0:.1f}V{y1:.1f}M{x1+24:.1f} {y0:.1f}H{x1+40:.1f}M{x1+24:.1f} {y1:.1f}H{x1+40:.1f}"/><text x="{(x0+x1)/2:.1f}" y="{y1+58:.1f}" text-anchor="middle">9.04 mm</text><text x="{x1+54:.1f}" y="{(y0+y1)/2:.1f}" text-anchor="middle" transform="rotate(90 {x1+54:.1f} {(y0+y1)/2:.1f})">9.34 mm</text>'
    subtitle={'Front':'Heart proxy / 6.00 × 6.00 mm','Profile':'Head depth / 5.58 mm','Reverse':'Shell and attachment boss'}[label]
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 720" role="img" aria-labelledby="title desc"><title id="title">Amara Nest {label.lower()} line study</title><desc id="desc">Orthographic line study projected from the approved model geometry. Dimensions from the technical sheet.</desc><style>path{{fill:none;stroke:#25231f;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}.dim{{stroke:#a17c4c}}text{{font:20px Arial;fill:#746b5e}}</style><rect width="700" height="720" fill="#f5f1ea"/><path d="'+''.join(paths)+'"/>'+measure+f'<text x="40" y="675">{subtitle}</text><text x="40" y="700" style="font-size:11px;letter-spacing:1px">MODEL-DERIVED LINE STUDY</text></svg>'
    (out/f'{file}.svg').write_text(svg,encoding='utf-8')
    (projection_out/f'{file}-projection.json').write_text(json.dumps({'faces':projected_faces}),encoding='utf-8')
    print('EXPORTED',file,len(paths),'visible edge segments',flush=True)
