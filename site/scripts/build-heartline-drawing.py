"""Compose a readable vector dimension sheet from original Heartline CAD views."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from html import escape
import json, base64
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'public/jewellery/heartline-pendant'
data=json.loads((ROOT/'docs/heartline-dimensions.json').read_text())
W,H=1600,1120
paper=Image.new('RGB',(W,H),'white'); draw=ImageDraw.Draw(paper)
ink='#20313b';muted='#56646a';accent='#8b7250'
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>Heartline - original pendant Model dimensions</title><rect width="100%" height="100%" fill="white"/>']
def text(x,y,value,size=24,bold=False,color=ink):
    font=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
    draw.text((x,y),value,font=font,fill=color,anchor='ls')
    svg.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(value)}</text>')
def line(x1,y1,x2,y2,color=muted):
    draw.line((x1,y1,x2,y2),fill=color,width=2)
    svg.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="1.5" fill="none"/>')
def arrow(x,y,dx,dy):
    p=[(x,y),(x+dx*10-dy*4,y+dy*10+dx*4),(x+dx*10+dy*4,y+dy*10-dx*4)]
    draw.polygon(p,fill=accent)
    svg.append(f'<polygon points="{" ".join(f"{a},{b}" for a,b in p)}" fill="{accent}"/>')
def hdim(x1,x2,edge,y,value):
    line(x1,edge,x1,y+8);line(x2,edge,x2,y+8);line(x1,y,x2,y,accent)
    arrow(x1,y,1,0);arrow(x2,y,-1,0)
    text((x1+x2)/2-35,y+35,value,26,True,accent)
def vdim(y1,y2,edge,x,value):
    line(edge,y1,x+8,y1);line(edge,y2,x+8,y2);line(x,y1,x,y2,accent)
    arrow(x,y1,0,1);arrow(x,y2,0,-1)
    text(x+14,(y1+y2)/2+8,value,26,True,accent)
def image(name,x,y,w,h,crop=False):
    im=Image.open(out/'technical'/data['views'][name]['image']).convert('RGBA')
    if crop:im=im.crop(im.getchannel('A').getbbox())
    from io import BytesIO
    buf=BytesIO();im.save(buf,format='PNG')
    svg.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"/>')
    im=im.resize((round(w),round(h)),Image.Resampling.LANCZOS)
    paper.paste(im,(round(x),round(y)),im)
    if crop:return (x,y,x+w,y+h)
    info=data['views'][name];scale=w/info['ortho_scale']
    lo,hi=info['projected_min'],info['projected_max']
    return (x+w/2+lo[0]*scale,y+h/2-hi[1]*scale,x+w/2+hi[0]*scale,y+h/2-lo[1]*scale)
text(60,72,'HEARTLINE',38,True)
text(60,118,'Pendant dimensions / front, reverse and side',25)
text(1320,76,'MODEL / mm',25,True)
line(60,150,1540,150)
text(100,205,'FRONT / X-Y',23,True)
a=image('front',100,220,650,650*1600/1800)
width,height,depth=data['body']['size']
hdim(a[0],a[2],a[3],a[3]+42,f'{width:.2f}')
vdim(a[1],a[3],a[2],a[2]+38,f'{height:.2f}')
text(950,205,'REVERSE / X-Y',23,True)
image('back',905,220,540,480)
text(925,773,'SIDE / Y-Z',23,True)
side=Image.open(out/'technical/side.png');b=side.getchannel('A').getbbox()
side_h=510*(b[3]-b[1])/(b[2]-b[0])
s=image('side',925,807,510,side_h,True)
vdim(s[1],s[3],s[2],s[2]+32,f'{depth:.2f}')
line(60,928,1540,928)
for x,label,value in [(60,'OVERALL WIDTH',width),(570,'OVERALL HEIGHT',height),(1080,'OVERALL DEPTH',depth)]:
    text(x,970,label,21,True)
    text(x,1010,f'{value:.2f} mm',28)
text(60,1063,'Metal body including the suspension loop. Dimensions exclude the chain.',21,color=muted)
text(60,1096,'Model dimensions in mm / before finishing / not to scale',20,color=muted)
svg.append('</svg>')
(out/'dimensions.svg').write_text(''.join(svg),encoding='utf-8')
paper.save(out/'dimensions-01.png')
paper.save(out/'dimensions-01.webp',quality=94,method=6)
print('ORIGINAL HEARTLINE DIMENSION SHEET COMPLETE')
