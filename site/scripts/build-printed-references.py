"""Crop verified matching designs from the unchanged award design PDF."""
from pathlib import Path
import json,hashlib
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
source=root/'public/objects/award-designs.pdf'
before=hashlib.sha256(source.read_bytes()).hexdigest()
pdf=pdfium.PdfDocument(source)
# Bounds measured against the reviewed 1100 x 617 page previews.
matches={
 'top-zone-trophy':(3,(8,170,345,530)),
 'top-campus-ministry':(3,(680,190,865,420)),
 'bible-projects-for-programs':(4,(12,138,346,531)),
 'projects-and-programs':(8,(16,155,350,530)),
 'individual-category':(8,(360,180,740,530)),
 'vit':(8,(910,205,1060,475)),
 'tuff':(7,(350,175,760,530)),
}
items=json.loads((root/'src/lib/printed-objects.json').read_text(encoding='utf-8'))
audit=[]
contact=Image.new('RGB',(1050,900),'#ece8df');draw=ImageDraw.Draw(contact)
for n,(slug,(page,box)) in enumerate(matches.items()):
 image=pdf[page-1].render(scale=4).to_pil().convert('RGB')
 crop=image.crop(tuple(round(v*(image.width/1100 if axis%2==0 else image.height/617)) for axis,v in enumerate(box)))
 out=root/'public/objects'/slug;crop.save(out/'reference-01.png');crop.save(out/'reference-01.webp',quality=95,method=6)
 item=next(i for i in items if i['slug']==slug)
 item['views']=[v for v in item['views'] if v.get('image')!=f'/objects/{slug}/reference-01.webp']
 item['views'].append(dict(kind='references',index=1,source=f'award-designs.pdf, page {page}',width=crop.width,height=crop.height,image=f'/objects/{slug}/reference-01.webp',full=f'/objects/{slug}/reference-01.png',label=f'Original design drawing / PDF page {page}',referencePage=page))
 audit.append(dict(slug=slug,page=page,bounds1100x617=box))
 thumb=crop.copy();thumb.thumbnail((325,260));x=n%3*350;y=n//3*300;contact.paste(thumb,(x,y));draw.text((x+10,y+270),item['title'],fill='black')
(root/'src/lib/printed-objects.json').write_text(json.dumps(items,indent=2),encoding='utf-8')
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
(root/'docs/printed-reference-audit.json').write_text(json.dumps(dict(sourceSha256=before,sourceUnchanged=True,matches=audit),indent=2))
contact.save(root/'docs/printed-reference-contact.jpg')
print('Cropped and attached 7 matched references; source PDF unchanged.')
