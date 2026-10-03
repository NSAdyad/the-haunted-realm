"""Non-mutating source verification; writes separate audit records only."""
from pathlib import Path
import hashlib
import json
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()
before = json.loads((WORK/'before-snapshot.json').read_text(encoding='utf-8'))
expected = before['protected_expected']
protected = {name:sha(ROOT/name) for name in expected}
assert protected == expected, 'Protected hash mismatch: STOP.'
allowed = {
    'AGENTS.md', 'docs/the-haunted-realm-development-workflow.md',
    'outputs/the-haunted-realm-navigation-current-design-status.md',
    'outputs/the-haunted-realm-navigation-images-approved.json'
}
missing = [name for name in before['files'] if not (ROOT/name).is_file()]
changed = [name for name,original in before['files'].items() if (ROOT/name).is_file() and sha(ROOT/name)!=original]
assert not missing, 'Existing files missing: STOP.'
assert set(changed)==allowed, f'Unexpected existing-file changes: {set(changed)^allowed}'
assert all(sha(ROOT/name)==original for name,original in before['files'].items() if name.endswith(('.png','.jpeg','.jpg','.py','.ps1'))), 'Existing artwork/review/script changed.'
manifest = json.loads((ROOT/'outputs/the-haunted-realm-navigation-images-approved.json').read_text(encoding='utf-8'))
assert len(manifest['approved_images']) == 9
for name,record in manifest['approved_images'].items():
    assert record['status']=='APPROVED / PROTECTED — NAVIGATION IMAGE'
    assert sha(ROOT/record['file'])==record['sha256']
    assert Image.open(ROOT/record['file']).size==(1254,1254)

registry = (ROOT/'src/activities.js').read_text(encoding='utf-8')
activities = json.loads(re.search(r'export const ACTIVITIES = (\[.*?\]);',registry,re.S).group(1))
globals_ = json.loads(re.search(r'export const GLOBAL_ASSETS = (\{.*?\});',registry,re.S).group(1))
paths = set(globals_.values())
for activity in activities:
    paths.update(activity[key] for key in ('navImage34','navImage38','scene','lettering','letteringFocus'))
assert [entry['name'] for entry in activities]==list(manifest['approved_images'])
for match in re.findall(r"url\(['\"]?([^)'\"]+)", (ROOT/'src/styles.css').read_text(encoding='utf-8')):
    paths.add((ROOT/'src'/match).resolve().relative_to(ROOT).as_posix())
paths.update(['index.html','src/app.js','src/activities.js','src/styles.css'])
for name in paths:
    current=ROOT
    for part in Path(name).parts:
        assert part in {child.name for child in current.iterdir()}, f'Case/path mismatch: {name}'
        current=current/part
    assert current.is_file(), f'Missing runtime asset: {name}'
for activity in activities:
    for key,size in [('navImage34',34),('navImage38',38)]:
        assert Image.open(ROOT/activity[key]).size==(size,size)
lineage=json.loads((ROOT/'assets/navigation/asset-lineage.json').read_text(encoding='utf-8'))
report = {
    'protected_assets_verified':len(protected), 'protected_hashes_after':protected,
    'all_protected_hashes_unchanged':True, 'approved_navigation_images':9,
    'pre_existing_files':len(before['files']), 'pre_existing_unchanged':len(before['files'])-len(changed),
    'existing_documentation_changes_only':changed, 'missing_pre_existing_files':missing,
    'all_pre_existing_images_reviews_scripts_unchanged':True,
    'exact_case_runtime_paths_verified':len(paths), 'runtime_paths':sorted(paths),
    'runtime_path_hashes':{name:sha(ROOT/name) for name in sorted(paths)},
    'title_source_dimensions':list(Image.open(ROOT/globals_['title']).size),
    'activity_names':[a['name'] for a in activities],
    'new_files':sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts and p.relative_to(ROOT).as_posix() not in before['files']),
    'navigation_lineage_record':'assets/navigation/asset-lineage.json'
}
(WORK/'final-source-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({key:value for key,value in report.items() if key not in ('protected_hashes_after','runtime_path_hashes','runtime_paths','new_files')},indent=2))
