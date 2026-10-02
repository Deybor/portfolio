"""Read frozen ring scenes; never save source Blender files."""
import bpy, json, hashlib, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
SRC=Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES')
paths={'confluence':SRC/'Confluence_First_Ring/Approved_Model/Confluence_Refined_Print.blend',
       'iced-out-ring':SRC/'Ring_Iced_Out_03/Ring_Iced_Out_03.blend'}
result={}
for slug,path in paths.items():
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(path))
    meshes=[]
    for o in bpy.data.objects:
        if o.type!='MESH': continue
        points=[o.matrix_world@v.co for v in o.data.vertices]
        lo=[min(v[i] for v in points) for i in range(3)]
        hi=[max(v[i] for v in points) for i in range(3)]
        meshes.append({'name':o.name,'collections':[c.name for c in o.users_collection],
            'hidden_render':o.hide_render,'hidden_viewport':o.hide_viewport,
            'dimensions':[hi[i]-lo[i] for i in range(3)],'min':lo,'max':hi,
            'vertices':len(o.data.vertices),'faces':len(o.data.polygons)})
    result[slug]={'source':str(path),'sha256':sha,'active_scene':bpy.context.scene.name,
        'unit_scale':bpy.context.scene.unit_settings.scale_length,
        'scenes':[{'name':s.name,'visible_meshes':[o.name for o in s.objects if o.type=='MESH' and not o.hide_render]} for s in bpy.data.scenes],
        'meshes':meshes}
    assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
(ROOT/'docs/ring-specification-inspection.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('READ_ONLY_RING_INSPECTION_COMPLETE')
