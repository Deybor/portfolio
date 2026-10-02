"""Reopen both saved CAD revisions and verify the local tip-edit scope."""
import bpy,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
report=json.loads((root/'docs/confluence-centre-prong-refinement.json').read_text())
bpy.ops.wm.open_mainfile(filepath=report['source'])
original=bpy.data.objects['Confluence - approved casting CAD body']
coords=[original.matrix_world@v.co for v in original.data.vertices]
bpy.ops.wm.open_mainfile(filepath=report['derived_model'])
body=bpy.data.objects['Confluence - refined centre-prong CAD body']
assert len(coords)==len(body.data.vertices)
quadrants={};changed=0;unchanged=0
for old,vertex in zip(coords,body.data.vertices):
    new=body.matrix_world@vertex.co;difference=(old-new).length
    if old.z<=21.75 or abs(old.x)>2.45 or abs(old.y)>2.45:
        assert difference<1e-6,'Geometry outside free centre ends changed'
        unchanged+=1
    elif difference>1e-6:
        changed+=1;key=f'{1 if old.x>0 else -1},{1 if old.y>0 else -1}'
        quadrants[key]=quadrants.get(key,0)+1
    assert abs(new.z-old.z)<1e-6,'Prong height changed'
parent=list(range(len(coords)))
def find(i):
    while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
    return i
for edge in body.data.edges:
    a,b=map(find,edge.vertices)
    if a!=b:parent[b]=a
components=len({find(i) for i in range(len(coords))})
assert components==1
assert len(quadrants)==4,'Each of the four centre tips must have an edit'
result={'saved_revision':report['derived_model'],'connected_components':components,
    'changed_vertices':changed,'preserved_vertices':unchanged,'four_tip_edits':quadrants,
    'roots_band_galleries_side_prongs_unchanged':True,'all_z_coordinates_unchanged':True}
(root/'docs/confluence-tip-scope-audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
