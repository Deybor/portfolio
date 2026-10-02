"""Prepare web copies of supplied renders without changing the source files."""
from pathlib import Path
from PIL import Image
import json
import shutil

root = Path(__file__).resolve().parents[1]
source = Path(r'C:\Users\Master\Documents\blender\blender filesss\troo\new\cad-3d print')
target = root / 'public' / 'objects'
projects = [
    ('zenith-cup', 'The Zenith Cup', 'The Zenith Cup.blend', ['preview1.png', 'preview2.png', 'preview3.png', 'preview8.png', 'preview4.png'], ['preview6 .png', 'preview7.png']),
    ('world', 'World', 'World.blend', ['World.png', 'World2.png', 'World3.png', 'World4.png', 'world (2).png'], []),
    ('top-campus-ministry', 'Top Campus Ministry', 'Top Campus Ministry.blend', ['Top Campus Ministry.png', 'Top Campus Ministry2.png', 'Top Campus Ministry3.png'], []),
    ('top-zone-trophy', 'Top Zone Trophy', 'Top Zone Trouphy.blend', ['Top Zone Trouphy.png', 'Top Zone Trouphy 2.png'], []),
    ('bible-projects-for-programs', 'Bible Projects for Programs', 'Bilble Projects for Programs.blend', ['Bilble Projects for Programs.png', 'Bilble Projects for Programs 2.png'], []),
    ('projects-and-programs', 'Projects & Programs', 'Project & Programs.blend', ['Project & Programs.png', 'Project & Programs 2.png'], []),
    ('individual-category', 'Individual Category', 'Individual Category.blend', ['Individual Category.png', 'Individual Category 2.png'], []),
    ('tuff', 'Tuff', 'tuff.blend', ['tuff.png', 'tuff (2).png', 'tuff (3).png'], []),
    ('vit', 'Vit', 'vit.blend', ['vit.png', 'vit (2).png', 'vit (3).png'], []),
    ('medal', 'Medal', 'medal.blend', ['medal.png'], []),
]
manifest = []
for slug, title, model, renders, wires in projects:
    folder = target / slug
    folder.mkdir(parents=True, exist_ok=True)
    views = []
    for kind, names in [('final', renders), ('wireframe', wires)]:
        for index, name in enumerate(names, 1):
            original = source / name
            stem = f'{kind}-{index:02}'
            shutil.copy2(original, folder / f'{stem}.png')
            with Image.open(original) as img:
                width, height = img.size
                web = img.convert('RGB')
                web.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
                web.save(folder / f'{stem}.webp', quality=88, method=6)
                if kind == 'final' and index == 1:
                    card = img.convert('RGB')
                    card.thumbnail((800, 800), Image.Resampling.LANCZOS)
                    card.save(folder / 'card.webp', quality=86, method=6)
            views.append({'kind': kind, 'index': index, 'source': name, 'width': width, 'height': height, 'image': f'/objects/{slug}/{stem}.webp', 'full': f'/objects/{slug}/{stem}.png'})
    manifest.append({'slug': slug, 'title': title, 'modelSource': model, 'card': f'/objects/{slug}/card.webp', 'views': views})

shutil.copy2(source / 'Award designs.pdf', target / 'award-designs.pdf')
sketches = Path(r'C:\Users\Master\Documents\itura\tmp\trophy-inspection')
for page in [2, 3, 4, 7, 8]:
    with Image.open(sketches / f'award-{page}.png') as img:
        web = img.convert('RGB')
        web.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        web.save(target / f'award-sketches-{page}.webp', quality=90, method=6)

(root / 'src' / 'lib' / 'printed-objects.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
(root / 'docs' / 'printed-objects-sources.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps({'projects': len(manifest), 'views': sum(len(p['views']) for p in manifest), 'sourceFilesUnchanged': True}))
