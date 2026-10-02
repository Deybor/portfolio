"""Encode ivory-background cover assets and inspect their fixed diagonal composition."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
root=Path(__file__).resolve().parents[1]
pieces=[('confluence','render-01-environment.webp'),('iced-out-ring','render-01-gallery.webp'),('heartline-pendant','render-01-studio.webp')]
paper=(239,232,220)
sheet=Image.new('RGB',(900,330),paper)
for index,(slug,beauty_name) in enumerate(pieces):
    folder=root/'public/jewellery'/slug
    original=Image.open(folder/'cover-wireframe.png').convert('RGBA')
    white=Image.new('RGBA',original.size,paper+(255,));white.alpha_composite(original)
    white.convert('RGB').save(folder/'cover-wireframe.webp',quality=95,method=6)
    beauty=Image.open(folder/beauty_name).convert('RGB')
    stage=Image.new('RGB',(900,900),(30,26,22))
    image=ImageOps.fit(beauty,(900,900),Image.Resampling.LANCZOS)
    stage.paste(image,((900-image.width)//2,(900-image.height)//2))
    wire_stage=Image.new('RGB',(900,900),paper)
    image=ImageOps.fit(white.convert('RGB'),(900,900),Image.Resampling.LANCZOS)
    wire_stage.paste(image,((900-image.width)//2,(900-image.height)//2))
    mask=Image.new('L',(900,900),0)
    ImageDraw.Draw(mask).polygon([(899,324),(899,899),(0,899),(0,720)],fill=255)
    stage.paste(wire_stage,(0,0),mask)
    ImageDraw.Draw(stage).line([(0,720),(899,324)],fill=(203,191,174),width=2)
    stage.save(root/'.qa'/f'{slug}-cover-composition.png')
    sheet.paste(stage.resize((300,300),Image.Resampling.LANCZOS),(index*300,0))
    ImageDraw.Draw(sheet).text((index*300+12,309),slug,fill=(30,26,22))
sheet.save(root/'.qa/cover-compositions.png')
print('Three cover wireframes encoded and cover compositions prepared')
