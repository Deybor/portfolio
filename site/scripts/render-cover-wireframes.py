"""Make cover-only wire renders from the exact beauty cameras; never save a .blend."""
import bpy, json, hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
audit=json.loads((root/'docs/cover-scene-inspection.json').read_text())
results={}
for slug,info in audit.items():
    source=Path(info['source'])
    assert hashlib.sha256(source.read_bytes()).hexdigest()==info['sha256']
    bpy.ops.wm.open_mainfile(filepath=str(source))
    original_scene=bpy.context.scene
    originals=[o for o in original_scene.objects if o.type=='MESH' and not o.hide_render
        and any(c==original_scene.collection for c in o.users_collection)]
    if slug=='confluence':
        originals=[o for o in originals if o.name!='Jewellery travertine dish']
    expected={'confluence':4,'iced-out-ring':418,'heartline-pendant':129}[slug]
    assert len(originals)==expected,(slug,len(originals))
    scene=bpy.data.scenes.new('Cover wireframe only - not saved')
    bpy.context.window.scene=scene
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=64
    scene.cycles.use_denoising=False
    scene.render.resolution_x=1200
    scene.render.resolution_y=round(1200*info['resolution'][1]/info['resolution'][0])
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
    material=bpy.data.materials.new('Cover wire / black on warm ivory');material.use_nodes=True
    nodes=material.node_tree.nodes;nodes.clear();links=material.node_tree.links
    wire=nodes.new('ShaderNodeWireframe');wire.use_pixel_size=True;wire.inputs['Size'].default_value=1.2
    mix=nodes.new('ShaderNodeMixRGB')
    def linear(channel):
        value=channel/255
        return value/12.92 if value<=.04045 else ((value+.055)/1.055)**2.4
    mix.inputs[1].default_value=tuple(linear(c) for c in (239,232,220))+(1,)
    mix.inputs[2].default_value=(.001,.001,.001,1)
    emission=nodes.new('ShaderNodeEmission')
    output=nodes.new('ShaderNodeOutputMaterial')
    links.new(wire.outputs['Fac'],mix.inputs[0]);links.new(mix.outputs[0],emission.inputs['Color'])
    links.new(emission.outputs[0],output.inputs['Surface'])
    display_topology=[]
    for original in originals:
        obj=original.copy();obj.data=original.data.copy();obj.parent=None
        obj.matrix_world=original.matrix_world.copy()
        obj.hide_render=False;obj.hide_viewport=False
        obj.data.materials.clear();obj.data.materials.append(material)
        for polygon in obj.data.polygons:polygon.material_index=0
        scene.collection.objects.link(obj)
        # Dense sculpt meshes become a grey mass at card size. A disposable
        # display copy exposes readable topology; source/design CAD is untouched.
        if len(obj.data.polygons)>6000:
            modifier=obj.modifiers.new('Cover display topology only','DECIMATE')
            modifier.ratio=6000/len(obj.data.polygons)
            modifier.use_collapse_triangulate=True
            display_topology.append({'object':original.name,'source_faces':len(original.data.polygons),
                'display_target_faces':6000,'ratio':modifier.ratio})
    camera=original_scene.camera.copy();camera.data=original_scene.camera.data.copy()
    camera.parent=None;camera.matrix_world=original_scene.camera.matrix_world.copy()
    camera.data.dof.use_dof=False;scene.collection.objects.link(camera);scene.camera=camera
    out=root/'public/jewellery'/slug/'cover-wireframe.png'
    scene.render.filepath=str(out)
    bpy.ops.render.render(write_still=True)
    assert hashlib.sha256(source.read_bytes()).hexdigest()==info['sha256']
    results[slug]={'source':str(source),'source_sha256':info['sha256'],'source_preserved':True,
        'camera':info['camera'],'mesh_count':len(originals),
        'mesh_geometry':'Beauty meshes copied into a disposable cover scene; dense surface topology simplified for legibility',
        'display_topology':display_topology,
        'environment_removed':True,'camera_depth_of_field':False,'image':str(out),
        'resolution':[scene.render.resolution_x,scene.render.resolution_y],
        'objects':[o.name for o in originals]}
    (root/'docs/cover-wireframe-provenance.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('COVER WIREFRAME COMPLETE',slug,flush=True)
