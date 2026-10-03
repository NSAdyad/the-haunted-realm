from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest().upper()
expected=json.loads((ROOT/'work/local-integrated-shell-v1/before-snapshot.json').read_text(encoding='utf-8'))['protected_expected']
nav=json.loads((ROOT/'outputs/the-haunted-realm-navigation-approved-assets.json').read_text(encoding='utf-8'))
for asset in nav['assets']:
    expected['outputs/'+asset['file']]=asset['sha256']
images=json.loads((ROOT/'outputs/the-haunted-realm-navigation-images-approved.json').read_text(encoding='utf-8'))
for asset in images['approved_images'].values():expected[asset['file']]=asset['sha256']
actual={name:sha(ROOT/name) for name in expected}
assert actual==expected,'Protected mismatch: STOP.'
mode=sys.argv[1]
snapshot=WORK/'before-snapshot.json'
if mode=='pre':
    assert not snapshot.exists(),'Do not overwrite the baseline.'
    files={p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts and WORK not in p.parents}
    source={name:(ROOT/name).read_text(encoding='utf-8') for name in ['index.html','src/app.js','src/activities.js','src/styles.css']}
    result={'files':files,'protected_expected':expected,'protected_before':actual,'source_before':source}
    snapshot.write_text(json.dumps(result,indent=2),encoding='utf-8')
else:
    before=json.loads(snapshot.read_text(encoding='utf-8'))
    missing=[name for name in before['files'] if not (ROOT/name).is_file()]
    changed=[name for name,h in before['files'].items() if (ROOT/name).is_file() and sha(ROOT/name)!=h]
    visual_changes=[name for name in changed if name.lower().endswith(('.png','.jpg','.jpeg'))]
    assert not missing and not visual_changes,'Existing file/visual regression: STOP.'
    result={'protected_count':len(actual),'protected_hashes_after':actual,'all_protected_unchanged':True,'pre_existing_count':len(before['files']),'pre_existing_changed':changed,'pre_existing_missing':missing,'existing_image_changes':visual_changes}
    (WORK/'protected-and-source-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'mode':mode,'protected_count':len(actual),'all_protected_unchanged':True,'pre_existing_count':len(result.get('files',{})) if mode=='pre' else result['pre_existing_count'],'changed':result.get('pre_existing_changed',[])},indent=2))
