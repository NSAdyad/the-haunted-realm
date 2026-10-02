"""Raster-only nine-destination review; no website or animation implementation."""
from pathlib import Path
import hashlib,json,math,textwrap
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter

ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
VERSION='v2'
NAV=json.loads((OUT/'the-haunted-realm-navigation-approved-assets.json').read_text(encoding='utf-8'))
PRIOR=json.loads((OUT/'the-haunted-realm-navigation-b-redesign-verification-v3-final.json').read_text(encoding='utf-8'))
EXPECTED=dict(PRIOR['protected_hashes_after'])
EXPECTED.update({a['file']:a['sha256'] for a in NAV['assets']})
def verify_sources():
 actual={n:hashlib.sha256((OUT/n).read_bytes()).hexdigest().upper() for n in EXPECTED}
 bad=[n for n,h in actual.items() if h!=EXPECTED[n]]
 if bad:raise RuntimeError('Protected source mismatch: '+', '.join(bad))
 return actual
BEFORE=verify_sources()
BASE=Image.open(OUT/'the-haunted-realm-navigation-b-home-redesign-review-v3-final.png').convert('RGBA')
SIZE=BASE.size
assert SIZE==(1536,1024)

NAMES=['Echoes of the Past','The Cursed Quest','The Book of Shadows','Fastest Finger First',
 'Words of the Feast','The Phantom Order','Door to Darkness','Build the Haunted Banquet','Hotel Transylvania']
LINES=[['Echoes of the Past'],['The Cursed Quest'],['The Book of Shadows'],['Fastest Finger First'],
 ['Words of the Feast'],['The Phantom Order'],['Door to Darkness'],['Build the Haunted','Banquet'],['Hotel Transylvania']]
BEHAVIOUR=[
 'Ancient traces and embers resurface through the landscape.',
 'Question material awakens; another challenge sheet is revealed.',
 'A single page lifts as ink and light emerge from the book.',
 'One competitor depresses the buzzer first; the other is still poised.',
 'Breath-like steam lifts from the menu; language comes into focus.',
 'An unseen presence materialises and delivers the order slip.',
 'Light opens a route from entrance through reception into dining.',
 'Separate drafts align into an unfinished role-play preparation.',
 'The original hotel hall opens; unusual guests become apparent.']

def blank(size=SIZE):return Image.new('RGBA',size,(0,0,0,0))
def font(size,bold=False,sans=False):
 p='C:/Windows/Fonts/arial.ttf' if sans else 'C:/Windows/Fonts/georgiab.ttf' if bold else 'C:/Windows/Fonts/georgia.ttf'
 return ImageFont.truetype(p,size)

def split_art(index):
 path=WORK/f'activity-{index+1:02d}-state-sheet.png'
 im=Image.open(path).convert('RGBA')
 im.putalpha(im.getchannel('A').point(lambda a:0 if a<=4 else a))
 w,h=im.size
 row=np.asarray(im.getchannel('A'),dtype=np.float32).sum(axis=1)
 # Find the central transparent separation; never cut through an opaque scene.
 lo,hi=int(h*.43),int(h*.57)
 sep=lo+int(np.argmin(row[lo:hi]))
 gap_alpha=float(row[sep]/w)
 if gap_alpha>20:raise RuntimeError(f'No clear separation in activity {index+1}; mean alpha {gap_alpha:.2f}')
 halves=[im.crop((0,0,w,sep)),im.crop((0,sep,w,h))]
 results=[]
 for state,half in zip(('rest','reveal'),halves):
  # Fade only residual mist at the sheet split. Raw generated sheet is preserved.
  alpha=np.asarray(half.getchannel('A'),dtype=np.float32).copy()
  edge=min(6,half.height)
  ramp=np.linspace(0,1,edge,dtype=np.float32)
  if state=='rest':alpha[-edge:]*=ramp[::-1,None]
  else:alpha[:edge]*=ramp[:,None]
  half.putalpha(Image.fromarray(np.rint(alpha).astype(np.uint8)))
  box=half.getchannel('A').point(lambda a:255 if a>7 else 0).getbbox()
  if box is None:raise RuntimeError('Empty artwork half')
  crop=half.crop(box)
  crop.save(WORK/f'activity-{index+1:02d}-{state}-cutout.png')
  results.append(crop)
 return results,{'file':str(path),'dimensions':[w,h],'split_y':sep,'gap_mean_alpha':gap_alpha,
  'cutout_dimensions':[list(a.size) for a in results]}

ART=[]
metadata=[]
for i in range(9):
 pair,meta=split_art(i);ART.append(pair);metadata.append(meta)

def fit(im,w,h,upscale=False):
 im=im.copy()
 if upscale:
  scale=min(w/im.width,h/im.height)
  return im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 im.thumbnail((w,h),Image.Resampling.LANCZOS)
 return im

def name_text(layer,lines,cx,cy,size=28):
 f=font(size,True)
 d=ImageDraw.Draw(layer)
 heights=[d.textbbox((0,0),s,font=f) for s in lines]
 line_step=32
 first=cy-(len(lines)-1)*line_step/2
 for line,b,yc in zip(lines,heights,[first+k*line_step for k in range(len(lines))]):
  x=round(cx-(b[2]-b[0])/2);y=round(yc-(b[3]-b[1])/2-b[1])
  shadow=blank(layer.size);sd=ImageDraw.Draw(shadow)
  sd.text((x,y+1),line,font=f,fill=(5,8,14,220),stroke_width=2,stroke_fill=(5,8,14,220))
  layer.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(.6)))
  d=ImageDraw.Draw(layer)
  d.text((x,y),line,font=f,fill=(243,236,219,255),stroke_width=1,stroke_fill=(8,12,20,255))

# Three rows of related visions; these positions/count are review-only.
# The approved title ends at y280. All new artwork starts below y301.
CX=[285,768,1251]
TOP=[309,541,770]
STAGGER=[0,7,-3,5,-2,8,-1,4,0]
NAME_Y=[507,739,973]
MAX_SCENE=[(420,172)]*8+[(438,176)]
LAYOUT=[]
for i in range(9):
 row,col=divmod(i,3)
 LAYOUT.append({'cx':CX[col],'top':TOP[row]+STAGGER[i],'name_y':NAME_Y[row],
  'max_size':MAX_SCENE[i],'row':row,'col':col})

def component(i,state):
 layer=blank()
 p=LAYOUT[i]
 source=ART[i][0 if state=='rest' else 1]
 im=fit(source,*p['max_size'])
 x=p['cx']-im.width//2
 y=p['top']+(p['max_size'][1]-im.height)//2
 layer.alpha_composite(im,(x,y))
 name_text(layer,LINES[i],p['cx'],p['name_y'])
 return layer

def save_new(im,path):
 if path.exists():
  old=Image.open(path).convert(im.mode)
  if old.size!=im.size or not np.array_equal(np.asarray(old),np.asarray(im)):
   raise RuntimeError('Will not overwrite existing different candidate: '+str(path))
 else:im.save(path)

base=np.asarray(BASE.convert('RGB'))
report={'project':'The Haunted Realm','status':'UNAPPROVED NINE-DESTINATION VISUAL REVIEW',
 'authorization':'Static composition and two-state illustrative storyboards only; no website implementation',
 'protected_hashes_before':BEFORE,'activity_names':NAMES,'artwork':metadata,
 'page_dimensions':[1536,1024],'layout':'Three rows, three visions per row; example composition, not a permanent capacity limit',
 'protected_navigation':'Exact approved reference retained, including its temporary navigation labels/IMAGE slots',
 'views':{},'state_comparisons':[]}

COMPS={}
for state in ('rest','reveal'):
 layer=blank()
 for i in range(9):layer.alpha_composite(component(i,state))
 result=Image.alpha_composite(BASE,layer).convert('RGB')
 delta=np.any(np.asarray(result)!=base,axis=2)
 support=np.asarray(layer.getchannel('A'))>0
 checks={'changed_pixels_in_title':int(delta[65:280,443:1093].sum()),
  'changed_pixels_in_navigation_band':int(delta[:65].sum()),
  'changed_pixels_above_activity_area':int(delta[:290].sum()),
  'changed_pixels_outside_new_overlays':int((delta & ~support).sum())}
 assert all(v==0 for v in checks.values()),checks
 path=OUT/f'the-haunted-realm-nine-destinations-{state}-review-{VERSION}.png'
 save_new(result,path)
 layer.save(WORK/f'nine-{state}-overlay-{VERSION}.png')
 COMPS[state]=result
 report['views'][state]={'file':str(path),'overlay_bounds':layer.getbbox(),**checks,
  'unmodified_base_pixel_percent':round(float(np.count_nonzero(~delta))*100/delta.size,2),
  'mean_source_visibility_in_activity_area_percent':round(float(np.mean(1-np.asarray(layer.getchannel('A'))[290:].astype(float)/255))*100,2)}

# Separate review boards. Captions/background are outside the Landing Page.
for group in range(3):
 board=Image.new('RGB',(1536,1500),(19,23,31))
 d=ImageDraw.Draw(board)
 d.text((32,24),f'SCENES IN THE MIST — STATE STUDIES {group*3+1}–{group*3+3}',font=font(28,True),fill=(237,234,224))
 d.text((32,70),'Illustrative keyframes, not working animation. Original page scenery remains behind every vision.',font=font(17),fill=(183,192,202))
 d.text((40,113),'RESTING / FIRST APPEARANCE',font=font(17,True),fill=(215,222,229))
 d.text((800,113),'HOVER / FOCUS / REVEAL DIRECTION',font=font(17,True),fill=(247,221,180))
 for k in range(3):
  i=group*3+k;p=LAYOUT[i];y=156+k*435
  d.text((36,y),f'{i+1}. {NAMES[i]}',font=font(23,True),fill=(240,234,220))
  # A magnified crop of only the unprotected activity region, not the title/nav.
  box=(p['cx']-235,p['top']-8,p['cx']+235,min(1024,max(p['top']+222,p['name_y']+36)))
  for state,x in [('rest',36),('reveal',800)]:
   region=Image.alpha_composite(BASE,component(i,state)).convert('RGB').crop(box)
   region=fit(region,696,344,upscale=True)
   board.paste(region,(x+(696-region.width)//2,y+36))
  text=BEHAVIOUR[i]
  d.text((36,y+395),text,font=font(17),fill=(193,202,211))
 path=OUT/f'the-haunted-realm-nine-destinations-state-study-{group+1}-{VERSION}.png'
 save_new(board,path)
 report['state_comparisons'].append({'file':str(path),'activities':NAMES[group*3:group*3+3],
  'note':'Magnified static storyboard crops; paired generated artwork may contain minor render differences beyond intended motion. No final animation assets approved.'})

report['protected_hashes_after']=verify_sources()
report['all_11_protected_assets_unchanged']=report['protected_hashes_after']==BEFORE
report['no_website_implementation']=True
report['no_activity_navigation_visuals_replaced']=True
report['no_final_activity_images_approved']=True
(OUT/f'the-haunted-realm-nine-destinations-verification-{VERSION}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
prompts=[]
for p in sorted(WORK.glob('activity-*-prompt.txt')):prompts.append(p.name+'\n'+p.read_text(encoding='utf-8'))
(OUT/f'the-haunted-realm-nine-destinations-artwork-prompts-{VERSION}.txt').write_text('\n\n'.join(prompts),encoding='utf-8')
print(json.dumps({'protected':report['all_11_protected_assets_unchanged'],'views':report['views'],
 'state_comparisons':report['state_comparisons']},indent=2))
