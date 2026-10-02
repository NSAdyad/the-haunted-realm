from pathlib import Path
from PIL import Image
import hashlib
import json
import shutil
import numpy as np

ROOT = Path(r'C:\Users\DELL\Documents\Codex\2026-09-30\ar')
OUT = ROOT / 'outputs'
WORK = ROOT / 'work' / 'title-protection'
WORK.mkdir(parents=True, exist_ok=True)
SOURCE = ROOT / 'work' / 'title-comparison-v1' / 'option-1-title.png'
BACKGROUND = OUT / 'the-haunted-realm-background-corrected-review-v3.png'
REFERENCE = OUT / 'the-haunted-realm-title-option-1-centred-review-v2.png'
BACKUP_BG = OUT / 'the-haunted-realm-background-review-v1.png'
FROZEN = OUT / 'the-haunted-realm-title-approved.png'
BACKUP_ART = OUT / 'the-haunted-realm-title-original-artwork-backup.png'
EXPECTED = {
    SOURCE: 'd40b8107d55723cd6976c880905564458dca17082d55aaaf7f561d6dc6d3f7c1',
    BACKGROUND: '1561627199d2da3412c5d5e49143a6b699201659ad1cee56a38ceb8e96f28c06',
    REFERENCE: '1a4b8c14c4229b0c2e68db47086b0a741c667930b16e531dcb2455905a0c7942',
    BACKUP_BG: '63392bf751f4c5518a26e9d82188c3c29cdceb61b9a50c6e8f2f32bb34bc668f',
}
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
for path, expected in EXPECTED.items():
    assert sha(path) == expected, f'Protected input mismatch: {path}'
assert not FROZEN.exists() and not BACKUP_ART.exists(), 'Do not overwrite assets.'

# Freeze the already-approved rendered title; do not change its appearance.
artwork = Image.open(SOURCE).convert('RGBA')
alpha = np.asarray(artwork.getchannel('A'))
ys, xs = np.where(alpha > 3)
crop = (int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1)
rendered = artwork.crop(crop).resize((650, 215), Image.Resampling.LANCZOS)
base = Image.open(BACKGROUND).convert('RGBA')
overlay = Image.new('RGBA', base.size, (0,0,0,0))
overlay.alpha_composite(rendered, (443,65))
reconstructed_reference = Image.alpha_composite(base, overlay).convert('RGB')
approved_reference = Image.open(REFERENCE).convert('RGB')
assert np.array_equal(np.asarray(reconstructed_reference), np.asarray(approved_reference)), 'Rendered title does not exactly reproduce approved reference.'
rendered.save(FROZEN, format='PNG')
assert np.array_equal(np.asarray(Image.open(FROZEN).convert('RGBA')), np.asarray(rendered))
shutil.copy2(SOURCE, BACKUP_ART)
assert sha(BACKUP_ART) == EXPECTED[SOURCE]
for path, expected in EXPECTED.items():
    assert sha(path) == expected, f'Protected input changed: {path}'
record = {
    'status': 'APPROVED / PROTECTED',
    'approval': 'User explicitly said TITLE APPROVED after visual inspection.',
    'title': 'THE HAUNTED REALM',
    'design': 'Ancient Village Sign',
    'frozen_asset': str(FROZEN),
    'frozen_asset_sha256': sha(FROZEN),
    'dimensions': [650,215],
    'position_on_1536x1024_background': [443,65],
    'bounds': [443,65,1093,280],
    'horizontal_centre': 768,
    'original_artwork_backup': str(BACKUP_ART),
    'original_artwork_backup_sha256': sha(BACKUP_ART),
    'approved_reference': str(REFERENCE),
    'approved_reference_sha256': EXPECTED[REFERENCE],
    'approved_reference_exact_pixel_match': True,
    'all_existing_protected_assets_unchanged': True,
    'website_implementation_authorized': False,
}
(WORK / 'title-protection-verification.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
print(json.dumps(record, indent=2))
