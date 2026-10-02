"""Refine only free centre-prong tips in a separate saved CAD revision."""
import bpy,bmesh,json,hashlib,math
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
source=root/'public/jewellery/confluence/technical/Confluence-Casting-Stock-CAD.blend'
before=hashlib.sha256(source.read_bytes()).hexdigest()
original=Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES\Confluence_First_Ring\Approved_Model\Confluence_Refined_Print.blend')
original_hash=hashlib.sha256(original.read_bytes()).hexdigest()
# Derive the axis of each original open stem from actual section intersections.
bpy.ops.wm.open_mainfile(filepath=str(original))
axes=[]
for i in range(4):
    obj=bpy.data.objects[f'Center casting prong {i+1}'];obj.data.calc_loop_triangles()
    points=[obj.matrix_world@v.co for v in obj.data.vertices]
    def centre(z):
        hits=[]
        for triangle in obj.data.loop_triangles:
            vs=[points[j] for j in triangle.vertices]
            for a,b in [(0,1),(1,2),(2,0)]:
                if (vs[a].z-z)*(vs[b].z-z)<0:
                    hits.append(vs[a].lerp(vs[b],(z-vs[a].z)/(vs[b].z-vs[a].z)))
        assert hits
        return Vector(tuple((min(p[k] for p in hits)+max(p[k] for p in hits))/2 for k in range(2)))
    a,b=centre(21.8),centre(22.25)
    axes.append({'quadrant':[1 if a.x>0 else -1,1 if a.y>0 else -1],
        'slope_xy':list((b-a)/.45),'centre_at_21_8':list(a)})
bpy.ops.wm.open_mainfile(filepath=str(source))
body=bpy.data.objects['Confluence - approved casting CAD body']
body.data=body.data.copy();body.name='Confluence - refined centre-prong CAD body'
changed=0;unchanged=0;max_move=0;by_quadrant={tuple(a['quadrant']):Vector(a['slope_xy']) for a in axes}
inverse=body.matrix_world.inverted();z0=21.75;transition=.4
for vertex in body.data.vertices:
    point=body.matrix_world@vertex.co
    if point.z<=z0 or abs(point.x)>2.45 or abs(point.y)>2.45:
        unchanged+=1;continue
    slope=by_quadrant[(1 if point.x>0 else -1,1 if point.y>0 else -1)]
    t=point.z-z0
    # Integrate a smoothstep derivative: preserve root tangent, then make
    # the final ~0.6 mm parallel to Z without a kink or a closed claw.
    u=min(t/transition,1)
    integral=transition*(u**3-.5*u**4) if t<transition else t-transition/2
    displacement=slope*integral
    revised=Vector((point.x-displacement.x,point.y-displacement.y,point.z))
    max_move=max(max_move,(revised-point).length)
    vertex.co=inverse@revised;changed+=1
body.data.update()
bm=bmesh.new();bm.from_mesh(body.data)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
audit={'boundary_edges':sum(e.is_boundary for e in bm.edges),
       'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'volume_mm3':bm.calc_volume(signed=True),
       'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces)}
assert audit['boundary_edges']==0 and audit['nonmanifold_edges']==0 and audit['volume_mm3']>0
bm.to_mesh(body.data);bm.free()
body['CAD purpose']='Centre stock stems retain their lower curvature; smooth transition to straight open tips. No seats cut, no stones.'
body['Manufacturing release']='CAD refinement only; purchased-stone fit and physical sample pending.'
scene=bpy.context.scene;scene.name='Confluence - refined curved stems and straight tips'
out=root/'public/jewellery/confluence/technical/Confluence-Refined-Centre-Prongs-CAD.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
assert hashlib.sha256(original.read_bytes()).hexdigest()==original_hash
(root/'docs/confluence-centre-prong-refinement.json').write_text(json.dumps({'source':str(source),
    'source_sha256':before,'original_source':str(original),'original_source_sha256':original_hash,
    'sources_preserved':True,'derived_model':str(out),'changed_vertices':changed,'unchanged_vertices':unchanged,
    'maximum_tip_translation_mm':max_move,'transition_start_z_mm':z0,'transition_end_z_mm':z0+transition,
    'straight_tip_length_mm':22.76827049255371-z0-transition,'original_stem_axes':axes,'audit':audit,
    'scope':'Free centre-prong ends only; roots, galleries, side prongs and band unchanged',
    'manufacturing_release':False},indent=2),encoding='utf-8')
print('REFINED CENTRE TIPS',changed,'vertices; maximum movement',max_move,'mm',audit)
