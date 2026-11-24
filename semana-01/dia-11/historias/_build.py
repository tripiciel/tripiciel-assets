# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
# Historias dia 11 (estilo v2 oscuro premium). Usa los fotogramas de los reels si existen;
# si no, dibuja un provisorio en el mismo estilo.
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = "C:/Users/PC/tripiciel-assets/semana-01/"
REEL1 = ROOT + "dia-11/reels/reel-1/fotograma.jpg"
REEL2 = ROOT + "dia-11/reels/reel-2/fotograma.jpg"
ISO = ROOT + "dia-01/reels/reel-4/isotipo.png"
F = "C:/Users/PC/video-editor/assets/fonts/"
W, H = 1080, 1920
VIO=(91,91,245); LAV=(169,156,255); CRE=(246,242,234); LIM=(198,244,50); GRY=(196,196,206)
FN={"black":"Inter-Black.otf","bold":"Inter-Bold.otf","reg":"Inter-Regular.otf","play":"PlayfairDisplay-Italic-VF.ttf","mono":"IBMPlexMono-Bold.ttf"}
def f(n,s): return ImageFont.truetype(F+FN[n],s)
USED = {}

def bg(tint=(10,6,26), glow=(540,900), gcol=(60,40,150), seed=1):
    rnd = random.Random(seed)
    im = Image.new("RGB",(W,H),tint)
    g = Image.new("RGB",(W,H),0); d = ImageDraw.Draw(g)
    d.ellipse((glow[0]-560,glow[1]-620,glow[0]+560,glow[1]+620),fill=gcol)
    im = ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(260)))
    bk = Image.new("RGB",(W,H),0); d = ImageDraw.Draw(bk)
    for _ in range(26):
        x,y,r = rnd.randint(0,W),rnd.randint(0,H),rnd.randint(14,60)
        c = rnd.choice([VIO,LAV,(90,70,200),(60,90,70)]); k = rnd.uniform(.12,.35)
        d.ellipse((x-r,y-r,x+r,y+r),fill=tuple(int(v*k) for v in c))
    im = ImageChops.add(im,bk.filter(ImageFilter.GaussianBlur(9)))
    return vignette(im)

def vignette(im, k=.78):
    m = Image.new("L",(W,H),0); d = ImageDraw.Draw(m)
    d.ellipse((-260,-160,W+260,H+160),fill=255)
    m = m.filter(ImageFilter.GaussianBlur(240))
    dark = Image.new("RGB",(W,H),(0,0,0))
    out = Image.composite(im,dark,m)
    return Image.blend(im,out,k)

def tw(d,t,fo): return d.textlength(t,font=fo)
def center(d,y,t,fo,col=CRE):
    d.text(((W-tw(d,t,fo))/2,y),t,font=fo,fill=col)
def runs(d,y,parts,size=54):
    # parts: [(texto, acento?)] centrados en una linea
    fo_r, fo_b = f("bold",size), f("black",size)
    tot = sum(tw(d,t,fo_b if a else fo_r) for t,a in parts); x = (W-tot)/2
    for t,a in parts:
        fo = fo_b if a else fo_r; d.text((x,y),t,font=fo,fill=a if a else CRE); x += tw(d,t,fo)

def shadow_paste(im, src, pos, mask=None, blur=40, off=(0,30), op=170):
    sh = Image.new("L",im.size,0)
    m = mask if mask else Image.new("L",src.size,255)
    sh.paste(m.point(lambda v: v*op//255),(pos[0]+off[0],pos[1]+off[1]))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.new("RGB",im.size,0),(0,0),sh)
    im.paste(src,pos,m)

def logo(im, corner="tl"):
    iso = Image.open(ISO).convert("RGBA"); s = 74
    iso = iso.resize((s, int(iso.height*s/iso.width)), Image.LANCZOS)
    im.paste(iso, (70, 230) if corner=="tl" else (W-70-s, 230), iso)

def framed(im, frame, box, r=46):
    x0,y0,x1,y1 = box; bw,bh = x1-x0,y1-y0
    sc = max(bw/frame.width, bh/frame.height)
    fr = frame.resize((int(frame.width*sc+.5),int(frame.height*sc+.5)),Image.LANCZOS)
    l,t = (fr.width-bw)//2,(fr.height-bh)//2; fr = fr.crop((l,t,l+bw,t+bh))
    m = Image.new("L",(bw,bh),0); ImageDraw.Draw(m).rounded_rectangle((0,0,bw-1,bh-1),r,fill=255)
    # halo de luz violeta detras
    g = Image.new("RGB",im.size,0); ImageDraw.Draw(g).rounded_rectangle((x0-20,y0-20,x1+20,y1+20),r+20,fill=(60,50,170))
    im.paste(ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(70))))
    shadow_paste(im, fr, (x0,y0), m, blur=50, off=(0,40), op=220)
    gl = Image.new("RGBA",(bw,bh),(0,0,0,0)); gd = ImageDraw.Draw(gl)
    for i in range(bh//2):  # reflejo suave arriba
        gd.line((0,i,bw,i),fill=(255,255,255,int(26*(1-i/(bh/2)))))
    gl.putalpha(ImageChops.multiply(gl.getchannel("A"),m)); im.paste(gl,(x0,y0),gl)
    ImageDraw.Draw(im).rounded_rectangle(box,r,outline=(120,110,230),width=3)

def get_frame(path, fallback, key):
    if os.path.exists(path):
        USED[key] = "real"; return Image.open(path).convert("RGB")
    USED[key] = "PROVISORIO"; return fallback()

def cta_pill(im, y, text):
    d = ImageDraw.Draw(im); fo = f("bold",40); pw = tw(d,text,fo)+150; x = (W-pw)/2
    d.rounded_rectangle((x,y,x+pw,y+90),45,outline=LAV,width=3,fill=(22,18,52))
    d.text((x+44,y+22),text,font=fo,fill=CRE)
    ax = x+pw-62; d.line((ax-24,y+45,ax+12,y+45),fill=LAV,width=5); d.polygon([(ax+24,y+45),(ax+4,y+30),(ax+4,y+60)],fill=LAV)

def _glow(im, box, col, blur):
    g = Image.new("RGB",im.size,0); ImageDraw.Draw(g).ellipse(box,fill=col)
    return ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(blur)))

def vignette_s(im):
    m = Image.new("L",im.size,0); ImageDraw.Draw(m).ellipse((-150,-100,im.width+150,im.height+100),fill=255)
    return Image.composite(im,Image.new("RGB",im.size,0),m.filter(ImageFilter.GaussianBlur(160)))
def option(im, box, label, col):
    x0,y0,x1,y1 = box; w,h = x1-x0,y1-y0
    card = Image.new("RGB",(w,h),(20,18,44)); cd = ImageDraw.Draw(card)
    for i in range(h): cd.line((0,i,w,i),fill=(int(30-14*i/h),int(26-12*i/h),int(66-28*i/h)))
    m = Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),40,fill=255)
    g = Image.new("RGB",im.size,0); ImageDraw.Draw(g).rounded_rectangle((x0,y0,x1,y1),40,fill=tuple(v//3 for v in col))
    im.paste(ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(60))))
    shadow_paste(im,card,(x0,y0),m,blur=36,off=(0,30),op=230)
    d = ImageDraw.Draw(im); d.rounded_rectangle(box,40,outline=col,width=3)
    d.line((x0+40,y0+3,x1-40,y0+3),fill=tuple(min(255,v+60) for v in col),width=2)
    fo = f("black",120); d.text((x0+(w-tw(d,label,fo))/2,y0+h/2-78),label,font=fo,fill=CRE)

# ---------- provisorios dia 10 ----------
CARR = ROOT + "dia-11/carrusel/slide-01.jpg"

def _drop(im, s, p, blur=30, off=(16,40), op=2/3):
    sh = Image.new("L",im.size,0); sh.paste(s.getchannel("A").point(lambda v:int(v*op)),(p[0]+off[0],p[1]+off[1]))
    im.paste(Image.new("RGB",im.size,0),(0,0),sh.filter(ImageFilter.GaussianBlur(blur))); im.paste(s,p,s)

def prov_chair():
    # mostrador de madera con luz calida; una silla que se aleja hacia la oscuridad
    w,h = 900,1000
    im = Image.new("RGB",(w,h),(8,7,12)); d = ImageDraw.Draw(im)
    d.rectangle((0,700,w,h),fill=(18,15,14))
    im = _glow(im,(60,200,560,760),(130,100,55),110)
    s = Image.new("RGBA",(w,h),(0,0,0,0)); sd = ImageDraw.Draw(s)
    sd.rectangle((40,430,470,760),fill=(96,64,38,255)); sd.rectangle((20,400,490,440),fill=(140,98,60,255))
    for y in range(450,760,26): sd.line((40,y,470,y+6),fill=(84,56,32,255),width=3)
    sd.line((20,402,490,402),fill=(214,180,130,255),width=3)
    sd.rectangle((330,330,420,400),fill=(246,242,234,255)); sd.rectangle((330,330,420,346),fill=(91,91,245,255))
    _drop(im,s,(0,0),20,(10,20))
    for (cx,cy,k,a) in [(760,680,.6,70),(730,692,.64,130),(700,706,.7,255)]:
        c = Image.new("RGBA",(w,h),(0,0,0,0)); cd = ImageDraw.Draw(c); col=(150,110,70,a); lt=(205,170,120,a)
        sw = int(150*k); sh_ = int(300*k)
        cd.rectangle((cx-sw//2,cy-sh_,cx+sw//2,cy-sh_+int(24*k)),fill=lt)
        cd.rectangle((cx-sw//2,cy-sh_,cx-sw//2+int(14*k),cy),fill=col)
        cd.rectangle((cx+sw//2-int(14*k),cy-sh_,cx+sw//2,cy),fill=col)
        cd.rectangle((cx-sw//2,cy-int(130*k),cx+sw//2,cy-int(110*k)),fill=lt)
        if a<255: c = c.filter(ImageFilter.GaussianBlur(6))
        im.paste(c,(0,0),c)
    im = _glow(im,(560,520,880,760),(30,26,70),60)
    return vignette_s(im.filter(ImageFilter.GaussianBlur(.7)))

def prov_scale():
    # balanza de platos con luz calida; monedas que se caen del plato bajo
    w,h = 900,1000
    im = Image.new("RGB",(w,h),(8,7,14)); im = _glow(im,(200,180,700,780),(120,96,50),120)
    s = Image.new("RGBA",(w,h),(0,0,0,0)); d = ImageDraw.Draw(s)
    gold=(214,182,110,255); dk=(150,120,66,255)
    d.rectangle((440,260,460,800),fill=gold); d.ellipse((330,790,570,840),fill=dk)
    d.line((200,360,700,260),fill=gold,width=14); d.ellipse((432,290,468,326),fill=(246,242,234,255))
    d.line((200,360,150,560),fill=dk,width=4); d.line((200,360,250,560),fill=dk,width=4)
    d.line((700,260,650,420),fill=dk,width=4); d.line((700,260,750,420),fill=dk,width=4)
    d.chord((100,520,300,600),0,180,fill=gold); d.chord((600,380,800,460),0,180,fill=gold)
    for i in range(6): d.ellipse((150+i*3,540-i*12,250-i*3,560-i*12),fill=(230,200,120,255),outline=dk)
    _drop(im,s,(0,0),28,(14,30))
    for (x,y,r) in [(300,640,22),(330,720,20),(290,800,24),(350,880,22)]:
        c = Image.new("RGBA",(w,h),(0,0,0,0)); cd = ImageDraw.Draw(c)
        cd.ellipse((x-r,y-r//2,x+r,y+r//2),fill=(230,200,120,255),outline=(150,120,66,255),width=3)
        c = c.filter(ImageFilter.GaussianBlur(2)); im.paste(c,(0,0),c)
    im = _glow(im,(560,180,860,440),(40,34,90),70)
    return vignette_s(im.filter(ImageFilter.GaussianBlur(.7)))

def prov_cover():
    # portada provisoria del carrusel: etiqueta de precio crema intacta con un 7
    w,h = 900,1000
    im = Image.new("RGB",(w,h),(10,8,18)); im = _glow(im,(150,150,750,850),(110,90,50),120)
    s = Image.new("RGBA",(w,h),(0,0,0,0)); d = ImageDraw.Draw(s)
    d.polygon([(330,400),(640,320),(700,560),(390,640),(270,540)],fill=(246,242,234,255))
    d.ellipse((310,500,350,540),fill=(10,8,18,255))
    d.line((330,520,240,300),fill=(169,156,255,255),width=4)
    d.text((450,370),"7",font=f("black",170),fill=(91,91,245,255))
    _drop(im,s,(0,0),36,(18,44))
    d = ImageDraw.Draw(im); w2 = d.textlength("ideas",font=f("bold",60)); d.text(((w-w2)/2,740),"ideas",font=f("bold",60),fill=CRE)
    return vignette_s(im.filter(ImageFilter.GaussianBlur(.6)))

def price_tag(im, cx, cy):
    s = Image.new("RGBA",(560,420),(0,0,0,0)); d = ImageDraw.Draw(s)
    d.polygon([(120,110),(470,60),(510,300),(160,350),(60,240)],fill=(246,242,234,255))
    d.ellipse((95,215,135,255),fill=(10,6,24,255)); d.line((115,235,20,40),fill=(169,156,255,255),width=5)
    d.text((210,120),"−%",font=f("black",130),fill=(91,91,245,255))
    _drop(im,s,(cx-280,cy-210),30,(16,40))

def h01():
    im = bg((6,8,18),(540,900),(40,40,130),21)
    framed(im, get_frame(REEL1, prov_chair, "reel-1"), (110,600,970,1320))
    d = ImageDraw.Draw(im)
    center(d,300,"ADELANTO DEL REEL",f("mono",28),LAV)
    runs(d,380,[("Tu ",None),("mejor cliente",LIM),(" está",None)],52)
    runs(d,452,[("a punto de irse.",None)],52)
    cta_pill(im,1440,"Mira el reel en el perfil")
    logo(im,"tl"); return im

def h02():
    im = bg((12,6,26),(540,900),(70,40,160),22)
    framed(im, get_frame(REEL2, prov_scale, "reel-2"), (110,600,970,1320))
    d = ImageDraw.Draw(im)
    center(d,300,"ADELANTO DEL REEL",f("mono",28),LAV)
    runs(d,370,[("Bajar el precio es la",None)],50)
    runs(d,438,[("forma ",None),("más cara",LIM),(" de vender más.",None)],50)
    cta_pill(im,1440,"Mira el reel en el perfil")
    logo(im,"tl"); return im

def h03():
    im = bg((10,6,24),(540,700),(60,40,150),23)
    im = _glow(im,(240,420,840,820),(70,56,30),110)
    price_tag(im,540,610)
    d = ImageDraw.Draw(im)
    center(d,300,"ENCUESTA",f("mono",28),LAV)
    runs(d,830,[("¿Hiciste ",None),("descuentos",LIM)],52)
    runs(d,900,[("este mes?",None)],52)
    center(d,985,"Responde SÍ o NO por mensaje",f("reg",36),GRY)
    option(im,(120,1080,520,1400),"SÍ",LIM)
    option(im,(560,1080,960,1400),"NO",LAV)
    center(d,1470,"Te leemos a todos",f("reg",32),GRY)
    logo(im,"tl"); return im

def h04():
    im = bg((4,10,8),(540,950),(40,60,140),24)
    framed(im, get_frame(CARR, prov_cover, "carrusel"), (170,560,910,1300))
    d = ImageDraw.Draw(im)
    center(d,300,"NUEVO CARRUSEL",f("mono",28),LAV)
    runs(d,380,[("7 ideas ",None),("sin bajar precios",LIM)],52)
    cta_pill(im,1440,"Míralo en el perfil")
    logo(im,"tl"); return im

if __name__ == "__main__":
    for i,fn in enumerate([h01,h02,h03,h04],1):
        im = fn(); p = os.path.join(OUT,f"historia-{i:02d}")
        im.save(p+".png"); im.save(p+".jpg",quality=95)
    print("fotogramas:",USED)
