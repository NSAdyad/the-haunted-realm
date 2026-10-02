from pathlib import Path
from PIL import Image
import hashlib
import json

ROOT = Path(r'C:\Users\DELL\Documents\Codex\2026-09-30\ar')
WORK = ROOT / 'work' / 'background-compositing-v3'
WORK.mkdir(parents=True, exist_ok=True)
SOURCE = ROOT / 'outputs' / 'the-haunted-realm-background-review-v1.png'
ENHANCED = ROOT / 'outputs' / 'the-haunted-realm-background-enhanced-review-v2.png'
source = Image.open(SOURCE).convert('RGB')
enhanced = Image.open(ENHANCED).convert('RGB')
assert source.size == enhanced.size == (1536, 1024)

regions = {'witch': (1070, 25, 1150, 85), 'window': (245, 35, 300, 115)}
for name, box in regions.items():
    source.crop(box).save(WORK / f'{name}-original-crop.png')
    enhanced.crop(box).save(WORK / f'{name}-enhanced-crop.png')
    source.crop(box).resize(((box[2]-box[0])*8, (box[3]-box[1])*8), Image.Resampling.NEAREST).save(WORK / f'{name}-original-inspection.png')
    enhanced.crop(box).resize(((box[2]-box[0])*8, (box[3]-box[1])*8), Image.Resampling.NEAREST).save(WORK / f'{name}-enhanced-inspection.png')
context = (200, 10, 340, 175)
source.crop(context).resize((560, 660), Image.Resampling.LANCZOS).save(WORK / 'window-context-inspection.png')
manifest = {'source': str(SOURCE), 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'source_size': source.size, 'regions': regions, 'window_context_box': context}
(WORK / 'baseline-and-regions.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest))
