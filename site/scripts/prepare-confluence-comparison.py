from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import pypdfium2 as pdfium
root=Path(__file__).resolve().parents[1];folder=root/'.qa/confluence-setting-comparison'
sheet=Image.new('RGB',(1200,420),'#f3f0e9')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
for i,(name,label) in enumerate([('finished','Finished / stones hidden'),('approved-stock','Revised CAD / original stock'),('current-cad','Previous vertical-prong CAD')]):
    image=Image.open(folder/(name+'.png')).convert('RGBA').crop((140,0,860,520))
    image.thumbnail((390,345),Image.Resampling.LANCZOS)
    sheet.paste(image,(i*400+(400-image.width)//2,50),image)
    ImageDraw.Draw(sheet).text((i*400+18,18),label,fill='#202b32',font=font)
ImageDraw.Draw(sheet).text((18,385),'Same front camera and scale. Original models preserved.',fill='#53646c',font=font)
sheet.save(root/'.qa/confluence-prong-comparison.png')
doc=pdfium.PdfDocument(str(root/'public/jewellery/confluence/technical-specification.pdf'))
assert len(doc)==8
doc[2].render(scale=1.4).to_pil().save(root/'.qa/confluence-section-corrected.png')
doc.close()
print('Comparison and corrected sheet rendered')
