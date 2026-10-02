"""Render the supplied Heartline scene without saving or changing source geometry."""
import bpy, hashlib, json
from pathlib import Path

source = Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES\Heartline_Pendant_01.blend')
out = Path(__file__).resolve().parents[1] / 'public/jewellery/heartline-pendant'
out.mkdir(parents=True, exist_ok=True)
before = hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
scene = bpy.context.scene
scene.render.resolution_percentage = 100
scene.cycles.samples = 96
scene.cycles.device = 'CPU'
scene.cycles.use_denoising = True
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(out / 'render-01.png')
bpy.ops.render.render(write_still=True)
after = hashlib.sha256(source.read_bytes()).hexdigest()
assert before == after, 'Source changed'
audit = {'source': str(source), 'scene': scene.name, 'camera': scene.camera.name,
         'source_sha256_before': before, 'source_sha256_after': after,
         'source_preserved': True, 'geometry_changed': False,
         'method': 'Existing saved camera, lighting and materials; Cycles 96 samples; no blend saved',
         'output': str(out / 'render-01.png'), 'resolution': [scene.render.resolution_x, scene.render.resolution_y]}
(Path(__file__).resolve().parents[1] / 'docs/heartline-portfolio-render.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
print('SOURCE_PRESERVED', before)
