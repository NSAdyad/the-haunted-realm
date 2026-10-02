"""Deterministic raster lettering studies; no browser or website code."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter

S=3
FONT='C:/Windows/Fonts/CASTELAR.TTF'
NAMES=['ECHOES OF THE PAST','THE CURSED QUEST','THE BOOK OF SHADOWS','FASTEST FINGER FIRST',
 'WORDS OF THE FEAST','THE PHANTOM ORDER','DOOR TO DARKNESS','BUILD THE HAUNTED BANQUET','HOTEL TRANSYLVANIA']
LINES=[[n] for n in NAMES]
LINES[7]=['BUILD THE HAUNTED','BANQUET']
assert [' '.join(v) for v in LINES]==NAMES
PALETTE=[(215,218,211),(224,229,231),(213,220,225),(240,233,216),
 (242,222,188),(214,232,236),(215,225,232),(231,223,202),(244,229,196)]
HALO=[(93,123,145),(126,130,156),(117,121,157),(153,138,112),
 (169,126,75),(92,148,163),(99,132,164),(145,133,113),(176,137,81)]

def shift(a,dx,dy):
 out=np.zeros_like(a);h,w=a.shape
 x0=max(0,dx);x1=min(w,w+dx);y0=max(0,dy);y1=min(h,h+dy)
 if x1>x0 and y1>y0:out[y0:y1,x0:x1]=a[y0-dy:y1-dy,x0-dx:x1-dx]
 return out

def coloured(mask,rgb,amount=1):
 alpha=np.clip(np.asarray(mask,dtype=np.float32)*amount,0,255).astype(np.uint8)
 out=Image.new('RGBA',mask.size,tuple(rgb)+(0,));out.putalpha(Image.fromarray(alpha));return out

def make_name(index,size=29,focus=False,width=440,lines=None):
 lines=LINES[index] if lines is None else lines
 height=104 if len(lines)>1 else 80
 wh=(width*S,height*S)
 mask=Image.new('L',wh,0);d=ImageDraw.Draw(mask)
 f=ImageFont.truetype(FONT,size*S)
 spacing=.32*S
 widths=[]
 line_step=34*S
 for row,line in enumerate(lines):
  extent=sum(f.getlength(c) for c in line)+spacing*(len(line)-1)
  assert extent<(width-20)*S,(line,extent/S,width)
  widths.append(extent/S)
  b=d.textbbox((0,0),line,font=f)
  cy=wh[1]/2+(row-(len(lines)-1)/2)*line_step
  y=round(cy-(b[3]-b[1])/2-b[1]);x=(wh[0]-extent)/2
  for c in line:
   d.text((round(x),y),c,font=f,fill=255,stroke_width=1,stroke_fill=255)
   x+=f.getlength(c)+spacing
 a=np.asarray(mask,dtype=np.float32)
 result=Image.new('RGBA',wh,(0,0,0,0))
 # Shadows/illumination are glyph shaped, not an opaque caption panel or button.
 shadow=mask.filter(ImageFilter.GaussianBlur(2.2*S))
 result.alpha_composite(coloured(Image.fromarray(shift(np.asarray(shadow),0,2*S)),(2,5,10),1.4))
 halo=mask.filter(ImageFilter.GaussianBlur(1.8*S if index==3 else 3.0*S))
 result.alpha_composite(coloured(halo,HALO[index],.95 if focus else .72))
 if index in (0,1,2,5,6,8):
  echo=mask.filter(ImageFilter.GaussianBlur(.9*S))
  echo=Image.fromarray(shift(np.asarray(echo),(2 if index in (0,5) else -2)*S,-2*S))
  result.alpha_composite(coloured(echo,HALO[index],.39 if focus else .26))
 # Quiet mist wisps below letter feet; primary glyphs always remain solid.
 fog=Image.new('L',wh,0);fd=ImageDraw.Draw(fog)
 rng=np.random.default_rng(937+index)
 actual=max(widths)*S
 for k in range(10):
  cx=wh[0]/2+rng.uniform(-.4,.4)*actual
  cy=wh[1]/2+size*S*.32+rng.uniform(-2,5)*S
  rx=rng.uniform(10,29)*S;ry=rng.uniform(1.4,3.2)*S
  fd.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=int(rng.uniform(55,110)))
 fog=fog.filter(ImageFilter.GaussianBlur(1.8*S))
 result.alpha_composite(coloured(fog,HALO[index],.58 if focus else .90))
 # Subtle dark engraved depth, micro-weathering and directional cut-edge light.
 for dy in (3,2,1):
  result.alpha_composite(coloured(Image.fromarray(shift(a,S,dy*S).astype(np.uint8)),(25,29,36),.94))
 yy=np.indices(a.shape)[0].astype(np.float32)/max(1,wh[1]-1)
 grain=rng.normal(0,5.6,a.shape)
 scratch=Image.fromarray(rng.integers(0,255,a.shape,dtype=np.uint8)).filter(ImageFilter.GaussianBlur(.32*S))
 wear=(np.asarray(scratch,dtype=np.float32)-128)*.24
 hi=np.maximum(0,a-shift(a,S,S))/255
 lo=np.maximum(0,a-shift(a,-S,-S))/255
 rgb=np.empty((*a.shape,3),dtype=np.uint8)
 for ch,c in enumerate(PALETTE[index]):
  local_y=np.mod(yy*wh[1]-wh[1]/2+size*S/2+line_step/2,line_step)/line_step
  value=c+28*np.cos(local_y*np.pi*1.35)-8+grain+wear+hi*25-lo*48
  if focus:value+=10+(4 if index in (3,4,8) else 0)
  rgb[:,:,ch]=np.clip(value,125,255).astype(np.uint8)
 face=Image.fromarray(rgb,'RGB').convert('RGBA');face.putalpha(mask)
 result.alpha_composite(face)
 scratches=Image.new('L',wh,0);sd=ImageDraw.Draw(scratches)
 for k in range(10):
  x=rng.uniform(wh[0]*.1,wh[0]*.9);y=rng.uniform(wh[1]/2-size*S*.34,wh[1]/2+size*S*.34)
  sd.line((x,y,x+rng.uniform(3,9)*S,y+rng.uniform(-.8,.8)*S),fill=70,width=1)
 scratch_alpha=np.minimum(np.asarray(scratches),a*.38).astype(np.uint8)
 result.alpha_composite(coloured(Image.fromarray(scratch_alpha),(70,75,80),.7))
 foreground=np.asarray(fog,dtype=np.float32)*np.clip(a/255,0,1)*.30
 result.alpha_composite(coloured(Image.fromarray(foreground.astype(np.uint8)),HALO[index],.48 if focus else .66))
 result=result.resize((width,height),Image.Resampling.LANCZOS)
 return result,{'exact_name':NAMES[index],'font_family':'Castelar engraved capitals','font_size':size,
  'line_widths':widths,'glyphs_opaque':True,'generated_text':False,
  'treatment':'etched weathered spectral inscription; directional depth, scuffs, mist and reflected local light',
  'focus_method':'same glyph geometry, mist and texture; controlled luminance only'}

def proof(folder):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
 canvas=Image.new('RGB',(1100,1210),(20,24,34))
 d=ImageDraw.Draw(canvas);caption=ImageFont.truetype('C:/Windows/Fonts/georgia.ttf',17)
 d.text((32,22),'HAUNTED ACTIVITY LETTERING — EXACT WORDING / ONE SHARED FAMILY',font=caption,fill=(229,230,221))
 d.text((34,62),'Resting',font=caption,fill=(214,223,230))
 d.text((582,62),'Controlled hover/focus light study',font=caption,fill=(246,220,174))
 data=[]
 for i in range(9):
  y=100+i*120
  for focus,x in [(False,26),(True,574)]:
   art,meta=make_name(i,focus=focus)
   canvas.paste(art,(x,y),art)
   art.save(folder/f'name-{i+1:02d}-{"focus" if focus else "rest"}.png')
  data.append(meta)
 canvas.save(folder/'lettering-proof.png')
 return data

if __name__=='__main__':
 import json
 folder=Path(__file__).resolve().parent
 # Keep name files in the working area; they are unapproved review artwork.
 data=[]
 canvas=Image.new('RGB',(1100,1210),(20,24,34));d=ImageDraw.Draw(canvas)
 f=ImageFont.truetype('C:/Windows/Fonts/georgia.ttf',17)
 d.text((28,22),'SPECTRAL INSCRIPTIONS — EXACT WORDING / ONE ENGRAVED FAMILY',font=f,fill=(228,230,220))
 d.text((28,62),'Resting',font=f,fill=(218,224,231));d.text((580,62),'Controlled hover/focus light',font=f,fill=(243,218,178))
 for i in range(9):
  for selected,x in [(False,26),(True,574)]:
   art,meta=make_name(i,focus=selected)
   art.save(folder/f'name-{i+1:02d}-{"focus" if selected else "rest"}.png')
   canvas.paste(art,(x,98+i*120),art)
  data.append(meta)
 canvas.save(folder/'lettering-proof-etched.png')
 (folder/'lettering-metadata.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
 print('Nine exact uppercase names rendered with one spectral engraved family. No website code.')
