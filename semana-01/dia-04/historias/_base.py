# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps
OUT = os.path.dirname(os.path.abspath(__file__))
F = "C:/Users/PC/video-editor/assets/fonts/"
W, H = 1080, 1920
BG=(7,10,28); VIO=(91,91,245); LAV=(169,156,255); CRE=(246,242,234); LIM=(198,244,50); CARD=(18,22,52)
FN={"black":"Inter-Black.otf","bold":"Inter-Bold.otf","reg":"Inter-Regular.otf","play":"PlayfairDisplay-Italic-VF.ttf","mono":"IBMPlexMono-Bold.ttf","heros":"texgyreheros-bold.otf"}
def f(n,s): return ImageFont.truetype(F+FN[n],s)
def base(glow=(540,800),col=(40,36,130),stripes=False):
    im=Image.new("RGB",(W,H),BG); g=Image.new("RGB",(W,H),0); d=ImageDraw.Draw(g)
    d.ellipse((glow[0]-520,glow[1]-520,glow[0]+520,glow[1]+520),fill=col)
    im=ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(220))); d=ImageDraw.Draw(im)
    if stripes:
        for x in range(-H,W,90): d.line((x,0,x+H,H),fill=(16,20,48),width=2)
    else:
        for x in range(30,W,60):
            for y in range(30,H,60): d.point((x,y),fill=(30,34,74))
    return im
def star(d,cx,cy,r,col=VIO):
    d.polygon([(cx+(r if i%2==0 else r*.28)*math.cos(-math.pi/2+i*math.pi/4),cy+(r if i%2==0 else r*.28)*math.sin(-math.pi/2+i*math.pi/4)) for i in range(8)],fill=col)
def sign(d,c="tr"): star(d,*{"tr":(960,280),"tl":(120,280),"br":(960,1560),"bl":(120,1560)}[c],40)
def tw(d,t,fo): return d.textlength(t,font=fo)
def center(d,y,t,fo,col=CRE,sp=10):
    for ln in t.split("\n"):
        d.text(((W-tw(d,ln,fo))/2,y),ln,font=fo,fill=col); y+=fo.size+sp
    return y
def left(d,x,y,t,fo,col=CRE,sp=10):
    for ln in t.split("\n"): d.text((x,y),ln,font=fo,fill=col); y+=fo.size+sp
    return y
def pill(d,y,t,fo,fill=VIO,col=CRE,x=None):
    pw=tw(d,t,fo)+60; x=(W-pw)/2 if x is None else x
    d.rounded_rectangle((x,y,x+pw,y+fo.size+34),(fo.size+34)//2,fill=fill); d.text((x+30,y+15),t,font=fo,fill=col)
def hole(d,box,lbl="Pega aquí el reel"):
    x0,y0,x1,y1=box
    d.rounded_rectangle((x0-10,y0-10,x1+10,y1+10),44,outline=VIO,width=6)
    d.rounded_rectangle(box,36,fill=(14,17,42))
    center(d,y0+(y1-y0)//2-20,lbl,f("mono",30),LAV)
def bot_icon(d,cx,cy,s):
    d.rounded_rectangle((cx-s,cy-s*.6,cx+s,cy+s*.7),s*.3,outline=CRE,width=int(s*.1))
    d.line((cx,cy-s*.6,cx,cy-s),fill=CRE,width=int(s*.08)); d.ellipse((cx-s*.14,cy-s*1.14,cx+s*.14,cy-s*.86),fill=LIM)
    d.ellipse((cx-s*.55,cy-s*.2,cx-s*.2,cy+s*.15),fill=LAV); d.ellipse((cx+s*.2,cy-s*.2,cx+s*.55,cy+s*.15),fill=LAV)
