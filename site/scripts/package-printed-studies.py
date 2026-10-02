from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,html,math
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'src/lib/printed-objects.json').read_text())
def simplify(p,e=1.0):
    if len(p)<3:return p
    a,b=p[0],p[-1];dx,dy=b[0]-a[0],b[1]-a[1];den=math.hypot(dx,dy)
    ds=[abs(dy*(q[0]-a[0])-dx*(q[1]-a[1]))/den if den else math.dist(q,a) for q in p]
    i=max(range(len(ds)),key=ds.__getitem__)
    return simplify(p[:i+1],e)[:-1]+simplify(p[i:],e) if ds[i]>e else [a,b]
def outlines(file):
    mask=np.array(Image.open(file))[:,:,3]>127;pad=np.pad(mask,1);adj={}
    for direction,other in enumerate([pad[:-2,1:-1],pad[1:-1,2:],pad[2:,1:-1],pad[1:-1,:-2]]):
        ys,xs=np.where(mask & ~other)
        for x,y in zip(xs.tolist(),ys.tolist()):
            a,b=[((x,y),(x+1,y)),((x+1,y),(x+1,y+1)),((x+1,y+1),(x,y+1)),((x,y+1),(x,y))][direction]
            adj.setdefault(a,[]).append(b)
    paths=[]
    while adj:
        a=start=next(iter(adj));line=[a]
        while a in adj:
            b=adj[a].pop()
            if not adj[a]:del adj[a]
            line.append(b);a=b
            if a==start:break
        if len(line)>20:
            mid=len(line)//2;paths.append(simplify(line[:mid+1])+simplify(line[mid:])[1:])
    return paths
for item in manifest:
    slug=item['slug'];out=root/'public/objects'/slug
    record=json.loads((root/'docs'/f'printed-study-{slug}.json').read_text())
    if not record['sourceUnchanged']:raise RuntimeError('Source changed: '+slug)
    dense=out/'dense-topology.npz'
    if dense.exists():
        data=np.load(dense);pixels=data['pixels'];edges=data['edges'];image=Image.open(out/'topology-01.png').convert('RGB');draw=ImageDraw.Draw(image)
        for a,b in edges:
            p,q=pixels[a],pixels[b]
            draw.line((float(p[0]),float(p[1]),float(q[0]),float(q[1])),fill=(72,68,63),width=1)
        image.save(out/'topology-01.png');dense.unlink()
    item['views']=[v for v in item['views'] if not v.get('generated')]
    for kind,name in [('clay','clay-01'),('wireframe','topology-01')]:
        Image.open(out/(name+'.png')).convert('RGB').save(out/(name+'.webp'),quality=90,method=6)
        item['views'].append(dict(kind=kind,index=1+sum(v['kind']==kind for v in item['views']),source=Path(record.get('sourceFile',item['modelSource'])).name,width=1200,height=1200,image=f'/objects/{slug}/{name}.webp',full=f'/objects/{slug}/{name}.png',generated=True))
    if record['dimension']:
        dim=record['dimension'];item['dimensions']={k:dim[k] for k in ['width','depth','height']}
        nodes=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 800"><rect width="1000" height="800" fill="#f3efe7"/><style>text{font-family:Arial,sans-serif;fill:#39352f}.line{fill:none;stroke:#514a40;stroke-width:1.3}.dim{fill:none;stroke:#786c57;stroke-width:1}</style>']
        nodes.append(f'<text x="50" y="58" font-size="24">{html.escape(item["title"])}</text><text x="50" y="86" font-size="12" letter-spacing="2">MODEL DIMENSIONS / mm</text><path class="dim" d="M50 110H950"/>')
        for n,(name,width) in enumerate([('front',dim['width']),('side',dim['depth'])]):
            cx=270+n*470;cy=405;factor=480/1200
            for path in outlines(out/f'dimension-{name}.png'):
                d='M'+'L'.join(f'{cx+(x-600)*factor:.2f},{cy+(y-600)*factor:.2f}' for x,y in path)+'Z'
                nodes.append(f'<path class="line" d="{d}"/>')
            w=width/(dim['orthoScale']*1000)*480;h=dim['height']/(dim['orthoScale']*1000)*480
            left=cx-w/2;right=cx+w/2;top=cy-h/2;bottom=cy+h/2;dy=bottom+35;dx=left-42
            nodes.append(f'<path class="dim" d="M{left} {bottom+8}V{dy+8}M{right} {bottom+8}V{dy+8}M{left} {dy}H{right}M{left-4} {dy+4}l8 -8M{right-4} {dy+4}l8 -8"/><text x="{cx}" y="{dy+24}" text-anchor="middle" font-size="15">{width:.1f}</text>')
            nodes.append(f'<path class="dim" d="M{left-8} {top}H{dx-8}M{left-8} {bottom}H{dx-8}M{dx} {top}V{bottom}M{dx-4} {top+4}l8 -8M{dx-4} {bottom+4}l8 -8"/><text transform="translate({dx-12},{cy}) rotate(-90)" text-anchor="middle" font-size="15">{dim["height"]:.1f}</text>')
            nodes.append(f'<text x="{cx}" y="690" text-anchor="middle" font-size="13" letter-spacing="2">{name.upper()}</text>')
        nodes.append('<path class="dim" d="M50 720H950"/><text x="50" y="748" font-size="12">Overall dimensions measured from the assembled Blender model.</text><text x="50" y="771" font-size="12">Dimensions in millimetres. Material and manufacturing tolerances are unconfirmed.</text></svg>')
        (out/'dimensions.svg').write_text(''.join(nodes),encoding='utf-8')
        item['views'].append(dict(kind='dimensions',index=1,source=Path(record.get('sourceFile',item['modelSource'])).name,width=1000,height=800,image=f'/objects/{slug}/dimensions.svg',full=f'/objects/{slug}/dimensions.svg',generated=True))
    if (out/'workspace-01.png').exists():
        im=Image.open(out/'workspace-01.png').convert('RGB');im.save(out/'workspace-01.webp',quality=94,method=6)
        item['views'].append(dict(kind='wireframe',index=1+sum(v['kind']=='wireframe' for v in item['views']),source=Path(record['sourceFile']).name,width=im.width,height=im.height,image=f'/objects/{slug}/workspace-01.webp',full=f'/objects/{slug}/workspace-01.png',label='Blender workspace',generated=True))
(root/'src/lib/printed-objects.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Packaged',len(manifest),'object studies')
