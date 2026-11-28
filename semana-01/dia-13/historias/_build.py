# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
# Historias del dia (estilo v2 oscuro premium). Usa los fotogramas de los reels si existen;
# si no, dibuja un provisorio en el mismo estilo.
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = "C:/Users/PC/tripiciel-assets/semana-01/"
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
        c = rnd.choice([(120,96,50),(90,80,60),(60,60,140),(60,90,60)]); k = rnd.uniform(.12,.35)
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
    g = Image.new("RGB",im.size,0); ImageDraw.Draw(g).rounded_rectangle((x0-20,y0-20,x1+20,y1+20),r+20,fill=(90,70,36))
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

CREA=(246,242,234,255)
def _drop(im, s, p, blur=30, off=(16,40), op=2/3):
    sh = Image.new("L",im.size,0); sh.paste(s.getchannel("A").point(lambda v:int(v*op)),(p[0]+off[0],p[1]+off[1]))
    im.paste(Image.new("RGB",im.size,0),(0,0),sh.filter(ImageFilter.GaussianBlur(blur))); im.paste(s,p,s)
def save_all(fns):
    for i,fn in enumerate(fns,1):
        im = fn(); p = os.path.join(OUT,f"historia-{i:02d}")
        im.save(p+".png"); im.save(p+".jpg",quality=95)
    for k,v in USED.items(): print("fotograma",k,"->",v)

# ---------- dia 13 ----------
REEL1 = ROOT + "dia-13/reels/reel-1/fotograma.jpg"
CARR = ROOT + "dia-13/carrusel/slide-01.jpg"

def prov_deposito():
    # deposito: cajas polvorientas apiladas con billetes grises encima, luz calida lateral
    w,h = 900,1000
    im = Image.new("RGB",(w,h),(9,8,10)); im = _glow(im,(120,150,760,800),(130,98,52),130)
    s = Image.new("RGBA",(w,h),(0,0,0,0)); d = ImageDraw.Draw(s)
    boxes = [(140,560,420,800),(440,580,760,800),(220,340,520,560),(530,400,720,580),(330,170,560,340)]
    for i,(x0,y0,x1,y1) in enumerate(boxes):
        top = (168-i*6,130-i*5,84-i*3,255); side=(120-i*4,90-i*3,58,255)
        d.rectangle((x0,y0,x1,y1),fill=top); d.rectangle((x1-28,y0,x1,y1),fill=side)
        d.rectangle((x0+(x1-x0)//2-16,y0,x0+(x1-x0)//2+16,y1),fill=(190,160,110,255))
        d.line((x0,y0,x1,y0),fill=(205,190,160,255),width=3)
    for (x,y,a) in [(360,140,-8),(470,130,6),(600,372,-4),(260,312,5)]:
        b = Image.new("RGBA",(150,70),(0,0,0,0)); bd = ImageDraw.Draw(b)
        bd.rounded_rectangle((0,0,149,69),6,fill=(150,152,150,255),outline=(110,112,110,255),width=3)
        bd.ellipse((55,15,95,55),outline=(110,112,110,255),width=3)
        b = b.rotate(a,expand=True,resample=Image.BICUBIC); s.paste(b,(x,y),b)
    _drop(im,s,(0,0),30,(18,36))
    dust = Image.new("RGBA",(w,h),(0,0,0,0)); dd = ImageDraw.Draw(dust); rnd = random.Random(13)
    for _ in range(140):
        x,y = rnd.randint(0,w),rnd.randint(80,900); r = rnd.randint(1,4)
        dd.ellipse((x-r,y-r,x+r,y+r),fill=(230,200,150,rnd.randint(40,120)))
    im.paste(dust,(0,0),dust.filter(ImageFilter.GaussianBlur(1)))
    return vignette_s(im.filter(ImageFilter.GaussianBlur(.6)))

def prov_hormiga():
    # portada provisoria: monedas chicas que se van en fila, cifra 5 en lima
    w,h = 900,1000
    im = Image.new("RGB",(w,h),(9,9,12)); im = _glow(im,(150,200,750,850),(120,94,50),120)
    s = Image.new("RGBA",(w,h),(0,0,0,0)); d = ImageDraw.Draw(s)
    for i in range(9):
        x = 120+i*76; y = 760-int(40*math.sin(i*.8)); r = 34-i*2
        d.ellipse((x-r,y-r*0.45,x+r,y+r*0.45),fill=(150,120,64,255))
        d.ellipse((x-r,y-r*0.45-12,x+r,y+r*0.45-12),fill=(214,182,110,255),outline=(160,130,70,255),width=2)
    _drop(im,s,(0,0),24,(12,26))
    d = ImageDraw.Draw(im); fo = f("black",380); t="5"
    im2 = _glow(im,(260,140,640,620),(70,80,20),110); d = ImageDraw.Draw(im2)
    d.text(((w-d.textlength(t,font=fo))/2,150),t,font=fo,fill=LIM)
    return vignette_s(im2.filter(ImageFilter.GaussianBlur(.5)))

def h01():
    im = bg((10,8,12),(540,900),(110,80,40),41)
    framed(im, get_frame(REEL1, prov_deposito, "reel-1 (deposito)"), (110,600,970,1320))
    d = ImageDraw.Draw(im)
    center(d,300,"ADELANTO DEL REEL",f("mono",28),LAV)
    runs(d,380,[("Esa mercadería en el depósito",None)],52)
    runs(d,452,[("es ",None),("plata dormida",LIM)],56)
    cta_pill(im,1440,"Mira el reel en el perfil")
    logo(im,"tl"); return im

def h02():
    im = bg((8,10,8),(540,950),(100,76,40),42)
    framed(im, get_frame(CARR, prov_hormiga, "carrusel slide-01"), (200,600,880,1320))
    d = ImageDraw.Draw(im)
    center(d,300,"NUEVO CARRUSEL",f("mono",28),LAV)
    runs(d,380,[("5",LIM),(" gastos hormiga",None)],60)
    runs(d,458,[("que se comen tu ganancia",None)],46)
    cta_pill(im,1440,"Míralo en el perfil y guárdalo")
    logo(im,"tl"); return im

if __name__ == "__main__":
    save_all([h01,h02])
