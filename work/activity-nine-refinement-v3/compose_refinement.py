"""Unapproved static raster review; no website implementation."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from type_art import NAMES,LINES,make_name

ROOT=Path(__file__).resolve().parents[2];WORK=Path(__file__).resolve().parent
OLD=ROOT/'work/activity-nine-review-v1';OUT=ROOT/'outputs'
PRIOR=json.loads((OUT/'the-haunted-realm-nine-destinations-verification-v2.json').read_text(encoding='utf-8'))
EXPECTED=PRIOR['protected_hashes_after']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def verify():
 actual={n:sha(OUT/n) for n in EXPECTED}
 bad=[n for n,h in actual.items() if h!=EXPECTED[n]]
 if bad:raise RuntimeError('Protected source mismatch; stop: '+', '.join(bad))
 return actual
BEFORE=verify()
BASE=Image.open(OUT/'the-haunted-realm-navigation-b-home-redesign-review-v3-final.png').convert('RGBA')
SIZE=BASE.size;assert SIZE==(1536,1024)
base=np.asarray(BASE.convert('RGB'));prior_page=Image.open(OUT/'the-haunted-realm-nine-destinations-rest-review-v2.png').convert('RGB')
CX=[285,768,1251];TOP=[309,541,770];STAGGER=[0,7,-3,5,-2,8,-1,4,0]
NAME_Y=[507,739,973];MAX_SCENE=[(420,172)]*8+[(438,176)]
REFINED={0,2,6,8};RETAINED={1,3,4,5,7}
def blank():return Image.new('RGBA',SIZE,(0,0,0,0))
def font(size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf' if bold else 'C:/Windows/Fonts/georgia.ttf',size)
def fit(im,w,h):
 im=im.copy();im.thumbnail((w,h),Image.Resampling.LANCZOS);return im
def source(i):
 path=WORK/f'activity-{i+1:02d}-scene.png' if i in REFINED else OLD/f'activity-{i+1:02d}-rest-cutout.png'
 raw=Image.open(path).convert('RGBA');im=raw.copy()
 if i in REFINED:
  im.putalpha(im.getchannel('A').point(lambda a:0 if a<=4 else a))
  box=im.getchannel('A').point(lambda a:255 if a>7 else 0).getbbox()
  assert box is not None
  im=im.crop(box)
 return path,raw,im
SOURCES=[];SCENES=[];metadata=[]
for i in range(9):
 p,raw,im=source(i);SOURCES.append(p)
 row,col=divmod(i,3);top=TOP[row]+STAGGER[i]
 fitted=fit(im,*MAX_SCENE[i]);x=CX[col]-fitted.width//2;y=top+(MAX_SCENE[i][1]-fitted.height)//2
 layer=blank();layer.alpha_composite(fitted,(x,y));SCENES.append(layer)
 metadata.append({'name':NAMES[i],'source_file':str(p),'source_sha256':sha(p),'raw_dimensions':list(raw.size),
  'display_box':[x,y,x+fitted.width,y+fitted.height],'revision':'scene refined' if i in REFINED else 'scene retained exactly',
  'true_transparency':raw.mode=='RGBA' and raw.getchannel('A').getextrema()[0]==0})

def title_layer(i,focus=False):
 row,col=divmod(i,3);art,meta=make_name(i,focus=focus)
 layer=blank();layer.alpha_composite(art,(CX[col]-art.width//2,NAME_Y[row]-art.height//2))
 return layer
def component(i,focus=False):
 layer=SCENES[i].copy();layer.alpha_composite(title_layer(i,focus));return layer
def page(focus=False):
 layer=blank()
 for i in range(9):layer.alpha_composite(component(i,focus))
 return Image.alpha_composite(BASE,layer).convert('RGB'),layer

result,overlay=page();focus_page,focus_overlay=page(True)
report={'status':'UNAPPROVED STATIC VISUAL REFINEMENT','project':'The Haunted Realm',
 'authorized_scope':'Four unapproved scene refinements and nine exact activity-name treatments, in the existing composition',
 'dimensions':[1536,1024],'activity_names':NAMES,'protected_hashes_before':BEFORE,'artwork':metadata,
 'layout_preserved':{'centres':CX,'row_tops':TOP,'stagger':STAGGER,'name_centres':NAME_Y,'maximum_scene_slots':MAX_SCENE},
 'retained_scene_checks':{},'pixel_checks':{},'comparison_notes':[
 'Before/after scenes are design refinements, not animation keyframes.',
 'Focus lettering uses the same font masks, positions, textures and mist geometry; only controlled light/opacity parameters change.',
 'No final activity images or mobile layout are approved by this review.'],
 'unexpected_details':['Hotel guest has a full realistic wolf head rather than subtle wolf features.',
 'Refined unapproved hotel artwork includes some architecture, furniture and lighting drift; protected sources are unaffected.',
 'Door departure/bill detail is small at the all-nine scale; the dominant change is the deep route through reception and dining.']}

for i in sorted(RETAINED):
 raw=Image.open(OLD/f'activity-{i+1:02d}-rest-cutout.png').convert('RGBA')
 fitted=fit(raw,*MAX_SCENE[i]);row,col=divmod(i,3)
 old=blank();old.alpha_composite(fitted,(CX[col]-fitted.width//2,TOP[row]+STAGGER[i]+(MAX_SCENE[i][1]-fitted.height)//2))
 changed=int(np.any(np.asarray(old)!=np.asarray(SCENES[i]),axis=2).sum())
 assert changed==0
 report['retained_scene_checks'][NAMES[i]]={'changed_image_layer_pixels':changed}
for view,(im,layer) in {'resting':(result,overlay),'focus_light_study':(focus_page,focus_overlay)}.items():
 delta=np.any(np.asarray(im)!=base,axis=2);support=np.asarray(layer.getchannel('A'))>0
 checks={'title_changed_pixels':int(delta[65:280,443:1093].sum()),'navigation_band_changed_pixels':int(delta[:65].sum()),
  'pixels_changed_above_activity_area':int(delta[:290].sum()),'pixels_changed_outside_review_overlays':int((delta & ~support).sum())}
 assert all(v==0 for v in checks.values()),checks
 checks['unmodified_base_pixel_percent']=round(float((~delta).mean())*100,2)
 checks['mean_base_visibility_activity_area_percent']=round(float((1-np.asarray(layer.getchannel('A'))[290:]/255).mean())*100,2)
 report['pixel_checks'][view]=checks
result.save(OUT/'the-haunted-realm-nine-destinations-refined-review-v3.png')
overlay.save(WORK/'nine-refined-overlay-v3.png')

# Before/after scene crops: review-board captions are separate from website imagery.
board=Image.new('RGB',(1536,1820),(19,23,31));d=ImageDraw.Draw(board)
d.text((30,20),'FOCUSED SCENE REFINEMENTS — BEFORE / REVISED',font=font(27,True),fill=(236,230,216))
d.text((30,64),'Design revisions only. These paired images do not represent working animation.',font=font(17),fill=(193,204,214))
d.text((35,104),'PREVIOUS REVIEW',font=font(17,True),fill=(218,224,230));d.text((800,104),'REVISED REVIEW',font=font(17,True),fill=(246,218,170))
notes=['Ancient roundhouses and cool darkness replace the ambiguous warm horizon; no ritual is depicted.',
 'The single book remains the hero; vessels, herbs, crystal and other surrounding props are removed.',
 'A deeper threshold, reception, dining room and receding arches establish a route through the restaurant.',
 'Original supernatural guests, reception keys and luggage strengthen the haunted monster-hotel identity.']
for k,i in enumerate((0,2,6,8)):
 row,col=divmod(i,3);top=TOP[row]+STAGGER[i];cy=NAME_Y[row];y=145+k*410
 d.text((35,y),NAMES[i],font=font(23,True),fill=(238,233,219))
 box=(CX[col]-238,top-8,CX[col]+238,min(1024,cy+43))
 for im,x in ((prior_page,35),(result,800)):
  region=im.crop(box);scale=min(695/region.width,320/region.height)
  region=region.resize((round(region.width*scale),round(region.height*scale)),Image.Resampling.LANCZOS)
  board.paste(region,(x+(695-region.width)//2,y+40))
 d.text((35,y+375),notes[k],font=font(16),fill=(197,207,216))
board.save(OUT/'the-haunted-realm-focused-scene-comparison-v3.png')

# On-scene before/after lettering, preserving the same unmodified local scenery.
board=Image.new('RGB',(1536,1135),(19,23,31));d=ImageDraw.Draw(board)
d.text((30,20),'ACTIVITY-NAME LETTERING — PREVIOUS / SPECTRAL INSCRIPTIONS',font=font(25,True),fill=(237,231,220))
d.text((35,64),'PREVIOUS PLAIN LABEL',font=font(17,True),fill=(218,224,230));d.text((800,64),'REVISED ENGRAVED / WEATHERED / MIST-LIT',font=font(17,True),fill=(245,218,174))
for i in range(9):
 row,col=divmod(i,3);y=104+i*112
 box=(CX[col]-238,NAME_Y[row]-42,CX[col]+238,min(1024,NAME_Y[row]+49))
 for im,x in ((prior_page,35),(result,800)):
  region=im.crop(box);region=region.resize((695,round(region.height*695/region.width)),Image.Resampling.LANCZOS)
  board.paste(region,(x,y))
board.save(OUT/'the-haunted-realm-lettering-before-after-v3.png')

# True controlled focus illustration: artwork and geometry identical between both columns.
board=Image.new('RGB',(1536,1000),(19,23,31));d=ImageDraw.Draw(board)
d.text((30,20),'LETTERING DETAILS — CONTROLLED HOVER / KEYBOARD FOCUS',font=font(25,True),fill=(237,231,220))
d.text((30,60),'Cropped details with identical artwork and lettering geometry. Static light studies; transitions are not implemented.',font=font(17),fill=(190,203,215))
d.text((35,99),'RESTING',font=font(17,True),fill=(218,224,230));d.text((800,99),'FOCUS: CLEARER LETTER LIGHT / LESS LOWER MIST',font=font(17,True),fill=(245,218,174))
for k,i in enumerate((2,5,8)):
 row,col=divmod(i,3);top=TOP[row]+STAGGER[i];y=141+k*275
 box=(CX[col]-238,top+46,CX[col]+238,min(1024,NAME_Y[row]+43))
 for im,x in ((result,35),(focus_page,800)):
  region=im.crop(box);scale=min(695/region.width,250/region.height)
  region=region.resize((round(region.width*scale),round(region.height*scale)),Image.Resampling.LANCZOS)
  board.paste(region,(x+(695-region.width)//2,y))
board.save(OUT/'the-haunted-realm-controlled-focus-study-v3.png')

# Lettering-only 320-pixel proof. No protected title/navigation adaptation is proposed here.
small_lines=[['ECHOES OF THE PAST'],['THE CURSED QUEST'],['THE BOOK OF','SHADOWS'],['FASTEST FINGER','FIRST'],
 ['WORDS OF THE FEAST'],['THE PHANTOM ORDER'],['DOOR TO DARKNESS'],['BUILD THE HAUNTED','BANQUET'],['HOTEL TRANSYLVANIA']]
assert [' '.join(v) for v in small_lines]==NAMES
small=Image.new('RGB',(320,875),(23,26,35));d=ImageDraw.Draw(small)
d.text((12,10),'320px LETTERING-ONLY STUDY',font=font(13),fill=(225,225,216))
for i in range(9):
 art,meta=make_name(i,size=22,width=320,lines=small_lines[i]);small.paste(art,(0,37+i*91),art)
small.save(OUT/'the-haunted-realm-small-screen-lettering-study-v3.png')

report['protected_hashes_after']=verify();report['all_11_protected_assets_unchanged']=report['protected_hashes_after']==BEFORE
report['accepted_five_scene_layers_unchanged']=all(v['changed_image_layer_pixels']==0 for v in report['retained_scene_checks'].values())
report['no_website_implementation']=True;report['no_navigation_or_title_changes']=True
report['historical_visual_reference']='https://museum.wales/collections/historic-buildings/3/Bryn-Eryr-Iron-Age-Roundhouses/'
report['historical_scope']='Archaeology-informed building forms used for ancient-past atmosphere; not a factual Samhain ritual or exact historical event.'
(OUT/'the-haunted-realm-refinement-verification-v3.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
prompts=[p.name+'\n'+p.read_text(encoding='utf-8') for p in sorted(WORK.glob('activity-*-prompt.txt'))]
(OUT/'the-haunted-realm-refinement-artwork-prompts-v3.txt').write_text('\n\n'.join(prompts),encoding='utf-8')
print(json.dumps({'protected_assets':report['all_11_protected_assets_unchanged'],'retained_five':report['accepted_five_scene_layers_unchanged'],
 'checks':report['pixel_checks'],'names':NAMES},indent=2))
