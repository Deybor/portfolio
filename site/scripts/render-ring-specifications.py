"""Derive orthographic views and sections from frozen CAD, without saving source files."""
import bpy, bmesh, json, hashlib, math, sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
inspection=json.loads((ROOT/'docs/ring-specification-inspection.json').read_text())
all_data=json.loads((ROOT/'docs/ring-specification-cad-data.json').read_text())
def bounds(objects):
    pts=[o.matrix_world@v.co for o in objects for v in o.data.vertices]
    lo=[min(v[i] for v in pts) for i in range(3)]
    hi=[max(v[i] for v in pts) for i in range(3)]
    return {'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]}
def section(obj,axis,value):
    # Intersect real mesh triangles with a plane. Lines are actual CAD contours.
    mesh=obj.data; mesh.calc_loop_triangles()
    points=[obj.matrix_world@v.co for v in mesh.vertices]
    output=[]
    for tri in mesh.loop_triangles:
        vs=[points[i] for i in tri.vertices]
        ds=[v[axis]-value for v in vs]
        if min(ds)>=0 or max(ds)<=0: continue
        hits=[]
        for i,j in [(0,1),(1,2),(2,0)]:
            if ds[i]*ds[j]<0:
                p=vs[i].lerp(vs[j],ds[i]/(ds[i]-ds[j])); hits.append(list(p))
        if len(hits)==2: output.append(hits)
    return output
def audit(obj):
    bm=bmesh.new(); bm.from_mesh(obj.data); bm.transform(obj.matrix_world)
    d={'boundary_edges':sum(e.is_boundary for e in bm.edges),
       'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),
       'signed_volume_mm3':bm.calc_volume(signed=True),'bounds':bounds([obj])}
    d['stored_vertices']=len(bm.verts)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.00001)
    d['coincident_vertex_weld_check']={'analysis_only':True,'distance_mm':0.00001,
        'vertices':len(bm.verts),'boundary_edges':sum(e.is_boundary for e in bm.edges),
        'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),
        'signed_volume_mm3':bm.calc_volume(signed=True)}
    bm.free(); return d
for slug,info in inspection.items():
    if '--confluence-only' in sys.argv and slug!='confluence':continue
    source=Path(info['source']); before=hashlib.sha256(source.read_bytes()).hexdigest()
    if slug=='confluence':
        original_source=source
        source=ROOT/'public/jewellery/confluence/technical/Confluence-Refined-Centre-Prongs-CAD.blend'
        before=hashlib.sha256(source.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(source))
    if slug=='confluence':
        metal=bpy.data.objects['Confluence - refined centre-prong CAD body']
        stones=[]
        stock=None
        eye={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'isometric':(1,-1,0.8)}
        axis=1
    else:
        metal=bpy.data.objects['CAD base - exact source mesh']
        stones=[]
        stock=None; eye={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'isometric':(1,-1,1)}; axis=1
    out=ROOT/'public/jewellery'/slug/'technical'; out.mkdir(parents=True,exist_ok=True)
    data={'source':str(source),'source_object':metal.name,'source_sha256':before,'units':'mm' if slug=='confluence' else 'source numerical units interpreted as mm; author confirmation pending',
          'metal':audit(metal),'assembly':bounds([metal]+stones),'stone_count':len(stones),
          'stone_bounds':[{'name':s.name,**bounds([s])} for s in stones],
          'section_plane':{'axis':axis,'value':0},'section_segments':section(metal,axis,0),'views':{}}
    if stock: data['casting_pattern']=audit(stock)
    if slug=='confluence':
        data['original_source']=str(original_source)
        data['original_source_sha256']=hashlib.sha256(original_source.read_bytes()).hexdigest()
        data['casting_stock_parameters']=json.loads((ROOT/'docs/confluence-casting-stock.json').read_text())['prongs']
        data['centre_prong_refinement']=json.loads((ROOT/'docs/confluence-centre-prong-refinement.json').read_text())
    if slug=='iced-out-ring':
        pts=[metal.matrix_world@v.co for v in metal.data.vertices]
        tree=BVHTree.FromPolygons(pts,[list(p.vertices) for p in metal.data.polygons])
        box=bounds([metal]); cx,cy,cz=[(box['min'][i]+box['max'][i])/2 for i in range(3)]
        samples=[]
        for section_i in range(151):
            axial=-1.5+section_i*.02; radii=[]
            for a in range(180):
                angle=a*2*math.pi/180; direction=Vector((math.cos(angle),0,math.sin(angle)))
                hit,normal,index,distance=tree.ray_cast(Vector((cx,cy+axial,cz)),direction,30)
                if hit is not None:radii.append(distance)
            if radii:samples.append({'axial_y_offset':axial,'minimum_sampled_diameter':2*min(radii),'rays':len(radii)})
        data['bore_samples']={'method':'First radial hits in X-Z at 151 axial Y sections within +/-1.50 of bbox centre; 180 rays per section; original object only',
            'minimum_sampled_clear_bore':min(s['minimum_sampled_diameter'] for s in samples),'sections':samples}
    if '--audit-only' in sys.argv:
        previous=json.loads((ROOT/'docs/ring-specification-cad-data.json').read_text())
        previous[slug]['metal']=data['metal']
        if stock: previous[slug]['casting_pattern']=data['casting_pattern']
        (ROOT/'docs/ring-specification-cad-data.json').write_text(json.dumps(previous,indent=2),encoding='utf-8')
        continue
    # Isolated presentation scene references frozen meshes, with transforms copied.
    scene=bpy.data.scenes.new('Specification only - never saved'); bpy.context.window.scene=scene
    scene.render.engine='BLENDER_WORKBENCH'
    scene.render.resolution_x=1800; scene.render.resolution_y=1600; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=True
    scene.display.shading.light='STUDIO'; scene.display.shading.color_type='OBJECT'
    scene.display.shading.show_shadows=True; scene.display.shading.show_cavity=True
    scene.display.shading.cavity_type='BOTH'; scene.display.shading.show_object_outline=True
    scene.display.shading.object_outline_color=(0.12,0.15,0.17)
    scene.world=bpy.data.worlds.new('Specification neutral'); scene.world.color=(1,1,1)
    scene.view_settings.view_transform='Standard'
    copies=[]
    for source_o in [metal]+stones+([stock] if stock else []):
        o=bpy.data.objects.new('SPEC '+source_o.name,source_o.data); o.matrix_world=source_o.matrix_world.copy()
        o.color=(0.54,0.58,0.60,1) if source_o==metal or source_o==stock else (0.87,0.9,0.91,1)
        scene.collection.objects.link(o); copies.append(o)
    camera=bpy.data.objects.new('Specification camera',bpy.data.cameras.new('Specification camera'))
    scene.collection.objects.link(camera); scene.camera=camera; camera.data.type='ORTHO'; camera.data.clip_end=1000
    def render(name,direction,indices,exploded=False,zoom=None):
        selected=[copies[i] for i in indices]
        for o in copies: o.hide_render=o not in selected
        saved=[o.matrix_world.copy() for o in selected]
        if exploded:
            for o in selected[1:]:
                if slug=='confluence': o.location.z+=6
                else:
                    p=o.location.copy(); radius=math.hypot(p.x,p.y)
                    if radius>0: o.location.x*=1.35; o.location.y*=1.35
        scene.view_layers[0].update()
        b=bounds(selected); centre=Vector([(b['min'][i]+b['max'][i])/2 for i in range(3)])
        if zoom: centre=Vector(zoom)
        direction=Vector(direction).normalized(); camera.location=centre+direction*100
        camera.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler()
        inv=camera.rotation_euler.to_matrix().transposed()
        projected=[inv@(o.matrix_world@v.co-centre) for o in selected for v in o.data.vertices]
        lo=[min(v[i] for v in projected) for i in range(2)]; hi=[max(v[i] for v in projected) for i in range(2)]
        aspect=1800/1600
        if not zoom:
            centre+=inv.transposed()@Vector(((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,0))
            camera.location=centre+direction*100
        scale=max((hi[1]-lo[1])*aspect,hi[0]-lo[0])*1.18
        if zoom: scale=12
        camera.data.ortho_scale=scale
        file=name+'.png'; scene.render.filepath=str(out/file)
        bpy.ops.render.render(write_still=True)
        data['views'][name]={'file':file,'ortho_scale':scale,'centre':list(centre),'rotation_inverse':[list(row) for row in inv], 'pixel_size':[1800,1600], 'display_only_exploded':exploded}
        for o,matrix in zip(selected,saved): o.matrix_world=matrix
    for name,direction in eye.items(): render(name,direction,list(range(1+len(stones))))
    render('metal-only',eye['isometric'],[0])
    if stock: render('casting-stock',eye['isometric'],[len(copies)-1])
    render('exploded',eye['isometric'],list(range(1+len(stones))),True)
    if slug=='confluence': render('setting-detail',(0,-1,0.25),list(range(1+len(stones))),zoom=(0,0,21))
    else: render('setting-detail',(0,-1,0.5),[0],zoom=(0,0,10.8))
    assert hashlib.sha256(source.read_bytes()).hexdigest()==before
    if slug=='confluence':
        # Same exact derived mesh, displayed as actual polygon wires for the gallery.
        scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8;scene.cycles.use_denoising=False
        scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(1,1,1,1)
        mat=bpy.data.materials.new('CAD wire shader');mat.use_nodes=True;n=mat.node_tree.nodes;n.clear();links=mat.node_tree.links
        output=n.new('ShaderNodeOutputMaterial');face=n.new('ShaderNodeEmission');face.inputs[0].default_value=(.72,.78,.81,1)
        edge=n.new('ShaderNodeEmission');edge.inputs[0].default_value=(.025,.045,.065,1)
        wire=n.new('ShaderNodeWireframe');wire.use_pixel_size=True;wire.inputs[0].default_value=.5
        mix=n.new('ShaderNodeMixShader');links.new(wire.outputs[0],mix.inputs[0]);links.new(face.outputs[0],mix.inputs[1]);links.new(edge.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs[0])
        copies[0].data=copies[0].data.copy();copies[0].data.materials.clear();copies[0].data.materials.append(mat)
        render('wireframe-01',eye['isometric'],[0])
        render('wireframe-02',(0,-1,.25),[0],zoom=(0,0,21))
    data['source_preserved']=True; all_data[slug]=data
    (out/'measurement-register.json').write_text(json.dumps({k:v for k,v in data.items() if k!='section_segments'},indent=2),encoding='utf-8')
if '--audit-only' not in sys.argv:
    (ROOT/'docs/ring-specification-cad-data.json').write_text(json.dumps(all_data,indent=2),encoding='utf-8')
print('ORTHOGRAPHIC_AND_SECTION_EXTRACTION_COMPLETE')
