import bpy,json
from pathlib import Path
source=Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES\Confluence_First_Ring\Approved_Model\Confluence_Refined_Print.blend')
bpy.ops.wm.open_mainfile(filepath=str(source))
for obj in bpy.data.objects:
    if obj.type=='MESH' and ('Confluence' in obj.name or 'Audit' in obj.name or 'pattern' in obj.name.lower()):
        print(json.dumps({'name':obj.name,'vertices':len(obj.data.vertices),'hidden':obj.hide_render,'scene':[s.name for s in bpy.data.scenes if obj.name in s.objects], 'modifiers':[m.type for m in obj.modifiers]}))
