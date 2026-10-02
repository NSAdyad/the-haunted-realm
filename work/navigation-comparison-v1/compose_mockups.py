"""Produce static review PNGs only; no website or navigation implementation."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np

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

def verify_sources():
    result = {}
    for name, expected in PROTECTED.items():
        actual = hashlib.sha256((OUT / name).read_bytes()).hexdigest().upper()
        if actual != expected:
            raise RuntimeError(f'Protected asset mismatch: {name}; stopping.')
        result[name] = actual
    return result

BEFORE = verify_sources()
BASE = Image.open(OUT / 'the-haunted-realm-title-option-1-centred-review-v2.png').convert('RGBA')
SIZE = BASE.size
TITLE_BOX = (443, 65, 1093, 280)
SERIF = 'C:/Windows/Fonts/GARA.TTF'
BOLD = 'C:/Windows/Fonts/GARABD.TTF'
SMALL = 'C:/Windows/Fonts/arial.ttf'
CREAM = (230, 213, 180, 255)
GOLD = (255, 195, 99, 255)

def font(size, bold=False, sans=False):
    return ImageFont.truetype(SMALL if sans else BOLD if bold else SERIF, size)

def blank(size=SIZE):
    return Image.new('RGBA', size, (0, 0, 0, 0))

def asset(name):
    im = Image.open(WORK / name).convert('RGBA')
    bbox = im.getchannel('A').point(lambda a: 255 if a > 4 else 0).getbbox()
    return im.crop(bbox)

def fitted(im, width, height, preserve_ends=False):
    """Adapt only unapproved material artwork; retain the horizontal end fittings."""
    if not preserve_ends:
        return im.resize((width, height), Image.Resampling.LANCZOS)
    scale = height / im.height
    scaled = im.resize((round(im.width * scale), height), Image.Resampling.LANCZOS)
    end = min(round(height * .85), scaled.width // 3, width // 3)
    result = blank((width, height))
    result.alpha_composite(scaled.crop((0, 0, end, height)), (0, 0))
    result.alpha_composite(scaled.crop((scaled.width-end, 0, scaled.width, height)), (width-end, 0))
    middle = scaled.crop((end, 0, scaled.width-end, height))
    middle = middle.resize((width-2*end, height), Image.Resampling.LANCZOS)
    result.alpha_composite(middle, (end, 0))
    return result

def put_with_shadow(layer, im, x, y, box):
    shadow = blank()
    shape = im.getchannel('A').filter(ImageFilter.GaussianBlur(2))
    shaded = Image.new('RGBA', im.size, (8, 5, 10, 160))
    shaded.putalpha(shape.point(lambda a: round(a * .5)))
    shadow.alpha_composite(shaded, (x+1, y+2))
    # Nothing may leak beyond the reserved navigation area.
    clip = Image.new('L', SIZE, 0)
    ImageDraw.Draw(clip).rectangle((box[0], box[1], box[2]-1, box[3]-1), fill=255)
    shadow.putalpha(ImageChops.multiply(shadow.getchannel('A'), clip))
    layer.alpha_composite(shadow)
    layer.alpha_composite(im, (x, y))

def lettering(layer, text, x, y, size=20, selected=False, centred=False, sans=False):
    draw = ImageDraw.Draw(layer)
    f = font(size, bold=selected, sans=sans)
    box = draw.textbbox((0, 0), text, font=f)
    tw, th = box[2]-box[0], box[3]-box[1]
    if centred:
        x -= tw / 2
    y -= th / 2 + box[1]
    draw.text((round(x+1), round(y+1)), text, font=f, fill=(12, 6, 5, 255), stroke_width=1, stroke_fill=(12, 6, 5, 210))
    draw.text((round(x), round(y)), text, font=f, fill=GOLD if selected else CREAM)

def image_space(layer, x, y, size, selected=False):
    """Explicitly empty geometric placeholders, never substitute activity illustrations."""
    draw = ImageDraw.Draw(layer)
    edge = (177, 132, 72, 255) if selected else (120, 98, 73, 255)
    draw.rectangle((x, y, x+size-1, y+size-1), fill=(32, 29, 34, 235), outline=edge, width=1)
    draw.line((x+1, y+1, x+size-2, y+1), fill=(71, 67, 68, 255))
    draw.line((x+1, y+size-2, x+size-2, y+size-2), fill=(13, 12, 15, 255))
    label_size = 6 if size <= 24 else 9
    lettering(layer, 'IMAGE', x+size/2, y+size/2, label_size, centred=True, sans=True)

def warm_region(layer, rect, frame_mask=None):
    tint = blank()
    d = ImageDraw.Draw(tint)
    x0,y0,x1,y1 = rect
    d.rectangle((x0,y0,x1-1,y1-1), fill=(255, 133, 30, 35))
    d.rectangle((x0,y0,x1-1,y1-1), outline=(241, 164, 71, 195), width=1)
    d.line((x0+1,y1-2,x1-2,y1-2), fill=(113, 63, 27, 220))
    if frame_mask:
        tint.putalpha(ImageChops.multiply(tint.getchannel('A'), frame_mask))
    layer.alpha_composite(tint)

def down_chevron(layer, cx, cy, colour=CREAM):
    ImageDraw.Draw(layer).line([(cx-4, cy-2), (cx, cy+2), (cx+4, cy-2)], fill=colour, width=1)

HORIZONTAL = asset('a-horizontal-frame.png')
VERTICAL = asset('a-vertical-frame.png')
PLAQUE = asset('b-single-plaque.png')
ITEMS = ['Home'] + [f'Activity {i}' for i in range(1, 7)] + ['Activities']

def home_a():
    layer = blank()
    x,y,w,h = 16,8,1504,48
    frame = fitted(HORIZONTAL, w,h, True)
    put_with_shadow(layer, frame, x,y, (x,y,x+w,y+h))
    inner_x, inner_w = x+43, w-86
    cell = inner_w/8
    for i, label in enumerate(ITEMS):
        left = round(inner_x + i*cell)
        right = round(inner_x + (i+1)*cell)
        if i==0:
            warm_region(layer, (left+3,y+10,right-3,y+37))
        if i:
            d=ImageDraw.Draw(layer)
            d.line((left,y+12,left,y+35),fill=(130,86,44,255),width=1)
            d.line((left+1,y+12,left+1,y+35),fill=(27,17,12,255),width=1)
        if label == 'Activities':
            lettering(layer,label,(left+right)/2-7,y+25,20,centred=True)
            down_chevron(layer, right-23,y+26)
        else:
            image_space(layer,left+10,y+13,22,i==0)
            lettering(layer,label,left+40,y+25,20,i==0)
    return layer

def home_b():
    layer=blank()
    x,y,w,h,gap=16,8,1504,48,7
    cell=(w-gap*7)/8
    for i,label in enumerate(ITEMS):
        left=round(x+i*(cell+gap))
        right=round(x+i*(cell+gap)+cell)
        frame=fitted(PLAQUE,right-left,h)
        put_with_shadow(layer,frame,left,y,(left,y,right,y+h))
        if i==0:
            mask=blank()
            mask.alpha_composite(frame,(left,y))
            warm_region(layer,(left+20,y+19,right-20,y+42),mask.getchannel('A'))
        if label=='Activities':
            lettering(layer,label,(left+right)/2-6,y+31,20,centred=True)
            down_chevron(layer,right-25,y+32)
        else:
            image_space(layer,left+24,y+20,20,i==0)
            lettering(layer,label,left+51,y+31,19,i==0)
    return layer

def activity_a():
    layer=blank()
    x,y,w,h=16,16,280,952
    frame=fitted(VERTICAL,w,h)
    put_with_shadow(layer,frame,x,y,(x,y,x+w,y+h))
    lettering(layer,'Activities',x+w/2,y+30,24,centred=True)
    d=ImageDraw.Draw(layer)
    d.line((x+28,y+48,x+w-28,y+48),fill=(137,94,51,230),width=1)
    for i,label in enumerate(['Home']+[f'Activity {j}' for j in range(1,11)]):
        row_y=70+i*78
        selected=i==3
        if selected:
            warm_region(layer,(x+22,row_y+7,x+w-31,row_y+65))
        if i:
            d=ImageDraw.Draw(layer)
            d.line((x+27,row_y-2,x+w-31,row_y-2),fill=(103,69,39,200),width=1)
            d.line((x+27,row_y-1,x+w-31,row_y-1),fill=(24,16,12,180),width=1)
        image_space(layer,x+31,row_y+15,40,selected)
        lettering(layer,label,x+85,row_y+36,23,selected)
    d=ImageDraw.Draw(layer)
    # A quiet scroll cue and a list continuation control, both static.
    d.line((x+w-23,81,x+w-23,919),fill=(37,24,18,230),width=3)
    d.line((x+w-23,89,x+w-23,618),fill=(131,92,54,255),width=3)
    lettering(layer,'More activities',x+w/2-7,945,17,centred=True)
    down_chevron(layer,x+w-38,945)
    return layer

def activity_b():
    layer=blank()
    x,w=16,280
    header=fitted(PLAQUE,w,40)
    put_with_shadow(layer,header,x,16,(x,16,x+w,56))
    lettering(layer,'Activities',x+w/2,43,20,centred=True)
    for i,label in enumerate(['Home']+[f'Activity {j}' for j in range(1,11)]):
        y=64+i*78
        frame=fitted(PLAQUE,w,72)
        put_with_shadow(layer,frame,x,y,(x,y,x+w,y+72))
        selected=i==3
        if selected:
            mask=blank()
            mask.alpha_composite(frame,(x,y))
            warm_region(layer,(x+27,y+28,x+w-27,y+63),mask.getchannel('A'))
        image_space(layer,x+37,y+30,30,selected)
        lettering(layer,label,x+81,y+47,23,selected)
    footer=fitted(PLAQUE,w,40)
    put_with_shadow(layer,footer,x,928,(x,928,x+w,968))
    lettering(layer,'More activities',x+w/2-8,954,17,centred=True)
    down_chevron(layer,x+w-40,954)
    return layer

REPORT = {'kind':'Static navigation comparison PNGs only','source_hashes_before':BEFORE,'views':{}}
layers = {'a-home':home_a(), 'a-activity':activity_a(), 'b-home':home_b(), 'b-activity':activity_b()}
base_arr=np.asarray(BASE.convert('RGB'))
for key, layer in layers.items():
    im=Image.alpha_composite(BASE,layer).convert('RGB')
    name=f'the-haunted-realm-navigation-{key}-mockup-v1.png'
    path=OUT/name
    if path.exists():
        raise RuntimeError(f'Refusing to overwrite existing review: {name}')
    changed=np.any(np.asarray(im)!=base_arr,axis=2)
    allowed=np.asarray(layer.getchannel('A'))>0
    outside=int(np.count_nonzero(changed & ~allowed))
    x0,y0,x1,y1=TITLE_BOX
    title_changes=int(np.count_nonzero(changed[y0:y1,x0:x1]))
    assert outside == 0
    assert title_changes == 0
    im.save(path)
    layer.save(WORK/f'{key}-overlay.png')
    REPORT['views'][key]={'file':name,'dimensions':im.size,'navigation_bounds':layer.getbbox(),
        'changed_pixels_outside_navigation_overlay':outside,'changed_pixels_in_protected_title_rectangle':title_changes,
        'selected_entry':'Home' if 'home' in key else 'Activity 3',
        'labels':'Temporary neutral layout labels; no activity names approved',
        'image_slots':'Empty IMAGE placeholders, no activity illustration generated'}

# A closer comparison view exposes the small top-band material and label treatment.
sheet=Image.new('RGB',(1536,870),(22,20,24))
sd=ImageDraw.Draw(sheet)
sd.text((32,20),'NAVIGATION COMPARISON — DETAIL VIEW',font=font(27,True),fill=(238,216,179))
sd.text((32,60),'Static mock-ups | IMAGE = temporary reserved illustration space',font=font(20),fill=(178,168,151))
sd.text((32,108),'A — Continuous Village Rail / Home',font=font(23,True),fill=(237,208,154))
a=Image.open(OUT/'the-haunted-realm-navigation-a-home-mockup-v1.png').crop((0,0,1536,65))
sheet.paste(a,(0,145))
sd.text((32,232),'B — Individual Village Plaques / Home',font=font(23,True),fill=(237,208,154))
b=Image.open(OUT/'the-haunted-realm-navigation-b-home-mockup-v1.png').crop((0,0,1536,65))
sheet.paste(b,(0,270))
sd.text((32,357),'A — left-side activity navigation',font=font(22,True),fill=(237,208,154))
sd.text((791,357),'B — left-side activity navigation',font=font(22,True),fill=(237,208,154))
for key, px in [('a-activity',32),('b-activity',791)]:
    crop=Image.open(OUT/f'the-haunted-realm-navigation-{key}-mockup-v1.png').crop((16,222,296,624))
    crop=crop.resize((314,450),Image.Resampling.LANCZOS)
    sheet.paste(crop,(px,396))
    sd.text((px+336,431),'Activity 3',font=font(24,True),fill=(251,194,100))
    sd.text((px+336,469),'Current-page highlight',font=font(20),fill=(200,190,170))
    sd.text((px+336,535),'Empty image spaces',font=font(20),fill=(200,190,170))
    sd.text((px+336,564),'await approved artwork.',font=font(20),fill=(200,190,170))
    sd.text((px+336,630),'Neutral labels are',font=font(20),fill=(200,190,170))
    sd.text((px+336,659),'for comparison only.',font=font(20),fill=(200,190,170))
sheet.save(OUT/'the-haunted-realm-navigation-comparison-details-v1.png')

REPORT['source_hashes_after']=verify_sources()
REPORT['all_protected_files_unchanged']=REPORT['source_hashes_after']==BEFORE
REPORT['dimensions']={'home_navigation':'1504 x 48 at x=16, y=8','left_navigation':'280 x 952 at x=16, y=16',
    'title':'650 x 215 at x=443, y=65, unchanged'}
(OUT/'the-haunted-realm-navigation-comparison-verification-v1.json').write_text(json.dumps(REPORT,indent=2),encoding='utf-8')
prompts=[]
for filename in ('a-horizontal-frame-prompt.txt','a-vertical-frame-prompt.txt','b-single-plaque-prompt.txt'):
    prompts.append(filename+'\n'+'='*len(filename)+'\n'+(WORK/filename).read_text(encoding='utf-8')+'\n')
(OUT/'the-haunted-realm-navigation-comparison-artwork-prompts-v1.txt').write_text('\n'.join(prompts),encoding='utf-8')
print(json.dumps({'output_views':list(REPORT['views']),'protected_files_unchanged':REPORT['all_protected_files_unchanged'],
                  'title_changed_pixels':{k:v['changed_pixels_in_protected_title_rectangle'] for k,v in REPORT['views'].items()},
                  'outside_navigation_changed_pixels':{k:v['changed_pixels_outside_navigation_overlay'] for k,v in REPORT['views'].items()}},indent=2))
