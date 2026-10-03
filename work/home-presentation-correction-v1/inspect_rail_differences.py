from pathlib import Path
import json
import numpy as np
from PIL import Image
WORK=Path(__file__).resolve().parent
items=json.loads((WORK/'rail-pixel-comparison.json').read_text(encoding='utf-8'))['tests']
for item in items:
    if item['changed_pixels']:
        a=np.array(Image.open(WORK/item['original']).convert('RGBA'))
        b=np.array(Image.open(WORK/item['candidate']).convert('RGBA'))
        mask=np.any(a!=b,axis=2)
        yy,xx=np.where(mask)
        print(json.dumps({'original':item['original'],'changed':item['changed_pixels'],'bbox':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],'maxChannelDiff':int(np.abs(a.astype(int)-b.astype(int)).max()),'meanAbsoluteChannelDifference':float(np.abs(a.astype(int)-b.astype(int)).mean())}))
