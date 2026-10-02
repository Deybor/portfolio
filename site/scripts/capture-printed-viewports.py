"""Export actual Blender 3D viewport snapshots, including theme background and grid.
Run with a separate Blender UI process. Originals are loaded but never saved.
"""
import bpy,json,hashlib,traceback
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'src/lib/printed-objects.json').read_text())
records=[]
def capture_next():
    try:
        if not items:
            (root/'docs/printed-viewport-audit.json').write_text(json.dumps(records,indent=2))
            bpy.ops.wm.quit_blender();return None
        item=items.pop(0);slug=item['slug']
        record=json.loads((root/f'docs/printed-study-{slug}.json').read_text())
        source=Path(record['sourceFile']);before=hashlib.sha256(source.read_bytes()).hexdigest()
        bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False)
        original=bpy.context.scene
        parts=[o for o in original.objects if o.name in record['parts']]
        scene=bpy.data.scenes.new('Portfolio viewport / disposable')
        window=bpy.context.window_manager.windows[0]
        window.scene=scene
        for o in parts:
            copy=o.copy();copy.data=o.data.copy();copy.parent=None;copy.matrix_world=o.matrix_world.copy()
            scene.collection.objects.link(copy)
            for m in copy.modifiers:
                if m.type=='SUBSURF':m.show_viewport=False
        points=[o.matrix_world@Vector(p) for o in scene.objects for p in o.bound_box]
        lo=Vector([min(p[i] for p in points) for i in range(3)]);hi=Vector([max(p[i] for p in points) for i in range(3)])
        centre=(lo+hi)*.5;span=max(hi-lo)
        direction=(original.camera.matrix_world.to_quaternion()@Vector((0,0,1))) if original.camera else Vector((1,-2,1))
        area=next(a for a in window.screen.areas if a.type=='VIEW_3D')
        region=next(r for r in area.regions if r.type=='WINDOW');space=area.spaces.active
        space.shading.type='WIREFRAME';space.shading.background_type='THEME'
        space.overlay.show_overlays=True;space.overlay.show_floor=True
        space.overlay.show_axis_x=True;space.overlay.show_axis_y=True
        space.overlay.grid_scale=span/10
        space.overlay.show_text=True;space.overlay.show_cursor=False
        space.region_3d.view_location=centre
        space.region_3d.view_rotation=(-direction).to_track_quat('-Z','Y')
        space.region_3d.view_perspective='ORTHO';space.region_3d.view_distance=span*1.6
        space.clip_start=span*.0001;space.clip_end=span*100
        scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
        scene.render.film_transparent=False;scene.render.image_settings.file_format='PNG'
        scene.render.filepath=str(root/f'public/objects/{slug}/viewport-01.png')
        with bpy.context.temp_override(window=window,area=area,region=region):
            bpy.ops.render.opengl(write_still=True,view_context=True)
        records.append(dict(slug=slug,sourceFile=str(source),sha256=before,sourceUnchanged=hashlib.sha256(source.read_bytes()).hexdigest()==before,method='Blender render.opengl, VIEW_3D context, theme background and overlays'))
        print('VIEWPORT_COMPLETE',slug,flush=True)
        return 1.0
    except Exception:
        (root/'docs/printed-viewport-error.txt').write_text(traceback.format_exc())
        bpy.ops.wm.quit_blender();return None
bpy.app.timers.register(capture_next,first_interval=3.0,persistent=True)
