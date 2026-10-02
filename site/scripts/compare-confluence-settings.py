"""Read-only, identical-camera comparison of finished and pre-setting Confluence models."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Matrix,Vector
root=Path(__file__).resolve().parents[1]
original=Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES\Confluence_First_Ring\Approved_Model\Confluence_Refined_Print.blend')
cad=root/'public/jewellery/confluence/technical/Confluence-Straight-Prong-CAD.blend'
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [original,cad]}
sources=[('finished',original,'Confluence finished metal — single solid'),('approved-stock',original,'Confluence casting pattern — uncut prong stock'),('current-cad',cad,'Confluence - straight-prong CAD body')]
out=root/'.qa/confluence-setting-comparison';out.mkdir(parents=True,exist_ok=True)
records=[]
for name,source,object_name in sources:
    bpy.ops.wm.open_mainfile(filepath=str(source))
    original_obj=bpy.data.objects[object_name]
    scene=bpy.data.scenes.new('Read-only comparison');bpy.context.window.scene=scene
    obj=bpy.data.objects.new('Comparison body',original_obj.data)
    obj.matrix_world=original_obj.matrix_world.copy();obj.color=(.4,.44,.46,1)
    scene.collection.objects.link(obj)
    scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=1000;scene.render.resolution_y=900
    scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.display.shading.light='STUDIO';scene.display.shading.color_type='OBJECT'
    scene.display.shading.show_shadows=False;scene.display.shading.show_cavity=True
    scene.display.shading.cavity_type='BOTH';scene.display.shading.show_object_outline=True
    scene.view_settings.view_transform='Standard'
    camera=bpy.data.objects.new('Same camera',bpy.data.cameras.new('Same camera'))
    camera.data.type='ORTHO';camera.data.ortho_scale=27
    camera.matrix_world=Matrix(((1,0,0,0),(0,0,-1,-100),(0,1,0,11.2),(0,0,0,1)))
    scene.collection.objects.link(camera);scene.camera=camera
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
    records.append({'view':name,'source':str(source),'object':object_name,'vertices':len(original_obj.data.vertices),
        'camera':'Front X-Z; fixed centre Z11.2; same 27 mm ortho scale; stones hidden'})
for source,expected in hashes.items():assert hashlib.sha256(Path(source).read_bytes()).hexdigest()==expected
(root/'docs/confluence-setting-comparison.json').write_text(json.dumps({'views':records,'sources_preserved':True,'source_hashes':hashes},indent=2),encoding='utf-8')
print('SAME-ANGLE COMPARISON COMPLETE')
