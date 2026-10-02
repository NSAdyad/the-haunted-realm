"""Option B v3: separate iron/glass static review images, no website code."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
SOURCES={
 'the-haunted-realm-background-corrected-review-v3.png':'1561627199D2DA3412C5D5E49143A6B699201659AD1CEE56A38CEB8E96F28C06',
 'the-haunted-realm-background-review-v1.png':'63392BF751F4C5518A26E9D82188C3C29CDCEB61B9A50C6E8F2F32BB34BC668F',
 'the-haunted-realm-title-approved.png':'5F3DB4E9112D076A73E22587FCAEE26022B2188993A1DB6ABBB7A912ABF68A4A',
 'the-haunted-realm-title-option-1-centred-review-v2.png':'1A4B8C14C4229B0C2E68DB47086B0A741C667930B16E531DCB2455905A0C7942',
 'the-haunted-realm-title-original-artwork-backup.png':'D40B8107D55723CD6976C880905564458DCA17082D55AAAF7F561D6DC6D3F7C1',
}
def verify_sources():
 hashes={}
 for name,expected in SOURCES.items():
  h=hashlib.sha256((OUT/name).read_bytes()).hexdigest().upper()
  if h!=expected: raise RuntimeError('Protected asset mismatch: '+name)
  hashes[name]=h
 return hashes
BEFORE=verify_sources()
BASE=Image.open(OUT/'the-haunted-realm-title-option-1-centred-review-v2.png').convert('RGBA')
SIZE=BASE.size
TITLE=(443,65,1093,280)

def blank(size=SIZE): return Image.new('RGBA',size,(0,0,0,0))
def asset(name):
 im=Image.open(WORK/name).convert('RGBA')
 im.putalpha(im.getchannel('A').point(lambda a:0 if a<=4 else 255 if a>=250 else a))
 b=im.getchannel('A').point(lambda a:255 if a>4 else 0).getbbox()
 if b is None: raise RuntimeError('Empty artwork '+name)
 return im.crop(b)
def font(size,bold=False,sans=False):
 path='C:/Windows/Fonts/arial.ttf' if sans else 'C:/Windows/Fonts/georgiab.ttf' if bold else 'C:/Windows/Fonts/georgia.ttf'
 return ImageFont.truetype(path,size)

def lettering(layer,value,x,y,size=22,selected=False,centred=False,sans=False):
 f=font(size,bold=selected,sans=sans)
 d=ImageDraw.Draw(layer)
 b=d.textbbox((0,0),value,font=f)
 if centred:x-=(b[2]-b[0])/2
 y-=(b[3]-b[1])/2+b[1]
 # Opaque letters and a tight dark keyline maintain clarity on clear glass.
 d.text((round(x),round(y)),value,font=f,fill=(255,218,143,255) if selected else (235,237,225,255),
        stroke_width=1,stroke_fill=(10,13,18,255))

def image_space(layer,x,y,size):
 d=ImageDraw.Draw(layer)
 d.rectangle((x,y,x+size-1,y+size-1),fill=(17,22,31,25),outline=(152,169,176,185),width=1)
 d.line((x+1,y+1,x+size-2,y+1),fill=(222,232,229,105))
 lettering(layer,'IMAGE',x+size/2,y+size/2,6 if size<=24 else 8,centred=True,sans=True)

def chevron(layer,x,y):
 ImageDraw.Draw(layer).line([(x-4,y-2),(x,y+2),(x+4,y-2)],fill=(230,232,224,255),width=1)

FRAME=asset('haunted-glass-frame.png')
CHAINS=asset('iron-chain-supports.png')
# Generated hardware remains an independent layer. Glass transmission is explicit,
# rather than lowering the opacity of an opaque object or its typography.

def glass_label(width,height,selected=False,variant=0):
 im=blank((width,height))
 inner=(round(width*.065),round(height*.19),round(width*.935),round(height*.89))
 x0,y0,x1,y1=inner
 glass=blank((width,height))
 d=ImageDraw.Draw(glass)
 d.rectangle((x0,y0,x1,y1),fill=(15,24,33,34))
 # Fine partial reflections, kept to the edge rather than washing out scenery.
 d.line((x0+1,y0+1,x1-2,y0+1),fill=(181,213,221,64),width=1)
 d.line((x0+1,y0+2,x0+1,y1-2),fill=(174,198,205,40),width=1)
 im.alpha_composite(glass)
 physical=FRAME
 # Vary damage placement on unprotected artwork; labels and scenery stay fixed.
 if variant in (1,3): physical=physical.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if variant in (2,3): physical=physical.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 physical=physical.resize((width,height),Image.Resampling.LANCZOS)
 if selected:
  # A restrained reflected lamp wash affects hardware, not the whole glass panel.
  arr=np.asarray(physical).copy()
  yy,xx=np.mgrid[0:height,0:width]
  falloff=np.exp(-(((xx-width*.18)/(width*.65))**2+((yy-height*.78)/(height*.9))**2))
  a=(falloff*48*arr[:,:,3]/255).astype('uint8')
  tint=Image.new('RGBA',physical.size,(255,171,70,0));tint.putalpha(Image.fromarray(a))
  physical=Image.alpha_composite(physical,tint)
  d=ImageDraw.Draw(im)
  # Weak warm glint on the existing lower glass edge, not a selection rectangle.
  d.line((x0+2,y1-1,round(width*.68),y1-1),fill=(244,184,95,100),width=1)
 im.alpha_composite(physical)
 return im,inner

def place(layer,obj,x,y):
 # A tight contact shadow under the metal only; no dark panel behind the assembly.
 shadow=Image.new('RGBA',obj.size,(6,9,15,0))
 alpha=obj.getchannel('A').point(lambda a:round(a*.25) if a>=180 else 0)
 shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(.55)))
 layer.alpha_composite(shadow,(x,y+1))
 layer.alpha_composite(obj,(x,y))

PANE_BOXES=[]
def home():
 layer=blank()
 labels=['Home']+[f'Activity {i}' for i in range(1,7)]+['Activities']
 gap=10;x=16;y=8;width=1504;height=48
 cell=(width-7*gap)/8
 for i,value in enumerate(labels):
  left=round(x+i*(cell+gap));right=round(x+i*(cell+gap)+cell)
  obj,inner=glass_label(right-left,height,i==0,i%4)
  place(layer,obj,left,y)
  if value=='Activities':
   lettering(layer,value,(left+right)/2-6,y+26,18,centred=True)
   chevron(layer,right-23,y+28)
  else:
   image_space(layer,left+18,y+15,22)
   lettering(layer,value,left+48,y+26,18,i==0)
 return layer

def activity():
 layer=blank()
 x=16;width=280
 # Sparse physical support chains. The large interior stays empty alpha.
 supports=CHAINS.resize((244,916),Image.Resampling.LANCZOS)
 layer.alpha_composite(supports,(34,28))
 obj,inner=glass_label(width,44)
 place(layer,obj,x,16)
 lettering(layer,'Activities',x+width/2,41,20,centred=True)
 labels=['Home']+[f'Activity {i}' for i in range(1,7)]
 for i,value in enumerate(labels):
  y=82+i*110
  obj,inner=glass_label(width,72,i==3,i%4)
  place(layer,obj,x,y)
  image_space(layer,x+28,y+23,38)
  lettering(layer,value,x+81,y+40,23,i==3)
  PANE_BOXES.append((x+inner[0],y+inner[1],x+inner[2],y+inner[3]))
 obj,inner=glass_label(width,48)
 place(layer,obj,x,918)
 lettering(layer,'More activities',x+width/2-7,945,17,centred=True)
 chevron(layer,x+width-30,945)
 return layer

layers={'home':home(),'activity':activity()}
report={'scope':'Ground-up Option B visual redesign; STATIC REVIEW ONLY; navigation NOT APPROVED',
        'protected_hashes_before':BEFORE,'material_identity':'corroded black iron + clear aged glass + sparse chains; no oak plaques','views':{}}
base_arr=np.asarray(BASE.convert('RGB'))
for key,layer in layers.items():
 output=Image.alpha_composite(BASE,layer).convert('RGB')
 path=OUT/f'the-haunted-realm-navigation-b-{key}-redesign-review-v3-final.png'
 if path.exists() and not np.array_equal(np.asarray(Image.open(path).convert('RGB')),np.asarray(output)):
  raise RuntimeError('Refusing to overwrite different review '+str(path))
 changes=np.any(np.asarray(output)!=base_arr,axis=2)
 allowed=np.asarray(layer.getchannel('A'))>0
 x0,y0,x1,y1=TITLE
 outside=int(np.count_nonzero(changes & ~allowed))
 title=int(np.count_nonzero(changes[y0:y1,x0:x1]))
 assert outside==0 and title==0
 if not path.exists():output.save(path)
 layer.save(WORK/f'{key}-overlay.png')
 report['views'][key]={'file':str(path),'dimensions':output.size,'navigation_bounds':layer.getbbox(),
   'changed_pixels_in_protected_title':title,'changed_pixels_outside_navigation':outside,
   'selected':'Home' if key=='home' else 'Activity 3','activity_names':'Temporary neutral labels only','illustrations':'Empty translucent IMAGE placeholders only'}

old_alpha=np.asarray(Image.open(ROOT/'work/navigation-b-revision-v2/activity-overlay.png').getchannel('A'))/255
new_alpha=np.asarray(layers['activity'].getchannel('A'))/255
zone=(16,16,296,968)
x0,y0,x1,y1=zone
old_mean=float(old_alpha[y0:y1,x0:x1].mean())
new_mean=float(new_alpha[y0:y1,x0:x1].mean())
panes=[]
for b in PANE_BOXES:
 x0,y0,x1,y1=b
 a=new_alpha[y0:y1,x0:x1]
 panes.append({'bounds':b,'mean_background_transmission_percent':round(float((1-a).mean()*100),2),
               'area_with_at_least_70_percent_background_transmission_percent':round(float((a<=.3).mean()*100),2)})
report['openness_comparison']={'same_vertical_measurement_region':zone,
 'v2_background_blend_contribution_percent':round((1-old_mean)*100,2),
 'v3_background_blend_contribution_percent':round((1-new_mean)*100,2),
 'v2_alpha_coverage_percent':round(old_mean*100,2),'v3_alpha_coverage_percent':round(new_mean*100,2),
 'glass_fill_alpha':34,'glass_base_transmission_percent':round((1-34/255)*100,2),
 'individual_destination_panes':panes,'no_solid_backplate':True,'text_and_iron_core_remain_opaque':True}

sheet=Image.new('RGB',(1536,920),(19,23,28))
d=ImageDraw.Draw(sheet)
d.text((32,22),'OPTION B — IRON AND GLASS REDESIGN',font=font(26,True),fill=(224,232,228))
d.text((32,63),'Visual review only | IMAGE spaces and numbered labels remain temporary',font=font(19),fill=(174,187,192))
d.text((32,111),'Horizontal Home navigation',font=font(22,True),fill=(220,232,230))
crop=Image.open(OUT/'the-haunted-realm-navigation-b-home-redesign-review-v3-final.png').crop((0,0,1536,65))
sheet.paste(crop,(0,150))
d.text((32,252),'Rejected v2 — solid oak plaques',font=font(22,True),fill=(213,198,168))
d.text((795,252),'New v3 — scenery through aged glass',font=font(22,True),fill=(223,234,230))
for name,px in [('the-haunted-realm-navigation-b-activity-review-v2.png',32),('the-haunted-realm-navigation-b-activity-redesign-review-v3-final.png',795)]:
 crop=Image.open(OUT/name).crop((16,286,296,606))
 crop=crop.resize((470,538),Image.Resampling.LANCZOS)
 sheet.paste(crop,(px,300))
d.text((526,359),'Opaque wood',font=font(18),fill=(186,173,155))
d.text((526,391),'Scenery between',font=font(18),fill=(186,173,155))
d.text((526,423),'destinations only',font=font(18),fill=(186,173,155))
d.text((1280,359),'Clear centres',font=font(18),fill=(201,219,219))
d.text((1280,391),'Thin real iron',font=font(18),fill=(201,219,219))
d.text((1280,423),'Opaque letters',font=font(18),fill=(201,219,219))
d.text((32,870),'Protected background and title unchanged. No navigation has been implemented or approved.',font=font(19),fill=(174,186,188))
sheet.save(OUT/'the-haunted-realm-navigation-b-redesign-comparison-v3-final.png')

report['protected_hashes_after']=verify_sources()
report['all_protected_files_unchanged']=BEFORE==report['protected_hashes_after']
(OUT/'the-haunted-realm-navigation-b-redesign-verification-v3-final.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
prompts=[]
for f in WORK.glob('*-prompt.txt'):prompts.append(f.name+'\n'+f.read_text(encoding='utf-8'))
(OUT/'the-haunted-realm-navigation-b-redesign-artwork-prompts-v3-final.txt').write_text('\n\n'.join(prompts),encoding='utf-8')
print(json.dumps({'protected_files_unchanged':report['all_protected_files_unchanged'],
 'views':report['views'],'openness_comparison':report['openness_comparison']},indent=2))
