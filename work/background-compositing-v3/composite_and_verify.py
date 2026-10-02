from pathlib import Path
from PIL import Image
import hashlib
import json
import numpy as np

ROOT = Path(r'C:\Users\DELL\Documents\Codex\2026-09-30\ar')
WORK = ROOT / 'work' / 'background-compositing-v3'
OUTPUT = ROOT / 'outputs' / 'the-haunted-realm-background-corrected-review-v3.png'
REPORT = ROOT / 'outputs' / 'the-haunted-realm-background-verification-v3.json'
SOURCE = ROOT / 'outputs' / 'the-haunted-realm-background-review-v1.png'
baseline = json.loads((WORK / 'baseline-and-regions.json').read_text(encoding='utf-8'))
hash_before = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
assert hash_before == baseline['source_sha256'], 'Original file changed since baseline.'
assert not OUTPUT.exists(), 'Do not overwrite an existing review candidate.'
original = Image.open(SOURCE).convert('RGB')
original_pixels = np.asarray(original).copy()
result = original.copy()

# Reuse only the extracted witch silhouette at its existing scale/location.
witch = Image.open(WORK / 'witch-cutout.png').convert('RGBA')
witch_box = tuple(baseline['regions']['witch'])
assert witch.size == (witch_box[2]-witch_box[0], witch_box[3]-witch_box[1])
moon = original.crop(witch_box).convert('RGBA')
result.paste(Image.alpha_composite(moon, witch).convert('RGB'), witch_box[:2])

# Use only the generated apparition's alpha silhouette, not any generated scene.
presence = Image.open(WORK / 'window-presence-generated.png').convert('RGBA')
alpha = np.asarray(presence.getchannel('A'))
assert alpha.min() == 0 and np.any(alpha > 0), 'Presence must be isolated on transparency.'
ys, xs = np.where(alpha > 8)
presence = presence.crop((int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1))
presence = presence.resize((18, 35), Image.Resampling.LANCZOS)
window_box = tuple(baseline['regions']['window'])
window = original.crop(window_box)
window_pixels = np.asarray(window).astype(np.float64)
presence_mask = Image.new('L', window.size, 0)
presence_mask.paste(presence.getchannel('A'), (26, 31))
figure_alpha = np.asarray(presence_mask).astype(np.float64) / 255.0

# The source glass has warm, bright pixels; dark frames/mullions remain unedited.
red, green, blue = [window_pixels[:, :, i] for i in range(3)]
glass = (red >= 185) & (green >= 90) & (red > green*1.1) & (red > blue*1.5)
yy, xx = np.indices(glass.shape)
glass &= (xx >= 24) & (xx <= 44) & (yy >= 27) & (yy <= 68)
strength = figure_alpha * glass.astype(np.float64) * 0.43
shadow_colour = np.array([43.0, 24.0, 19.0])
composited_window = np.rint(window_pixels * (1-strength[:, :, None]) + shadow_colour * strength[:, :, None]).clip(0, 255).astype(np.uint8)
result.paste(Image.fromarray(composited_window), window_box[:2])

result_pixels = np.asarray(result)
changed = np.any(result_pixels != original_pixels, axis=2)
allowed = np.zeros(changed.shape, dtype=bool)
for box in (witch_box, window_box):
    x0, y0, x1, y1 = box
    allowed[y0:y1, x0:x1] = True
outside_changed = int(np.count_nonzero(changed & ~allowed))
assert outside_changed == 0, 'Pixels outside approved regions changed.'
local_window_changed = np.any(composited_window != np.asarray(window), axis=2)
assert not np.any(local_window_changed & ~glass), 'A window frame/divider was changed.'
assert np.count_nonzero(local_window_changed) > 0, 'Window addition is absent.'
result.save(OUTPUT, format='PNG')
saved = Image.open(OUTPUT).convert('RGB')
assert saved.size == original.size == (1536, 1024)
assert np.array_equal(np.asarray(saved), result_pixels), 'Saved PNG changed decoded pixels.'
hash_after = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
assert hash_after == hash_before, 'Original source file was altered.'

def region_report(name, box):
    x0, y0, x1, y1 = box
    local = changed[y0:y1, x0:x1]
    ly, lx = np.where(local)
    return {'region': list(box), 'changed_pixels': int(local.sum()), 'actual_change_bbox': [int(lx.min()+x0), int(ly.min()+y0), int(lx.max()+x0+1), int(ly.max()+y0+1)] if len(lx) else None}

report = {
    'status': 'review-candidate-not-approved',
    'output': str(OUTPUT),
    'dimensions': list(saved.size),
    'source_sha256_before': hash_before,
    'source_sha256_after': hash_after,
    'original_file_unchanged': hash_before == hash_after,
    'outside_approved_regions_changed_pixels': outside_changed,
    'outside_approved_regions_exact_pixel_match': outside_changed == 0,
    'witch': region_report('witch', witch_box),
    'window': region_report('window', window_box),
    'window_frame_and_dividers_changed_pixels': int(np.count_nonzero(local_window_changed & ~glass)),
    'saved_png_lossless_pixel_match': True,
    'method': 'original pixels plus extracted existing witch and generated presence alpha, bounded compositing',
}
REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
context_box = tuple(baseline['window_context_box'])
saved.crop(context_box).resize((560, 660), Image.Resampling.LANCZOS).save(WORK / 'window-corrected-context-inspection.png')
saved.crop(witch_box).resize((640, 480), Image.Resampling.NEAREST).save(WORK / 'witch-corrected-inspection.png')
print(json.dumps(report, indent=2))
