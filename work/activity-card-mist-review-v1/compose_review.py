"""Static activity-card concept review only. No website or interactive code."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops,ImageEnhance

ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
VERSION='v2'
NAV=json.loads((OUT/'the-haunted-realm-navigation-approved-assets.json').read_text(encoding='utf-8'))
PREVIOUS=json.loads((OUT/'the-haunted-realm-navigation-b-redesign-verification-v3-final.json').read_text(encoding='utf-8'))
PROTECTED=dict(PREVIOUS['protected_hashes_after'])
PROTECTED.update({a['file']:a['sha256'] for a in NAV['assets']})
def source_hashes():
 hashes={}
 for name,expected in PROTECTED.items():
  actual=hashlib.sha256((OUT/name).read_bytes()).hexdigest().upper()
  if actual!=expected:raise RuntimeError('Protected asset mismatch: '+name)
  hashes[name]=actual
 return hashes
BEFORE=source_hashes()
BASE=Image.open(OUT/'the-haunted-realm-navigation-b-home-redesign-review-v3-final.png').convert('RGBA')
SIZE=BASE.size
TITLE=(443,65,1093,280)

def blank(size=SIZE):return Image.new('RGBA',size,(0,0,0,0))
def font(size,bold=False,sans=False):
 return ImageFont.truetype('C:/Windows/Fonts/arial.ttf' if sans else 'C:/Windows/Fonts/georgiab.ttf' if bold else 'C:/Windows/Fonts/georgia.ttf',size)

def artwork(name):
 im=Image.open(WORK/name).convert('RGBA')
 # Remove only virtually invisible generation dust on temporary materials.
 im.putalpha(im.getchannel('A').point(lambda a:0 if a<=4 else a))
 box=im.getchannel('A').point(lambda a:255 if a>7 else 0).getbbox()
 if box is None:raise RuntimeError('Empty generated artwork: '+name)
 return im.crop(box)

def fit(im,w,h):
 im=im.copy();im.thumbnail((w,h),Image.Resampling.LANCZOS)
 return im

def multiplied_alpha(im,factor):
 result=im.copy()
 result.putalpha(result.getchannel('A').point(lambda a:round(a*factor)))
 return result

def words(layer,value,cx,cy,size,bold=False,selected=False,sans=False):
 f=font(size,bold,sans)
 d=ImageDraw.Draw(layer)
 b=d.textbbox((0,0),value,font=f)
 x=round(cx-(b[2]-b[0])/2);y=round(cy-(b[3]-b[1])/2-b[1])
 # Names are opaque, with only a tight glyph-shaped contact shadow.
 shadow=blank()
 sd=ImageDraw.Draw(shadow)
 sd.text((x,y+1),value,font=f,fill=(6,9,17,200),stroke_width=1,stroke_fill=(6,9,17,200))
 shadow=shadow.filter(ImageFilter.GaussianBlur(.6))
 layer.alpha_composite(shadow)
 d=ImageDraw.Draw(layer)
 colour=(254,225,177,255) if selected else (237,231,214,255)
 d.text((x,y),value,font=f,fill=colour,stroke_width=1,stroke_fill=(10,13,22,255))

SCENES=[artwork('temporary-scene-'+s+'.png') for s in ('a','b','c')]
MIST=artwork('temporary-mist-veil.png')
LAYOUT=[(78,340),(558,365),(1038,340)]
COMPONENTS=[]

def vision(index,focus=False):
 layer=blank()
 x,y=LAYOUT[index]
 scene=fit(SCENES[index],420,315)
 sx=x+(420-scene.width)//2
 sy=y+(315-scene.height)//2
 layer.alpha_composite(scene,(sx,sy))
 mist=MIST.resize((456,245),Image.Resampling.LANCZOS)
 # Reverse the asymmetric veil on one example to avoid repeated visual contours.
 if index==2:mist=mist.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 # Raw generated veil was too dense; restrained compositing avoids a cloud frame.
 if index==1:
  # Foreground mist crosses the actual lower path, so withdrawal reveals scenery.
  mist=MIST.resize((342,196),Image.Resampling.LANCZOS)
  mist=multiplied_alpha(mist,0 if focus else .50)
  layer.alpha_composite(mist,(x+39,y+119))
 else:
  mist=multiplied_alpha(mist,.32)
  layer.alpha_composite(mist,(x-18,y+135))
 words(layer,f'Activity {index+1}',x+210,y+343,30,True,focus)
 words(layer,'TEMPORARY SCENE',x+210,y+373,11,sans=True)
 return layer

rest=blank()
for i in range(3):
 part=vision(i)
 COMPONENTS.append(part)
 rest.alpha_composite(part)
focus=blank()
for i in range(3):focus.alpha_composite(vision(i,i==1))

base_arr=np.asarray(BASE.convert('RGB'))
report={'status':'UNAPPROVED ACTIVITY-CARD CONCEPT REVIEW','scope':'Static images only; no website implementation',
 'dominant_direction':'Scenes in the Mist','borrowed_details':'Occasional masonry fragments and faint aged photographic edges; no complete frames or photo borders',
 'imagery':'Three disposable neutral atmosphere studies, not approved activity content or permanent scenes',
 'protected_hashes_before':BEFORE,'views':{}}
for name,layer in [('rest',rest),('focus',focus)]:
 result=Image.alpha_composite(BASE,layer).convert('RGB')
 path=OUT/f'the-haunted-realm-activity-cards-mist-{name}-review-{VERSION}.png'
 if path.exists() and not np.array_equal(np.asarray(Image.open(path).convert('RGB')),np.asarray(result)):
  raise RuntimeError('Review output already exists with different pixels: '+str(path))
 change=np.any(np.asarray(result)!=base_arr,axis=2)
 allowed=np.asarray(layer.getchannel('A'))>0
 x0,y0,x1,y1=TITLE
 title_count=int(np.count_nonzero(change[y0:y1,x0:x1]))
 nav_count=int(np.count_nonzero(change[:65,:]))
 outside=int(np.count_nonzero(change & ~allowed))
 assert title_count==0 and nav_count==0 and outside==0
 if not path.exists():result.save(path)
 layer.save(WORK/f'{name}-overlay-{VERSION}.png')
 report['views'][name]={'file':str(path),'size':result.size,'overlay_bounds':layer.getbbox(),
  'changed_pixels_in_title':title_count,'changed_pixels_in_top_navigation_band':nav_count,'changed_pixels_outside_vision_overlay':outside}

rest_result=np.asarray(Image.alpha_composite(BASE,rest).convert('RGB'))
focus_result=np.asarray(Image.alpha_composite(BASE,focus).convert('RGB'))
changed=np.any(rest_result!=focus_result,axis=2)
middle_support=(np.asarray(vision(1).getchannel('A'))>0)|(np.asarray(vision(1,True).getchannel('A'))>0)
assert int(np.count_nonzero(changed & ~middle_support))==0
report['focus_demonstration']={'focused_example':'Activity 2','changed_pixels_outside_middle_example':0,
 'behaviour':'Foreground mist reduced; slightly warmer opaque lettering; identical scene, scale and positions',
 'interactive_implementation':False}

# Close-up compares the same location; captions sit outside the website reference.
sheet=Image.new('RGB',(1100,630),(20,23,30))
d=ImageDraw.Draw(sheet)
d.text((28,22),'SCENES IN THE MIST — STATIC FOCUS STUDY',font=font(24,True),fill=(230,231,222))
d.text((28,64),'Same temporary scene and position. Mist withdraws; no glowing button or frame.',font=font(16),fill=(182,190,197))
d.text((28,111),'Resting',font=font(21,True),fill=(227,232,231))
d.text((575,111),'Hover / keyboard focus',font=font(21,True),fill=(246,219,178))
box=(520,336,1016,794)
for key,px in [('rest',28),('focus',575)]:
 crop=Image.open(OUT/f'the-haunted-realm-activity-cards-mist-{key}-review-{VERSION}.png').crop(box)
 sheet.paste(crop,(px,150))
sheet.save(OUT/f'the-haunted-realm-activity-cards-mist-focus-detail-{VERSION}.png')

report['protected_hashes_after']=source_hashes()
report['all_11_protected_assets_unchanged']=report['protected_hashes_after']==BEFORE
report['architecture']='Three examples only; no activity count/order/names finalized; future list remains expandable'
(OUT/f'the-haunted-realm-activity-cards-mist-verification-{VERSION}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
parts=[]
for p in sorted(WORK.glob('*-prompt.txt')):parts.append(p.name+'\n'+p.read_text(encoding='utf-8'))
(OUT/'the-haunted-realm-activity-cards-mist-artwork-prompts-v1.txt').write_text('\n\n'.join(parts),encoding='utf-8')
print(json.dumps({'all_11_protected_assets_unchanged':report['all_11_protected_assets_unchanged'],
 'views':report['views'],'focus_demonstration':report['focus_demonstration']},indent=2))
