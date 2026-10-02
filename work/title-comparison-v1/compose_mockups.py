from pathlib import Path
from PIL import Image
import hashlib
import json
import numpy as np

ROOT = Path(r'C:\Users\DELL\Documents\Codex\2026-09-30\ar')
WORK = ROOT / 'work' / 'title-comparison-v1'
OUT = ROOT / 'outputs'
SOURCE = OUT / 'the-haunted-realm-background-corrected-review-v3.png'
BACKUP = OUT / 'the-haunted-realm-background-review-v1.png'
EXPECTED_SOURCE = '1561627199d2da3412c5d5e49143a6b699201659ad1cee56a38ceb8e96f28c06'
EXPECTED_BACKUP = '63392bf751f4c5518a26e9d82188c3c29cdceb61b9a50c6e8f2f32bb34bc668f'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(SOURCE) == EXPECTED_SOURCE, 'Protected background mismatch; stop.'
assert sha(BACKUP) == EXPECTED_BACKUP, 'Original backup mismatch; stop.'
base = Image.open(SOURCE).convert('RGBA')
assert base.size == (1536, 1024)
base_pixels = np.asarray(base.convert('RGB'))
specs = [(1, 'Ancient Village Sign', (650, 220)), (2, 'Moonlit Stone Inscription', (700, 230)), (3, 'Victorian Manor Emblem', (550, 190))]
report = {'status': 'comparison-mockups-only-no-design-selected', 'source_sha256': EXPECTED_SOURCE, 'background_dimensions': list(base.size), 'options': []}
for number, label, bounds in specs:
    artwork_path = WORK / f'option-{number}-title.png'
    artwork = Image.open(artwork_path).convert('RGBA')
    alpha = np.asarray(artwork.getchannel('A'))
    assert np.any(alpha == 0) and np.any(alpha > 0), f'Option {number} needs transparency.'
    ys, xs = np.where(alpha > 3)
    crop = (int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1)
    artwork = artwork.crop(crop)
    ratio = min(bounds[0] / artwork.width, bounds[1] / artwork.height)
    size = (round(artwork.width * ratio), round(artwork.height * ratio))
    artwork = artwork.resize(size, Image.Resampling.LANCZOS)
    x, y = round(670 - artwork.width/2), 65
    assert x + artwork.width <= 1035, 'Title intrudes into the protected moon display region.'
    overlay = Image.new('RGBA', base.size, (0,0,0,0))
    overlay.alpha_composite(artwork, (x,y))
    mockup = Image.alpha_composite(base, overlay).convert('RGB')
    changed = np.any(np.asarray(mockup) != base_pixels, axis=2)
    support = np.asarray(overlay.getchannel('A')) > 0
    outside_changed = int(np.count_nonzero(changed & ~support))
    assert outside_changed == 0, 'Background altered beyond title overlay.'
    final_path = OUT / f'the-haunted-realm-title-option-{number}-mockup-v1.png'
    assert not final_path.exists(), 'Do not overwrite review mockups.'
    mockup.save(final_path, format='PNG')
    saved = Image.open(final_path).convert('RGB')
    assert np.array_equal(np.asarray(saved), np.asarray(mockup)), 'Saved pixel mismatch.'
    # Inspection only: large view of the title in its actual scene context.
    mockup.crop((max(0,x-25), max(0,y-15), x+size[0]+25, y+size[1]+25)).resize((1200, round(1200*(size[1]+40)/(size[0]+50))), Image.Resampling.LANCZOS).save(WORK / f'option-{number}-context-inspection.png')
    report['options'].append({'number': number, 'label': label, 'file': str(final_path), 'title_bounds': [x,y,x+size[0],y+size[1]], 'display_size': list(size), 'outside_title_overlay_changed_pixels': outside_changed})
assert sha(SOURCE) == EXPECTED_SOURCE and sha(BACKUP) == EXPECTED_BACKUP, 'Protected source files changed.'
report['protected_background_and_backup_unchanged'] = True
(WORK / 'mockup-verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
