from pathlib import Path
import json
import numpy as np
from PIL import Image

WORK=Path(__file__).resolve().parent
results=[]
for width,run in [(1920,'presentation-run-2'),(1366,'presentation-run-3-laptop-baseline')]:
    originals=sorted(WORK.glob(f'before-rail-{width}-*.png'))
    assert len(originals)==9,'Expected exactly nine original rail references.'
    for original in originals:
        candidate=WORK/run/original.name.replace('before-rail-','after-rail-')
        assert candidate.is_file(),f'After screenshot missing: {candidate.name}'
        a=np.array(Image.open(original).convert('RGBA'))
        b=np.array(Image.open(candidate).convert('RGBA'))
        assert a.shape==b.shape,'Rail dimensions changed.'
        changed=int(np.count_nonzero(np.any(a!=b,axis=2)))
        results.append({'width':width,'original':original.name,'candidate':candidate.relative_to(WORK).as_posix(),'changed_pixels':changed,'status':'PASS' if changed==0 else 'FAIL'})
result={'tests':results,'passed':sum(r['status']=='PASS' for r in results),'failed':sum(r['status']=='FAIL' for r in results),'errors':[],'badRequests':[],'method':'Pixel-by-pixel RGBA comparison of same-route direct-load rail screenshots; all18 original images remain unchanged.'}
(WORK/'rail-pixel-comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'passed':result['passed'],'failed':result['failed'],'total_changed_pixels':sum(r['changed_pixels'] for r in results)}))
assert result['failed']==0,'TEST FAILURE: report rail differences before any correction.'
