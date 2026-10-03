from pathlib import Path
import ast,hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2];WORK=Path(__file__).resolve().parent
OUT=ROOT/'outputs';ASSETS=ROOT/'assets/navigation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
b=json.loads((WORK/'before-snapshot.json').read_text(encoding='utf-8'))
assert all(sha(ROOT/p)==h for p,h in b['protected_expected'].items())
source=ROOT/'work/navigation-lettering-decision-v1/compose_decision_studies.py'
tree=ast.parse(source.read_text(encoding='utf-8'))
needed={'blank','expand_middle','pane'}
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in needed]
assert {n.name for n in nodes}==needed
frame=Image.open(OUT/'the-haunted-realm-navigation-approved-iron-glass-frame.png').convert('RGBA')
frame=frame.crop(frame.getchannel('A').point(lambda a:255 if a>4 else 0).getbbox())
chains=Image.open(OUT/'the-haunted-realm-navigation-approved-chain-supports.png').convert('RGBA')
chains=chains.crop(chains.getchannel('A').point(lambda a:255 if a>4 else 0).getbbox())
env={'Image':Image,'ImageDraw':ImageDraw,'ImageFont':ImageFont,'np':np,'math':math,'FRAME':frame}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),env)
sizes=[(430,72),(460,72),(288,70),(430,64),(430,44),(460,44),(288,44),(430,52),(460,52),(179,48),(136,52),(160,52)]
states={(430,72),(460,72),(288,70),(179,48),(136,52)}
paths=[ASSETS/f'frame-{w}-{h}-{s}.png' for w,h in sizes for s in (['rest','current'] if (w,h) in states else ['rest'])]
paths +=[ASSETS/'chain-left.png',ASSETS/'chain-right.png',ASSETS/'asset-lineage.json',ROOT/'src/activities.js']
assert not any(p.exists() for p in paths),'Refusing to replace runtime files.'
ASSETS.mkdir(parents=True,exist_ok=True)
manifest={'method':'Existing pure pane authoring definitions and protected material assets only; no new artwork generation','source_authoring_file':source.relative_to(ROOT).as_posix(),'source_authoring_sha256':sha(source),'source_material_hashes':{p:h for p,h in b['protected_expected'].items() if 'iron-glass-frame' in p or 'chain-supports' in p},'derived_files':{}}
for w,h in sizes:
 for s in (['rest','current'] if (w,h) in states else ['rest']):
  im=env['pane'](w,h,s=='current',0)
  p=ASSETS/f'frame-{w}-{h}-{s}.png';im.save(p)
  manifest['derived_files'][p.relative_to(ROOT).as_posix()]={'dimensions':list(im.size),'sha256':sha(p),'existing_pane_variant':0,'current':s=='current'}
base=chains.resize((244,916),Image.Resampling.LANCZOS)
for key,box in [('left',(0,0,66,916)),('right',(178,0,244,916))]:
 p=ASSETS/f'chain-{key}.png';im=base.crop(box);im.save(p)
 manifest['derived_files'][p.relative_to(ROOT).as_posix()]={'dimensions':list(im.size),'sha256':sha(p),'method':'Unchanged existing supports() side extraction'}
(ASSETS/'asset-lineage.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
approved=json.loads((OUT/'the-haunted-realm-navigation-images-approved.json').read_text(encoding='utf-8'))['approved_images']
scenes=json.loads((OUT/'the-haunted-realm-refinement-verification-v3.json').read_text(encoding='utf-8'))['artwork']
slugs=['echoes-of-the-past','the-cursed-quest','the-book-of-shadows','fastest-finger-first','words-of-the-feast','the-phantom-order','door-to-darkness','build-the-haunted-banquet','hotel-transylvania']
stems=['echoes','cursed-quest','book-of-shadows','fastest-finger-first','words-of-the-feast','phantom-order','door-to-darkness','build-the-haunted-banquet','hotel-transylvania']
activities=[]
for i,((name,item),scene,slug,stem) in enumerate(zip(approved.items(),scenes,slugs,stems)):
 assert sha(ROOT/item['file'])==item['sha256']
 scene_path=Path(scene['source_file']);assert sha(scene_path)==scene['source_sha256']
 t34=f'work/{stem}-navigation-image-review-v1/{stem}-thumbnail-34-review.png'
 t38=f'work/{stem}-navigation-image-review-v1/{stem}-thumbnail-38-review.png'
 assert (ROOT/t34).is_file() and (ROOT/t38).is_file()
 activities.append({'id':slug,'name':name,'navImage34':t34,'navImage38':t38,'scene':scene_path.relative_to(ROOT).as_posix(),'sceneBox':scene['display_box'],'lettering':f'work/activity-nine-refinement-v3/name-{i+1:02d}-rest.png','letteringFocus':f'work/activity-nine-refinement-v3/name-{i+1:02d}-focus.png','implementationState':'shell'})
assert len(activities)==len(approved)
src=ROOT/'src';src.mkdir(exist_ok=True)
(src/'activities.js').write_text('// Shared destination registry. Add an approved entry here to extend the same website.\nexport const ACTIVITIES = '+json.dumps(activities,indent=2,ensure_ascii=False)+';\n\nexport const GLOBAL_ASSETS = '+json.dumps({'background':'outputs/the-haunted-realm-background-corrected-review-v3.png','title':'outputs/the-haunted-realm-title-approved.png'},indent=2)+';\n',encoding='utf-8')
assert all(sha(ROOT/p)==h for p,h in b['protected_expected'].items())
print(json.dumps({'runtime_material_files':len(manifest['derived_files']),'registry_destinations':[a['name'] for a in activities],'protected_sources_unchanged':True},indent=2))
