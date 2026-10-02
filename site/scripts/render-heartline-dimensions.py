"""Derive Heartline orthographic views from its saved CAD; never save the source."""
import bpy, numpy as np, hashlib, json
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1]
source=Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES\Heartline_Pendant_01.blend')
before=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
source_scene=bpy.context.scene
body=bpy.data.objects['SOURCE_UNCHANGED_Pendant']
selected=[body]
def points(obj):
    p=np.empty(len(obj.data.vertices)*3,dtype=np.float64)
    obj.data.vertices.foreach_get('co',p)
    p=p.reshape((-1,3)); matrix=np.array(obj.matrix_world)
    return p@matrix[:3,:3].T+matrix[:3,3]
def box(p):
    lo=p.min(axis=0);hi=p.max(axis=0)
    return {'min':lo.tolist(),'max':hi.tolist(),'size':(hi-lo).tolist()}
world_points=[points(o) for o in selected]
combined=np.concatenate(world_points)
assembly=box(combined)
data={'source':str(source),'source_object':body.name,'sha256':before,'units':'mm',
      'unit_basis':'Saved METRIC scene, scale_length 0.001; 1 Blender unit = 1 mm',
      'scene_unit_scale':source_scene.unit_settings.scale_length,
      'body':box(world_points[0]),'assembly':assembly,
      'excluded':'Finished Heartline variant, stock variant, added melee stones, connecting ring, reference chain, clasp and floor',
      'basis':'Retained unchanged original mesh only; no added geometry',
      'views':{}}
scene=bpy.data.scenes.new('Heartline CAD presentation - not saved')
bpy.context.window.scene=scene
scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=1800;scene.render.resolution_y=1600;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=True
scene.display.shading.light='STUDIO';scene.display.shading.color_type='OBJECT'
scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
scene.display.shading.cavity_type='BOTH';scene.display.shading.show_object_outline=True
scene.display.shading.object_outline_color=(.12,.15,.17)
scene.world=bpy.data.worlds.new('CAD neutral');scene.world.color=(1,1,1)
scene.view_settings.view_transform='Standard'
for original in selected:
    obj=bpy.data.objects.new('CAD '+original.name,original.data)
    obj.matrix_world=original.matrix_world.copy()
    obj.color=(.52,.57,.6,1)
    scene.collection.objects.link(obj)
camera=bpy.data.objects.new('CAD camera',bpy.data.cameras.new('CAD camera'))
scene.collection.objects.link(camera);scene.camera=camera
camera.data.type='ORTHO';camera.data.clip_end=1000
out=ROOT/'public/jewellery/heartline-pendant/technical';out.mkdir(parents=True,exist_ok=True)
for name,direction in [('front',(0,0,1)),('side',(1,0,0)),('back',(0,0,-1)),('isometric',(1,-.4,1))]:
    centre=Vector((np.array(assembly['min'])+np.array(assembly['max']))/2)
    direction=Vector(direction).normalized()
    up_hint=Vector((0,0,1)) if name=='side' else Vector((0,1,0))
    right=up_hint.cross(direction).normalized()
    up=direction.cross(right).normalized()
    rotation=Matrix((right,up,direction)).transposed()
    inv=rotation.transposed()
    projection=(combined-np.array(centre))@np.array(inv).T
    lo=projection[:,:2].min(axis=0);hi=projection[:,:2].max(axis=0)
    offset=(lo+hi)/2
    centre+=inv.transposed()@Vector((offset[0],offset[1],0))
    camera.matrix_world=rotation.to_4x4()
    camera.matrix_world.translation=centre+direction*100
    scale=max(hi[0]-lo[0],(hi[1]-lo[1])*1800/1600)*1.18
    camera.data.ortho_scale=scale
    scene.view_layers[0].update()
    scene.render.filepath=str(out/(name+'.png'))
    bpy.ops.render.render(write_still=True)
    data['views'][name]={'image':name+'.png','ortho_scale':float(scale),
        'projected_min':(lo-offset).tolist(),'projected_max':(hi-offset).tolist()}
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
data['source_preserved']=True
(ROOT/'docs/heartline-dimensions.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print('HEARTLINE CAD VIEWS COMPLETE',json.dumps({k:v for k,v in data.items() if k!='views'}))
