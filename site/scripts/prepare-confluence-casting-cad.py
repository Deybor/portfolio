"""Freeze the existing approved casting mesh for CAD views, without remodelling it."""
import bpy,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES\Confluence_First_Ring\Approved_Model\Confluence_Refined_Print.blend')
before=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
original=bpy.data.objects['Confluence casting pattern — uncut prong stock']
original_name=original.name
parameters=[]
for obj in bpy.data.objects:
    if 'casting prong' in obj.name:
        pts=[obj.matrix_world@v.co for v in obj.data.vertices]
        parameters.append({'name':obj.name,'bounds_mm':{'min':[min(p[i] for p in pts) for i in range(3)],'max':[max(p[i] for p in pts) for i in range(3)]}})
assert len(parameters)==12
scene=bpy.data.scenes.new('Confluence - original casting CAD');bpy.context.window.scene=scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001
body=bpy.data.objects.new('Confluence - approved casting CAD body',original.data.copy())
body.matrix_world=original.matrix_world.copy();scene.collection.objects.link(body)
assert len(body.data.vertices)==len(original.data.vertices)
assert all((a.co-b.co).length==0 for a,b in zip(body.data.vertices,original.data.vertices))
body['CAD purpose']='Original casting stock: open tips, flared centre stems, no gemstones. Finished fitted claws shown in beauty renders.'
body['Manufacturing release']='Physical supplier/sample validation remains pending.'
scene['source_sha256']=before
for old in list(bpy.data.scenes):
    if old!=scene:bpy.data.scenes.remove(old)
for obj in list(bpy.data.objects):
    if obj!=body:bpy.data.objects.remove(obj,do_unlink=True)
out=root/'public/jewellery/confluence/technical/Confluence-Casting-Stock-CAD.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
(root/'docs/confluence-casting-stock.json').write_text(json.dumps({'source':str(source),'source_object':original_name,'source_sha256':before,'source_preserved':True,'derived_model':str(out),'geometry':'Exact copied original casting stock; no remodel','prongs':parameters,'stone_count':0,'manufacturing_release':False},indent=2),encoding='utf-8')
print('ORIGINAL CASTING CAD FROZEN')
