from pathlib import Path
import hashlib,json
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
target=WORK/'before-snapshot.json'
assert not target.exists(),'Refusing to overwrite the pre-implementation snapshot.'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
prior=json.loads((ROOT/'work/hotel-transylvania-mobile-bottom-scrolled-review-v1/verification.json').read_text(encoding='utf-8'))
expected=prior['protected_hashes_after']
actual={p:sha(ROOT/p) for p in expected}
assert actual==expected,'Protected-asset mismatch; STOP.'
manifest=json.loads((ROOT/'outputs/the-haunted-realm-navigation-images-approved.json').read_text(encoding='utf-8'))
assert len(manifest['approved_images'])==8
assert manifest['artwork_only_approvals']['Hotel Transylvania']['sha256']==expected['outputs/the-haunted-realm-hotel-transylvania-navigation-image-review-v1.png']
files={p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.rglob('*') if p.is_file()
       and '.git' not in p.relative_to(ROOT).parts and WORK not in p.parents}
title=Image.open(ROOT/'outputs/the-haunted-realm-title-approved.png')
assert title.size==(650,215)
target.write_text(json.dumps({'protected_expected':expected,'protected_before':actual,'files':files,
                              'protected_title_dimensions':list(title.size)},indent=2),encoding='utf-8')
print(json.dumps({'protected_assets_verified':len(actual),'existing_files_snapshotted':len(files),
                  'protected_title_dimensions':list(title.size),'mismatches':[]},indent=2))
