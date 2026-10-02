"""Extract the approved v2 witch at its existing position, without its moon matte.

Only this 80x60 foreground and an inspection image are written. The original
and enhanced full-size images are read-only inputs. No scaling or redesign is
performed. The alpha is inferred solely at the original antialiased outline.
"""
from collections import deque
from pathlib import Path
import json

import numpy as np
from PIL import Image

ROOT = Path(r'C:\Users\DELL\Documents\Codex\2026-09-30\ar')
WORK = ROOT / 'work' / 'background-compositing-v3'
BOX = (1070, 25, 1150, 85)
original = Image.open(ROOT / 'outputs' / 'the-haunted-realm-background-review-v1.png').convert('RGB').crop(BOX)
enhanced = Image.open(ROOT / 'outputs' / 'the-haunted-realm-background-enhanced-review-v2.png').convert('RGB').crop(BOX)
background = np.asarray(original, dtype=np.float64)
observed = np.asarray(enhanced, dtype=np.float64)
h, w = observed.shape[:2]
contrast = (background - observed).mean(axis=2)
channel_max = observed.max(axis=2)

def component(mask, seed):
    """Keep only the 8-connected witch, excluding the distant spire and sky."""
    result = np.zeros(mask.shape, dtype=bool)
    queue = deque([seed])
    while queue:
        y, x = queue.popleft()
        if not (0 <= y < h and 0 <= x < w) or result[y, x] or not mask[y, x]:
            continue
        result[y, x] = True
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx or dy:
                    queue.append((y + dy, x + dx))
    return result

search = np.zeros((h, w), dtype=bool)
search[7:51, 12:69] = True
silhouette = component(search & (contrast > 35) & (channel_max < 190), (30, 40))
assert silhouette[30, 40]
# One pixel of adjacent antialiasing is accepted only where the enhanced pixel
# is darkened relative to the source. This cannot pull in adjacent moon texture.
dilated = np.zeros_like(silhouette)
for dy in (-1, 0, 1):
    for dx in (-1, 0, 1):
        shifted = np.roll(np.roll(silhouette, dy, axis=0), dx, axis=1)
        dilated |= shifted
outline = dilated & search & (contrast > 18) & (channel_max < 210)
mask = component(silhouette | outline, (30, 40))

# The fully dark foreground pixels keep their exact enhanced RGB values. For
# the antialiased perimeter, infer the alpha using nearby opaque witch colors,
# then remove the original moon matte. This retains the source edge while
# allowing the caller to composite it over the untouched original moon.
core = mask & (channel_max <= 90) & ((channel_max - observed.min(axis=2)) <= 40)
core_yx = np.argwhere(core)
assert core_yx.size
alpha = np.zeros((h, w), dtype=np.float64)
foreground = np.zeros((h, w, 3), dtype=np.float64)
for y, x in np.argwhere(mask):
    if core[y, x]:
        alpha[y, x] = 1.0
        foreground[y, x] = observed[y, x]
        continue
    squared_distance = ((core_yx - (y, x)) ** 2).sum(axis=1)
    nearest = core_yx[np.argsort(squared_distance)[:4]]
    local_foreground = np.median(observed[nearest[:, 0], nearest[:, 1]], axis=0)
    direction = background[y, x] - local_foreground
    amount = np.dot(background[y, x] - observed[y, x], direction) / np.dot(direction, direction)
    if amount < 0.14:
        continue
    # Respect the alpha lower bound required for a physically valid RGB color.
    lower_bound = np.maximum((background[y, x] - observed[y, x]) / np.maximum(background[y, x], 1), 0).max()
    amount = float(np.clip(max(amount, lower_bound), 0, 1))
    alpha[y, x] = amount
    foreground[y, x] = np.clip((observed[y, x] - (1 - amount) * background[y, x]) / amount, 0, 255)

rgba = np.concatenate((np.rint(foreground).astype(np.uint8), np.rint(alpha[..., None] * 255).astype(np.uint8)), axis=2)
rgba[rgba[..., 3] == 0, :3] = 0
cutout = Image.fromarray(rgba, 'RGBA')
cutout.save(WORK / 'witch-cutout.png')
composite = Image.alpha_composite(original.convert('RGBA'), cutout).convert('RGB')

checker = np.zeros((h, w, 3), dtype=np.uint8)
for y in range(h):
    for x in range(w):
        checker[y, x] = 218 if ((x // 5 + y // 5) % 2) else 245
transparent_preview = Image.alpha_composite(Image.fromarray(checker, 'RGB').convert('RGBA'), cutout).convert('RGB')
inspection = Image.new('RGB', (w * 16, h * 8))
inspection.paste(transparent_preview.resize((w * 8, h * 8), Image.Resampling.NEAREST), (0, 0))
inspection.paste(composite.resize((w * 8, h * 8), Image.Resampling.NEAREST), (w * 8, 0))
inspection.save(WORK / 'witch-composited-crop-inspection.png')

footprint = rgba[..., 3] > 0
ys, xs = np.nonzero(footprint)
bbox = (int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1))
result = {
    'patch_dimensions': list(cutout.size),
    'patch_placement_xy': list(BOX[:2]),
    'local_alpha_bbox_exclusive': list(bbox),
    'global_alpha_bbox_exclusive': [bbox[0]+BOX[0], bbox[1]+BOX[1], bbox[2]+BOX[0], bbox[3]+BOX[1]],
    'nonzero_alpha_pixels': int(footprint.sum()),
    'opaque_pixels': int((rgba[..., 3] == 255).sum()),
    'soft_edge_pixels': int(((rgba[..., 3] > 0) & (rgba[..., 3] < 255)).sum()),
    'min_nonzero_alpha': int(rgba[..., 3][footprint].min()),
    'exact_v2_rgb_opaque_pixels': int(((rgba[..., 3] == 255) & (rgba[..., :3] == observed).all(axis=2)).sum()),
    'outside_alpha_rgb_and_alpha_all_zero': bool((rgba[~footprint] == 0).all()),
    'edge_contact': bool(footprint[0].any() or footprint[-1].any() or footprint[:, 0].any() or footprint[:, -1].any()),
}
print(json.dumps(result, indent=2))
