"""Load originals read-only; stage disposable copies for portfolio study exports."""
import bpy, json, math, hashlib, sys, numpy as np
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
source=Path(r'C:\Users\Master\Documents\blender\blender filesss\troo\new\cad-3d print')
manifest=json.loads((root/'src/lib/printed-objects.json').read_text())
audit=json.loads((root/'docs/printed-geometry-audit.json').read_text())
only=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
dimensions_only='--dimensions-only' in only
only=[value for value in only if value!='--dimensions-only']
dimension_projects={'zenith-cup','individual-category','world','top-campus-ministry','top-zone-trophy','bible-projects-for-programs','vit','tuff','projects-and-programs'}
records=[]
for item in manifest:
    slug=item['slug']
    if only and slug not in only:continue
    file=source/item['modelSource']
    overrides={
        'top-zone-trophy':'white back/untitled2.blend',
        'top-campus-ministry':'white back/throuphy upload/6.blend',
        'projects-and-programs':'white back/throuphy upload/5.blend',
        'world':'new/lets upload/second.blend',
    }
    if slug in overrides:file=source.parent.parent/overrides[slug]
    source_hash=hashlib.sha256(file.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(file),load_ui=False)
    original=bpy.context.scene
    def keep(o):
        cols={c.name for c in o.users_collection}
        if o.type not in {'MESH','CURVE','FONT'} or o.hide_render:return False
        if cols & {'Collection 1','Room and lights','tree','tree.001','hh',"not'"}:return False
        return True
    parts=[o for o in original.objects if keep(o)]
    direction=(original.camera.matrix_world.to_quaternion()@Vector((0,0,1))) if original.camera else Vector((1,-2,1))
    # Medal lies in Y/Z. Its saved camera supplies the appropriate face direction.
    stage=bpy.data.scenes.new('Portfolio export / disposable')
    bpy.context.window.scene=stage
    for o in parts:
        copy=o.copy();copy.data=o.data.copy();copy.parent=None;copy.matrix_world=o.matrix_world.copy()
        stage.collection.objects.link(copy)
    copies=list(stage.objects)
    deps=bpy.context.evaluated_depsgraph_get()
    bounds=[]
    for o in copies:
        evaluated=o.evaluated_get(deps)
        mesh=evaluated.to_mesh()
        bounds.extend(evaluated.matrix_world@v.co for v in mesh.vertices)
        evaluated.to_mesh_clear()
    lo=Vector([min(v[i] for v in bounds) for i in range(3)])
    hi=Vector([max(v[i] for v in bounds) for i in range(3)])
    centre=(lo+hi)*.5;span=max(hi-lo)
    cam=bpy.data.objects.new('Study camera',bpy.data.cameras.new('Study camera'))
    stage.collection.objects.link(cam);stage.camera=cam;cam.data.type='ORTHO'
    cam.location=centre+direction.normalized()*span*5
    cam.rotation_euler=(centre-cam.location).to_track_quat('-Z','Y').to_euler()
    rotation=cam.rotation_euler.to_matrix().transposed()
    projected=[rotation@(v-centre) for v in bounds]
    cam.data.ortho_scale=max(max(v[i] for v in projected)-min(v[i] for v in projected) for i in [0,1])*1.25
    cam.data.clip_start=span*.001;cam.data.clip_end=span*20
    stage.render.engine='BLENDER_WORKBENCH'
    stage.render.resolution_x=1200;stage.render.resolution_y=1200;stage.render.resolution_percentage=100
    stage.render.image_settings.file_format='PNG';stage.render.film_transparent=False
    sh=stage.display.shading;sh.light='STUDIO';sh.studiolight_rotate_z=.35
    sh.color_type='SINGLE';sh.single_color=(.64,.61,.56)
    sh.background_type='WORLD';stage.world=bpy.data.worlds.new('Study background');stage.world.color=(.86,.84,.80)
    sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='BOTH';sh.show_object_outline=False
    stage.view_settings.view_transform='Standard'
    out=root/'public/objects'/slug;out.mkdir(parents=True,exist_ok=True)
    if not dimensions_only:
        stage.render.filepath=str(out/'clay-01.png');bpy.ops.render.render(write_still=True)
    # Native mesh edge strips preserve authored polygons (no shader triangulation).
    for o in copies:
        if dimensions_only:continue
        if o.type!='MESH':continue
        if len(o.data.vertices)>500000:
            coords=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',coords)
            coords=coords.reshape(-1,3)
            matrix=np.array(o.matrix_world);coords=coords@matrix[:3,:3].T+matrix[:3,3]
            projected=(coords-np.array(centre))@np.array(rotation).T
            pixels=np.column_stack((600+projected[:,0]*1200/cam.data.ortho_scale,600-projected[:,1]*1200/cam.data.ortho_scale))
            edges=np.empty(len(o.data.edges)*2,dtype=np.int32);o.data.edges.foreach_get('vertices',edges)
            np.savez_compressed(out/'dense-topology.npz',pixels=pixels,edges=edges.reshape(-1,2))
            o.hide_render=True
            continue
        for mod in o.modifiers:
            if mod.type=='SUBSURF':mod.show_render=False;mod.show_viewport=False
        wire=o.modifiers.new('Portfolio topology','WIREFRAME')
        wire.thickness=span*.00045/max(abs(v) for v in o.matrix_world.to_scale())
        wire.use_replace=True;wire.use_even_offset=False;wire.offset=0
    sh.single_color=(.13,.12,.11);sh.show_cavity=False;sh.show_shadows=False
    if not dimensions_only:
        stage.render.filepath=str(out/'topology-01.png');bpy.ops.render.render(write_still=True)
    # Dimensioned front/side silhouettes, rendered from evaluated original forms.
    if slug in dimension_projects:
        for o in copies:
            if o.type=='MESH':
                wire=o.modifiers.get('Portfolio topology')
                if wire:o.modifiers.remove(wire)
                for mod in o.modifiers:
                    if mod.type=='SUBSURF':mod.show_render=True;mod.show_viewport=True
        sh.single_color=(.3,.29,.27);sh.light='FLAT';sh.show_cavity=False
        stage.render.film_transparent=True
        view_axes=[('front',Vector((0,-1,0))),('side',Vector((1,0,0)))]
        if slug=='individual-category':view_axes=[('front',Vector((1,0,0))),('side',Vector((0,-1,0)))]
        for name,axis in view_axes:
            cam.location=centre+axis*span*5;cam.rotation_euler=(centre-cam.location).to_track_quat('-Z','Y').to_euler()
            cam.data.ortho_scale=span*1.25
            stage.render.filepath=str(out/f'dimension-{name}.png');bpy.ops.render.render(write_still=True)
        width_axis=1 if slug=='individual-category' else 0
        depth_axis=1-width_axis
        dimension=dict(width=round((hi[width_axis]-lo[width_axis])*original.unit_settings.scale_length*1000,1),depth=round((hi[depth_axis]-lo[depth_axis])*original.unit_settings.scale_length*1000,1),height=round((hi.z-lo.z)*original.unit_settings.scale_length*1000,1),bounds=[list(lo),list(hi)],widthAxis=width_axis,depthAxis=depth_axis,orthoScale=span*1.25)
    else:dimension=None
    unchanged=hashlib.sha256(file.read_bytes()).hexdigest()==source_hash
    record=dict(slug=slug,sourceFile=str(file),sha256=source_hash,parts=[o.name for o in parts],dimension=dimension,sourceUnchanged=unchanged)
    (root/'docs'/f'printed-study-{slug}.json').write_text(json.dumps(record,indent=2))
    print('STUDY_COMPLETE',slug,record,flush=True)
