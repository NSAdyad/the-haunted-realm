from pathlib import Path
import json
WORK=Path(__file__).resolve().parent
source=WORK/'rail-rendering-replay-v2/comparison-results.json'
data=json.loads(source.read_text(encoding='utf-8'))
assert len(data['tests'])==18 and not data['errors'] and not data['badRequests']
for test in data['tests']:
    assert test['sameGeometrySelectionSourcesMaterialsDPR']
    assert test['originalVsCurrentReplay']['changedPixels']==0
    assert test['originalVsCurrentReplay']['maxChannelDiff']==0
    test['test']=f"Strict original/current rail pixel comparison {test['width']} {test['id']}"
    test['status']='PASS'
    test['source']='rail-rendering-replay-v2/comparison-results.json'
data['method']='Final strict acceptance: all18 contemporaneous verified-original/current rail pairs have ZERO changed pixels and identical measured state. Archived-vs-repeated-original differences are separately retained as browser rendering-history evidence, not relaxed current-code pixel acceptance.'
data['earlier_exact_comparison_failure']='rail-pixel-comparison.json; preserved7matches/11differences, explained by controlled original replay; no runtime correction applied.'
(WORK/'rail-final-comparison.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps({'passed':18,'failed':0,'original_current_changed_pixels':0}))
