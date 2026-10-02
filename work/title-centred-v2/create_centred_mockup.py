from pathlib import Path
from PIL import Image
import hashlib
import json
import numpy as np

ROOT = Path(r'C:\Users\DELL\Documents\Codex\2026-09-30\ar')
WORK = ROOT / 'work' / 'title-centred-v2'
WORK.mkdir(parents=True, exist_ok=True)
OUT = ROOT / 'outputs'
SOURCE = OUT / 'the-haunted-realm-background-corrected-review-v3.png'
BACKUP = OUT / 'the-haunted-realm-background-review-v1.png'
ART = ROOT / 'work' / 'title-comparison-v1' / 'option-1-title.png'
FINAL = OUT / 'the-haunted-realm-title-option-1-centred-review-v2.png'
EXPECTED_SOURCE = '1561627199d2da3412c5d5e49143a6b699201659ad1cee56a38ceb8e96f28c06'
EXPECTED_BACKUP = '63392bf751f4c5518a26e9d82188c3c29cdceb61b9a50c6e8f2f32bb34bc668f'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert sha(SOURCE) == EXPECTED_SOURCE, 'Protected background mismatch; stop.'
assert sha(BACKUP) == EXPECTED_BACKUP, 'Original backup mismatch; stop.'
art_hash_before = sha(ART)
assert not FINAL.exists(), 'Do not overwrite an existing review image.'
base = Image.open(SOURCE).convert('RGBA')
assert base.size == (1536, 1024)
artwork = Image.open(ART).convert('RGBA')
alpha = np.asarray(artwork.getchannel('A'))
ys, xs = np.where(alpha > 3)
crop = (int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1)
artwork = artwork.crop(crop).resize((650, 215), Image.Resampling.LANCZOS)
x, y = (base.width-artwork.width)//2, 65
assert x == 443 and x+artwork.width == 1093
assert x == base.width-(x+artwork.width), 'Unequal horizontal margins.'
overlay = Image.new('RGBA', base.size, (0,0,0,0))
overlay.alpha_composite(artwork, (x,y))
mockup = Image.alpha_composite(base, overlay).convert('RGB')
changed = np.any(np.asarray(mockup) != np.asarray(base.convert('RGB')), axis=2)
support = np.asarray(overlay.getchannel('A')) > 0
assert np.count_nonzero(changed & ~support) == 0, 'Background changed beyond title overlay.'
mockup.save(FINAL, format='PNG')
saved = Image.open(FINAL).convert('RGB')
assert np.array_equal(np.asarray(saved), np.asarray(mockup))
assert sha(SOURCE) == EXPECTED_SOURCE and sha(BACKUP) == EXPECTED_BACKUP
assert sha(ART) == art_hash_before, 'Existing title artwork was changed.'
report = {
    'status': 'selected-option-1-centred-review-only-awaiting-user-inspection',
    'background_dimensions': list(base.size),
    'title_dimensions': list(artwork.size),
    'title_bounds': [x,y,x+artwork.width,y+artwork.height],
    'title_horizontal_centre': x+artwork.width/2,
    'background_horizontal_centre': base.width/2,
    'equal_horizontal_margins': x,
    'previous_title_bounds': [345,65,995,280],
    'horizontal_shift_pixels': x-345,
    'title_design_and_scale_unchanged': True,
    'protected_background_sha256': EXPECTED_SOURCE,
    'protected_background_and_backup_unchanged': True,
    'outside_title_overlay_changed_pixels': int(np.count_nonzero(changed & ~support)),
    'existing_artwork_sha256': art_hash_before,
    'output': str(FINAL),
}
(WORK / 'centred-mockup-verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
