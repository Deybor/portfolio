"""Create a separate stone-free CAD revision with twelve truly straight prongs."""
import bpy,bmesh,json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES\Confluence_First_Ring\Approved_Model\Confluence_Refined_Print.blend')
sha=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
scene=bpy.data.scenes.new('Confluence - stone-free straight-prong CAD');bpy.context.window.scene=scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001
frame=bpy.data.objects['Audit frame — prongs excluded']
body=bpy.data.objects.new('Confluence - straight-prong CAD body',frame.data.copy())
body.matrix_world=frame.matrix_world.copy();scene.collection.objects.link(body)
prongs=[];parameters=[]
for name,cx,cy,radius,diameter,z0,z1 in [('Centre',0,0,2.63,.95,19.65,22.75),('Left',-3.9,-.4,1.38,.8,19.35,21.52),('Right',3.9,.4,1.38,.8,19.35,21.52)]:
    for i in range(4):
        angle=math.pi/4+i*math.pi/2;x=cx+radius*math.cos(angle);y=cy+radius*math.sin(angle)
        bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=diameter/2,depth=z1-z0,location=(x,y,(z0+z1)/2))
        o=bpy.context.object;o.name=f'{name} straight prong {i+1}'
        bevel=o.modifiers.new('Rounded stock edges','BEVEL');bevel.width=.06;bevel.segments=3
        bpy.ops.object.modifier_apply(modifier=bevel.name)
        bpy.context.view_layer.objects.active=body
        mod=body.modifiers.new('Fuse '+o.name,'BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=o
        bpy.ops.object.modifier_apply(modifier=mod.name)
        parameters.append({'name':o.name,'axis':'Z - straight','centre_xy_mm':[x,y],'diameter_mm':diameter,'z0_mm':z0,'z1_mm':z1})
        bpy.data.objects.remove(o,do_unlink=True)
bm=bmesh.new();bm.from_mesh(body.data)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.000001)
boundary=[e for e in bm.edges if e.is_boundary]
if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=3)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
assert not any(not e.is_manifold for e in bm.edges),'Derived CAD has unresolved nonmanifold edges'
bm.to_mesh(body.data);bm.free();body.data.update()
for p in body.data.polygons:p.use_smooth=True
body['CAD purpose']='User-requested stone-free view with straight prongs. Separate revision; no stone seats cut.'
body['Manufacturing release']='Pending geometry audit and supplier sample. Existing approved casting STL is a different geometry.'
scene['source_sha256']=sha
# Save only the new isolated scene and body, never the supplied model.
for s in list(bpy.data.scenes):
    if s!=scene:bpy.data.scenes.remove(s)
for o in list(bpy.data.objects):
    if o!=body:bpy.data.objects.remove(o,do_unlink=True)
out=ROOT/'public/jewellery/confluence/technical/Confluence-Straight-Prong-CAD.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
(ROOT/'docs/confluence-straight-prongs.json').write_text(json.dumps({'source':str(source),'source_sha256':sha,'source_preserved':True,'derived_model':str(out),'prongs':parameters,'stone_count':0,'approval_basis':'User requested diamonds removed and all prongs straight','manufacturing_release':False},indent=2),encoding='utf-8')
print('STRAIGHT_PRONG_CAD_COPY_SAVED')
