"""Read Heartline scene geometry and units without saving its source file."""
import bpy, json, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
source = Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES\Heartline_Pendant_01.blend')
before = hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
scene = bpy.context.scene
items = []
for obj in bpy.data.objects:
    if obj.type not in {'MESH', 'CURVE'}: continue
    items.append({'name': obj.name, 'type': obj.type, 'dimensions': list(obj.dimensions),
                  'location': list(obj.location), 'rotation': list(obj.rotation_euler),
                  'scale': list(obj.scale), 'hidden': obj.hide_render,
                  'vertices': len(obj.data.vertices) if obj.type == 'MESH' else None,
                  'collections': [c.name for c in obj.users_collection],
                  'in_active_scene': obj.name in scene.objects})
data = {'source': str(source), 'sha256': before, 'units': scene.unit_settings.system,
        'unit_scale': scene.unit_settings.scale_length, 'objects': items}
assert before == hashlib.sha256(source.read_bytes()).hexdigest()
(ROOT/'docs/heartline-scene-inspection.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
print(json.dumps({**{k:v for k,v in data.items() if k!='objects'},
                  'objects': [o for o in items if not o['name'].startswith(('Chain_Link_', 'Heartline_Melee_'))]}))
