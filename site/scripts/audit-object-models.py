"""Read model metadata for the portfolio without saving or modifying models."""
import bpy
from pathlib import Path
import json

root = Path(r'C:\Users\Master\Documents\portfolio\porfolio update')
source = Path(r'C:\Users\Master\Documents\blender\blender filesss\troo\new\cad-3d print')
records = []
for model in sorted(source.glob('*.blend')):
    bpy.ops.wm.open_mainfile(filepath=str(model), load_ui=False)
    scene = bpy.context.scene
    records.append({
        'file': model.name,
        'units': scene.unit_settings.system,
        'lengthUnit': scene.unit_settings.length_unit,
        'unitScale': scene.unit_settings.scale_length,
        'sceneProperties': {key: str(scene[key]) for key in scene.keys() if key != '_RNA_UI'},
        'meshObjects': [{
            'name': obj.name,
            'dimensionsInSceneUnits': list(obj.dimensions),
            'properties': {key: str(obj[key]) for key in obj.keys() if key != '_RNA_UI'},
        } for obj in scene.objects if obj.type == 'MESH'],
    })
    print('READ_ONLY_AUDIT', model.name, scene.unit_settings.system, flush=True)
(root / 'docs' / 'printed-objects-model-audit.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
print('AUDIT_COMPLETE', len(records), flush=True)
