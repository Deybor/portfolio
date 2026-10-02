"""Read beauty-scene cameras and collections without changing their saved files."""
import bpy, json, hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sources=Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES\BlenderKit_Beauty')
results={}
for slug,filename in [('confluence','Confluence_Environment.blend'),('iced-out-ring','Iced_Ring_Gallery.blend'),('heartline-pendant','Heartline_Studio.blend')]:
    source=sources/filename
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene=bpy.context.scene
    results[slug]={'source':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'camera':scene.camera.name if scene.camera else None,
        'resolution':[scene.render.resolution_x,scene.render.resolution_y],
        'collections':[{ 'name':c.name,'hide_render':c.hide_render,'objects':len(c.objects),'children':[x.name for x in c.children]} for c in bpy.data.collections],
        'objects':[{'name':o.name,'type':o.type,'hidden':o.hide_render,'collections':[c.name for c in o.users_collection], 'vertices':len(o.data.vertices) if o.type=='MESH' else 0} for o in scene.objects]}
    print('COVER SCENE',slug,json.dumps({k:v for k,v in results[slug].items() if k!='objects'}))
(root/'docs/cover-scene-inspection.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
