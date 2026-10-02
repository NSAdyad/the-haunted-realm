"""Raster-only Option B review. No website/navigation code is produced."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
OUT = ROOT / 'outputs'
PROTECTED = {
    'the-haunted-realm-background-corrected-review-v3.png': '1561627199D2DA3412C5D5E49143A6B699201659AD1CEE56A38CEB8E96F28C06',
    'the-haunted-realm-background-review-v1.png': '63392BF751F4C5518A26E9D82188C3C29CDCEB61B9A50C6E8F2F32BB34BC668F',
    'the-haunted-realm-title-approved.png': '5F3DB4E9112D076A73E22587FCAEE26022B2188993A1DB6ABBB7A912ABF68A4A',
    'the-haunted-realm-title-option-1-centred-review-v2.png': '1A4B8C14C4229B0C2E68DB47086B0A741C667930B16E531DCB2455905A0C7942',
    'the-haunted-realm-title-original-artwork-backup.png': 'D40B8107D55723CD6976C880905564458DCA17082D55AAAF7F561D6DC6D3F7C1',
}

def source_hashes():
    hashes = {}
    for name, expected in PROTECTED.items():
        actual = hashlib.sha256((OUT/name).read_bytes()).hexdigest().upper()
        if actual != expected:
            raise RuntimeError(f'Protected file hash mismatch: {name}; stopping.')
        hashes[name] = actual
    return hashes

BEFORE = source_hashes()
BASE = Image.open(OUT/'the-haunted-realm-title-option-1-centred-review-v2.png').convert('RGBA')
SIZE = BASE.size
TITLE = (443,65,1093,280)
CREAM = (226,214,188,255)
AMBER = (255,204,115,255)
REGULAR = 'C:/Windows/Fonts/GARA.TTF'
BOLD = 'C:/Windows/Fonts/GARABD.TTF'
SANS = 'C:/Windows/Fonts/arial.ttf'

def blank(size=SIZE):
    return Image.new('RGBA',size,(0,0,0,0))

def face(size, bold=False, sans=False):
    return ImageFont.truetype(SANS if sans else BOLD if bold else REGULAR,size)

def tight_asset(filename):
    im=Image.open(WORK/filename).convert('RGBA')
    # Normalize generation alpha dust on the new, unapproved materials only.
    # Keep genuine antialiasing; make the near-opaque material core opaque.
    im.putalpha(im.getchannel('A').point(lambda a:0 if a<=4 else 255 if a>=250 else a))
    box=im.getchannel('A').point(lambda a:255 if a>4 else 0).getbbox()
    if box is None:
        raise RuntimeError(f'Empty asset: {filename}')
    return im.crop(box)

def text(layer, value, x, y, size, selected=False, centred=False, sans=False):
    f=face(size,selected,sans)
    d=ImageDraw.Draw(layer)
    box=d.textbbox((0,0),value,font=f)
    if centred:
        x-=(box[2]-box[0])/2
    y-=(box[3]-box[1])/2+box[1]
    d.text((round(x+1),round(y+1)),value,font=f,fill=(9,6,8,255),stroke_width=1,stroke_fill=(9,6,8,210))
    d.text((round(x),round(y)),value,font=f,fill=AMBER if selected else CREAM)

def placeholder(layer,x,y,size,selected=False):
    d=ImageDraw.Draw(layer)
    border=(177,134,76,255) if selected else (102,92,77,255)
    d.rectangle((x,y,x+size-1,y+size-1),fill=(24,24,31,245),outline=border,width=1)
    d.line((x+1,y+1,x+size-2,y+1),fill=(53,50,55,255))
    label=6 if size<28 else 8
    text(layer,'IMAGE',x+size/2,y+size/2,label,centred=True,sans=True)

def chevron(layer,x,y):
    ImageDraw.Draw(layer).line([(x-4,y-2),(x,y+2),(x+4,y-2)],fill=CREAM,width=1)

def warm_lantern_light(im):
    """A soft local wash retains the wood and metal detail; no selected-button box."""
    arr=np.asarray(im).copy()
    h,w=arr.shape[:2]
    yy,xx=np.mgrid[0:h,0:w]
    wash=np.exp(-(((xx-w*.29)/(w*.46))**2+((yy-h*.73)/(h*.57))**2))
    a=(wash*52).astype('uint8')
    a=(a.astype('uint16')*arr[:,:,3].astype('uint16')//255).astype('uint8')
    light=Image.new('RGBA',im.size,(255,142,39,0))
    light.putalpha(Image.fromarray(a))
    return Image.alpha_composite(im,light)

def place_material(layer,im,x,y,box,selected=False):
    if selected:
        im=warm_lantern_light(im)
    shape=im.getchannel('A')
    shadow=Image.new('RGBA',im.size,(7,6,12,0))
    shadow.putalpha(shape.filter(ImageFilter.GaussianBlur(1.3)).point(lambda a:round(a*.42)))
    temp=blank()
    temp.alpha_composite(shadow,(x+1,y+2))
    clip=Image.new('L',SIZE,0)
    ImageDraw.Draw(clip).rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=255)
    temp.putalpha(ImageChops.multiply(temp.getchannel('A'),clip))
    layer.alpha_composite(temp)
    layer.alpha_composite(im,(x,y))

PLAQUE = tight_asset('plaque-material.png')
CHAINS = tight_asset('chain-supports.png')

def plate(width,height):
    return PLAQUE.resize((width,height),Image.Resampling.LANCZOS)

def horizontal():
    layer=blank()
    labels=['Home']+[f'Activity {i}' for i in range(1,7)]+['Activities']
    x,y,w,h,gap=16,8,1504,48,7
    unit=(w-7*gap)/8
    for i,label in enumerate(labels):
        left=round(x+i*(unit+gap))
        right=round(left+unit)
        material=plate(right-left,h)
        selected=i==0
        place_material(layer,material,left,y,(left,y,right,y+h),selected)
        if label=='Activities':
            text(layer,label,(left+right)/2-7,y+29,20,centred=True)
            chevron(layer,right-24,y+30)
        else:
            placeholder(layer,left+25,y+18,22,selected)
            text(layer,label,left+54,y+29,19,selected)
    return layer

def vertical():
    layer=blank()
    x,w=16,280
    # The alpha opening between these chains is empty: no rectangular backing.
    supports=CHAINS.resize((244,907),Image.Resampling.LANCZOS)
    layer.alpha_composite(supports,(34,30))
    header=plate(w,44)
    place_material(layer,header,x,16,(x,16,x+w,60))
    text(layer,'Activities',x+w/2,44,20,centred=True)
    labels=['Home']+[f'Activity {i}' for i in range(1,7)]
    for i,label in enumerate(labels):
        y=82+i*110
        selected=i==3
        material=plate(w,72)
        place_material(layer,material,x,y,(x,y,x+w,y+72),selected)
        placeholder(layer,x+39,y+26,36,selected)
        text(layer,label,x+89,y+45,24,selected)
    footer=plate(w,48)
    place_material(layer,footer,x,918,(x,918,x+w,966))
    text(layer,'More activities',x+w/2-8,948,18,centred=True)
    chevron(layer,x+w-35,948)
    return layer

layers={'home':horizontal(),'activity':vertical()}
report={'scope':'Option B visual revision only; static PNG review; no navigation implementation',
    'protected_hashes_before':BEFORE,'views':{}}
base_pixels=np.asarray(BASE.convert('RGB'))
for key,layer in layers.items():
    result=Image.alpha_composite(BASE,layer).convert('RGB')
    path=OUT/f'the-haunted-realm-navigation-b-{key}-review-v2.png'
    if path.exists():
        if not np.array_equal(np.asarray(Image.open(path).convert('RGB')),np.asarray(result)):
            raise RuntimeError(f'Refusing to overwrite a different review file: {path}')
    changed=np.any(np.asarray(result)!=base_pixels,axis=2)
    allowed=np.asarray(layer.getchannel('A'))>0
    x0,y0,x1,y1=TITLE
    outside=int(np.count_nonzero(changed & ~allowed))
    title_changes=int(np.count_nonzero(changed[y0:y1,x0:x1]))
    assert outside==0 and title_changes==0
    if not path.exists():
        result.save(path)
    layer.save(WORK/f'{key}-overlay.png')
    report['views'][key]={'file':str(path),'size':result.size,'navigation_bounds':layer.getbbox(),
        'changed_pixels_outside_navigation_overlay':outside,'changed_pixels_in_protected_title_rectangle':title_changes,
        'selected_label':'Home' if key=='home' else 'Activity 3',
        'labels':'Temporary neutral labels only','image_placeholders':'Empty labeled IMAGE slots; no final illustrations'}

old=Image.open(ROOT/'work/navigation-comparison-v1/b-activity-overlay.png').getchannel('A')
new=layers['activity'].getchannel('A')
box=(16,16,296,968)
old_a=np.asarray(old.crop(box))/255
new_a=np.asarray(new.crop(box))/255
report['vertical_openness']={
    'measurement_box':box,
    'previous_alpha_weighted_coverage_percent':round(float(old_a.mean()*100),2),
    'revised_alpha_weighted_coverage_percent':round(float(new_a.mean()*100),2),
    'previous_fully_uncovered_area_percent':round(float((old_a==0).mean()*100),2),
    'revised_fully_uncovered_area_percent':round(float((new_a==0).mean()*100),2),
    'opaque_backing_panel':False,'visible_example_destinations':7,
    'example_plaque_size':[280,72],'example_row_pitch':110,'space_between_plaque_bounds':38,
}

sheet=Image.new('RGB',(1536,940),(21,20,25))
d=ImageDraw.Draw(sheet)
d.text((32,22),'OPTION B — REVISED INDIVIDUAL VILLAGE PLAQUES',font=face(28,True),fill=(230,215,185))
d.text((32,65),'Static review only | IMAGE = temporary reserved illustration space',font=face(20),fill=(181,175,163))
d.text((32,115),'Horizontal Home navigation',font=face(24,True),fill=(233,203,157))
top=Image.open(OUT/'the-haunted-realm-navigation-b-home-review-v2.png').crop((0,0,1536,65))
sheet.paste(top,(0,156))
d.text((32,250),'Previous vertical treatment',font=face(23,True),fill=(210,199,177))
d.text((790,250),'Revised open vertical treatment',font=face(23,True),fill=(241,203,146))
old_crop=Image.open(OUT/'the-haunted-realm-navigation-b-activity-mockup-v1.png').crop((16,222,296,624))
old_crop=old_crop.resize((314,450),Image.Resampling.LANCZOS)
sheet.paste(old_crop,(32,300))
new_crop=Image.open(OUT/'the-haunted-realm-navigation-b-activity-review-v2.png').crop((16,256,296,826))
new_crop=new_crop.resize((314,639),Image.Resampling.LANCZOS)
sheet.paste(new_crop,(790,280))
for value,yy in [('Tighter row spacing',342),('More repeated plaque surface',380),('Temporary IMAGE slots',470)]:
    d.text((373,yy),value,font=face(20),fill=(189,180,165))
for value,yy in [('Wider open gaps',342),('Sparse chain supports',380),('Blackened iron / aged oak',440),('Local amber illumination',490),('Temporary IMAGE slots',590)]:
    d.text((1124,yy),value,font=face(20),fill=(212,195,168))
sheet.save(OUT/'the-haunted-realm-navigation-b-revision-details-v2.png')

after=source_hashes()
report['protected_hashes_after']=after
report['protected_files_unchanged']=BEFORE==after
(OUT/'the-haunted-realm-navigation-b-revision-verification-v2.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
prompt_parts=[]
for name in ['plaque-material-prompt.txt','chain-supports-prompt.txt']:
    prompt_parts.append(name+'\n'+(WORK/name).read_text(encoding='utf-8'))
(OUT/'the-haunted-realm-navigation-b-revision-artwork-prompts-v2.txt').write_text('\n\n'.join(prompt_parts),encoding='utf-8')
print(json.dumps({'protected_files_unchanged':report['protected_files_unchanged'],
    'zero_title_changes':all(v['changed_pixels_in_protected_title_rectangle']==0 for v in report['views'].values()),
    'zero_changes_outside_navigation':all(v['changed_pixels_outside_navigation_overlay']==0 for v in report['views'].values()),
    'vertical_openness':report['vertical_openness']},indent=2))
