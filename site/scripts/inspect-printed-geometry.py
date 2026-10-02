import bpy, json, hashlib
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
source=Path(r'C:\Users\Master\Documents\blender\blender filesss\troo\new\cad-3d print')
manifest=json.loads((root/'src/lib/printed-objects.json').read_text())
audit=[]
for item in manifest:
    file=source/item['modelSource']
    bpy.ops.wm.open_mainfile(filepath=str(file),load_ui=False)
    scene=bpy.context.scene
    objects=[]
    for o in scene.objects:
        if o.type not in {'MESH','CURVE','FONT'}:continue
        bounds=[o.matrix_world@Vector(p) for p in o.bound_box]
        objects.append(dict(name=o.name,type=o.type,hidden=o.hide_render,viewport=o.hide_get(),collections=[c.name for c in o.users_collection],min=[min(p[i] for p in bounds) for i in range(3)],max=[max(p[i] for p in bounds) for i in range(3)],vertices=len(o.data.vertices) if o.type=='MESH' else 0,modifiers=[m.type for m in o.modifiers]))
    audit.append(dict(slug=item['slug'],source=item['modelSource'],sha256=hashlib.sha256(file.read_bytes()).hexdigest(),scale=scene.unit_settings.scale_length,camera=scene.camera.name if scene.camera else None,objects=objects))
(root/'docs/printed-geometry-audit.json').write_text(json.dumps(audit,indent=2))
