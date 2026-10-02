"""Read-only connectivity and section audit of the frozen Confluence CAD."""
import bpy, json, hashlib
from pathlib import Path
from collections import Counter, defaultdict
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'docs/ring-specification-cad-data.json').read_text())['confluence']
source=Path(data['source']);before=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
obj=bpy.data.objects[data['source_object']]
parent=list(range(len(obj.data.vertices)))
def find(x):
    while parent[x]!=x:
        parent[x]=parent[parent[x]];x=parent[x]
    return x
for edge in obj.data.edges:
    a,b=map(find,edge.vertices)
    if a!=b:parent[b]=a
groups=defaultdict(list)
for vertex in obj.data.vertices:groups[find(vertex.index)].append(obj.matrix_world@vertex.co)
components=[{'vertices':len(points),'min':[min(p[i] for p in points) for i in range(3)],
    'max':[max(p[i] for p in points) for i in range(3)]} for points in groups.values()]
degree=Counter();neighbors=defaultdict(set)
for a,b in data['section_segments']:
    a=tuple(round(x,5) for x in a);b=tuple(round(x,5) for x in b)
    degree[a]+=1;degree[b]+=1;neighbors[a].add(b);neighbors[b].add(a)
seen=set();loops=[]
for vertex in degree:
    if vertex in seen:continue
    stack=[vertex];group=[]
    while stack:
        point=stack.pop()
        if point in seen:continue
        seen.add(point);group.append(point);stack.extend(neighbors[point]-seen)
    loops.append({'points':len(group),'degrees':dict(Counter(degree[p] for p in group)),
        'min':[min(p[i] for p in group) for i in range(3)],'max':[max(p[i] for p in group) for i in range(3)]})
result={'source':str(source),'source_sha256':before,'mesh_components':sorted(components,key=lambda c:-c['vertices']),
    'section_segments':len(data['section_segments']),'section_graph_components':loops,
    'section_endpoint_degrees':dict(Counter(degree.values()))}
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
(root/'docs/confluence-section-audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
