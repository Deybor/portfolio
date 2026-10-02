"""Package supplied portfolio images, preserving originals and their provenance."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import shutil, json, hashlib

root = Path(__file__).resolve().parents[1]
source = Path(r'C:\Users\Master\Documents\itura\PORFOLIO PIECES')
jobs = {
    'heartline-pendant': [
        ('BlenderKit_Beauty/Heartline_Studio.png', 'render-01-studio'),
    ],
    'confluence': [
        ('BlenderKit_Beauty/Confluence_Environment.png', 'render-01-environment'),
        (str(root / 'assets/source/confluence-studio.png'), 'render-02-studio'),
        ('Confluence_First_Ring/Renders_and_Dimensions/Beauty_Setting.png', 'render-03'),
        ('Confluence_First_Ring/Renders_and_Dimensions/Wireframe_Final.png', 'wireframe-01'),
        ('Confluence_First_Ring/Renders_and_Dimensions/Wireframe_Setting.png', 'wireframe-02'),
        ('Confluence_First_Ring/Renders_and_Dimensions/Specification_Preview.png', 'dimensions-01'),
        ('Confluence_First_Ring/SVG_Concept_Drawings/Confluence_Concept_Sketches_v02_Preview.png', 'sketches-01'),
    ],
    'iced-out-ring': [
        ('BlenderKit_Beauty/Iced_Ring_Gallery.png', 'render-01-gallery'),
        ('Ring_Iced_Out_03/Ring_Beauty_Angle.png', 'render-01'),
        ('Ring_Iced_Out_03/Ring_Base_CAD_Drawings.png', 'dimensions-01'),
    ],
}
audit, contact = [], []
for slug, files in jobs.items():
    out = root / 'public/jewellery' / slug
    out.mkdir(parents=True, exist_ok=True)
    for relative, name in files:
        if slug == 'confluence' and name.startswith('wireframe') and (root / 'docs/confluence-straight-prongs.json').exists():
            continue
        if name == 'dimensions-01' and (root / 'docs/jewellery-drawing-refinement.json').exists():
            continue
        original = source / relative
        shutil.copy2(original, out / (name + '.png'))
        with Image.open(original) as image:
            image.load()
            size = image.size
            preview = image.convert('RGB')
            preview.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
            preview.save(out / (name + '.webp'), quality=90, method=6)
            if (slug == 'confluence' and name == 'render-01-environment') or (slug == 'iced-out-ring' and name == 'render-01-gallery'):
                card = image.convert('RGB')
                card.thumbnail((900, 900), Image.Resampling.LANCZOS)
                card.save(out / 'card.webp', quality=90, method=6)
            contact.append((slug + ' / ' + name, ImageOps.contain(image.convert('RGB'), (320, 300))))
        audit.append({'source': str(original), 'destination': str(out / (name + '.png')), 'size': size,
                      'sha256': hashlib.sha256(original.read_bytes()).hexdigest(),
                      'preserved': original.read_bytes() == (out / (name + '.png')).read_bytes()})
extras = [
    ('Confluence_First_Ring/Renders_and_Dimensions/Confluence_Specification.pdf', 'confluence/specification.pdf'),
    ('Confluence_First_Ring/SVG_Concept_Drawings/Confluence_Concept_Sketches_v02.svg', 'confluence/sketches.svg'),
    ('Ring_Iced_Out_03/Ring_Base_CAD_Drawings.svg', 'iced-out-ring/dimensions.svg'),
]
for relative, target in extras:
    if target.endswith('dimensions.svg') and (root / 'docs/jewellery-drawing-refinement.json').exists():
        continue
    shutil.copy2(source / relative, root / 'public/jewellery' / target)
pendant = root / 'public/jewellery/heartline-pendant/render-01.png'
if pendant.exists():
    with Image.open(pendant) as image:
        preview = image.convert('RGB')
        preview.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
        preview.save(pendant.with_suffix('.webp'), quality=90, method=6)
        preview.thumbnail((900, 900), Image.Resampling.LANCZOS)
        preview.save(pendant.parent / 'card.webp', quality=90, method=6)
        audit.append({'source': str(pendant), 'size': image.size, 'method': 'Actual saved-scene Blender render'})
sheet = Image.new('RGB', (320 * 4, 335 * ((len(contact) + 3) // 4)), '#dedbd5')
draw = ImageDraw.Draw(sheet)
for n, (label, thumb) in enumerate(contact):
    x, y = (n % 4) * 320, (n // 4) * 335
    sheet.paste(thumb, (x + (320 - thumb.width) // 2, y))
    draw.text((x + 8, y + 305), label, fill='#202020')
sheet.save(root / '.qa/jewellery-pieces-inspection.jpg')
(root / 'docs/jewellery-pieces-assets.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
print(json.dumps([{'source': x['source'], 'size': x['size']} for x in audit if 'size' in x]))
