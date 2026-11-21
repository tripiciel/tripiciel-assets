# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
# Historias dia 09 (estilo v2 oscuro premium). Usa los fotogramas de los reels si existen;
# si no, dibuja un provisorio en el mismo estilo.
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = "C:/Users/PC/tripiciel-assets/semana-01/"
REEL1 = ROOT + "dia-09/reels/reel-1/fotograma.jpg"
REEL2 = ROOT + "dia-09/reels/reel-2/fotograma.jpg"
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

# ---------- provisorios (si los fotogramas de los reels aun no estan) ----------
def _glow(im, box, col, blur):
    g = Image.new("RGB",im.size,0); ImageDraw.Draw(g).ellipse(box,fill=col)
    return ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(blur)))

def vignette_s(im):
    m = Image.new("L",im.size,0); ImageDraw.Draw(m).ellipse((-150,-100,im.width+150,im.height+100),fill=255)
    return Image.composite(im,Image.new("RGB",im.size,0),m.filter(ImageFilter.GaussianBlur(160)))

def _die(s, pips, rot, tint=(244,240,232)):
    t = Image.new("RGBA",(s*2,s*2),(0,0,0,0)); d = ImageDraw.Draw(t)
    c = s; h = s*0.55
    top = [(c-s*.8,c-h*.45),(c,c-h),(c+s*.8,c-h*.45),(c,c+h*.1)]
    L = [(c-s*.8,c-h*.45),(c,c+h*.1),(c,c+h*1.15),(c-s*.8,c+h*.6)]
    R = [(c,c+h*.1),(c+s*.8,c-h*.45),(c+s*.8,c+h*.6),(c,c+h*1.15)]
    d.polygon(top,fill=tint+(255,)); d.polygon(L,fill=tuple(int(v*.78) for v in tint)+(255,))
    d.polygon(R,fill=tuple(int(v*.58) for v in tint)+(255,))
    A,B,C,D = top  # bilineal sobre la cara superior
    def pt(u,v):
        return (A[0]*(1-u)*(1-v)+B[0]*u*(1-v)+C[0]*u*v+D[0]*(1-u)*v, A[1]*(1-u)*(1-v)+B[1]*u*(1-v)+C[1]*u*v+D[1]*(1-u)*v)
    pos = {1:[(.5,.5)],2:[(.25,.25),(.75,.75)],3:[(.25,.25),(.5,.5),(.75,.75)],
           4:[(.25,.25),(.75,.25),(.25,.75),(.75,.75)],5:[(.25,.25),(.75,.25),(.5,.5),(.25,.75),(.75,.75)],
           6:[(.25,.2),(.25,.5),(.25,.8),(.75,.2),(.75,.5),(.75,.8)]}[pips]
    for u,v in pos:
        px,py = pt(u,v); r = s*.075; d.ellipse((px-r*1.3,py-r*.75,px+r*1.3,py+r*.75),fill=(30,26,40,255))
    d.line([top[0],top[1],top[2]],fill=(255,255,255,140),width=2)
    return t.rotate(rot,expand=True,resample=Image.BICUBIC)

def prov_board():
    w,h = 900,1000; rnd = random.Random(9)
    im = Image.new("RGB",(w,h),(6,10,8)); im = _glow(im,(100,250,800,900),(90,75,50),150)
    d = ImageDraw.Draw(im)
    bd = [(120,520),(780,520),(880,930),(20,930)]
    d.polygon([(x,y+24) for x,y in bd],fill=(0,0,0)); d.polygon(bd,fill=(96,66,40))
    for i in range(40):
        y = 520+i*10.5; k = (y-520)/410
        d.line((120-100*k,y,780+100*k,y),fill=(110+rnd.randint(-12,12),76,46),width=1)
    def P(u,v): x0 = 120-100*v; x1 = 780+100*v; return (x0+(x1-x0)*u, 520+410*v)
    for i in range(6):
        for j in range(4):
            u0,u1,v0,v1 = .04+i*.16,.04+i*.16+.13,.06+j*.235,.06+j*.235+.18
            d.polygon([P(u0,v0),P(u1,v0),P(u1,v1),P(u0,v1)],fill=(214,200,172) if (i+j)%2 else (196,182,154))
            if rnd.random()<.55:
                cx,cy = P((u0+u1)/2,(v0+v1)/2+.04); s = 14+26*((v0+v1)/2)
                col = rnd.choice([(230,224,210),(200,190,170),(91,91,245),(169,156,255)])
                d.rectangle((cx-s,cy-s*1.3,cx+s,cy),fill=col)
                d.polygon([(cx-s*1.2,cy-s*1.3),(cx,cy-s*2.1),(cx+s*1.2,cy-s*1.3)],fill=tuple(int(v*.7) for v in col))
                d.rectangle((cx-s*.25,cy-s*.6,cx+s*.25,cy),fill=(198,170,90))
    im = im.filter(ImageFilter.GaussianBlur(.8))
    for x,y,s,p,r in [(250,260,120,5,-12),(560,200,130,3,16),(420,400,110,6,6)]:
        dd = _die(s,p,r); sh = Image.new("L",im.size,0)
        sh.paste(dd.getchannel("A").point(lambda v:v*3//4),(int(x-s)+30,int(y-s)+90))
        im.paste(Image.new("RGB",im.size,0),(0,0),sh.filter(ImageFilter.GaussianBlur(26))); im.paste(dd,(int(x-s),int(y-s)),dd)
    return vignette_s(im)

def prov_tubes():
    w,h = 900,1000
    im = Image.new("RGB",(w,h),(8,6,20)); im = _glow(im,(300,200,600,900),(50,40,120),160)
    for k in range(10):
        x = 90+k*80; lit = k==6; top = 240 if lit else 320+(k*37)%110
        if lit: im = _glow(im,(x-150,150,x+150,950),(120,160,30),90)
        d = ImageDraw.Draw(im)
        if k==0: d.rectangle((0,800,w,h),fill=(14,12,26)); d.line((0,800,w,800),fill=(60,56,90),width=2)
        liq = (198,244,50) if lit else (66,60,118)
        d.rounded_rectangle((x-24,top,x+24,792),24,fill=(20,18,36),outline=(150,145,190),width=3)
        lv = 330 if lit else 690-(k*29)%90
        d.rounded_rectangle((x-19,lv,x+19,787),19,fill=liq)
        d.line((x-13,top+24,x-13,770),fill=(230,230,245),width=3)
        d.ellipse((x-28,top-9,x+28,top+11),outline=(180,175,215),width=3)
        ref = Image.new("L",im.size,0)
        ImageDraw.Draw(ref).rounded_rectangle((x-19,808,x+19,808+(787-lv)//4),12,fill=110 if lit else 50)
        im.paste(Image.new("RGB",im.size,liq),(0,0),ref.filter(ImageFilter.GaussianBlur(8)))
    return vignette_s(im.filter(ImageFilter.GaussianBlur(.6)))

# ---------- historias ----------
def h01():
    im = bg((4,10,8),(540,900),(30,70,50),1)
    framed(im, get_frame(REEL1, prov_board, "reel-1"), (110,560,970,1320))
    d = ImageDraw.Draw(im)
    center(d,300,"ADELANTO DEL REEL",f("mono",28),LAV)
    runs(d,370,[("¿Cuántos ",None),("dados",LIM),(" tiene",None)],54)
    runs(d,444,[("tu negocio?",None)],54)
    cta_pill(im,1440,"Mira el reel en el perfil")
    logo(im,"tl"); return im

def h02():
    im = bg((12,6,26),(540,900),(70,40,160),2)
    framed(im, get_frame(REEL2, prov_tubes, "reel-2"), (110,560,970,1320))
    d = ImageDraw.Draw(im)
    center(d,300,"ADELANTO DEL REEL",f("mono",28),LAV)
    runs(d,370,[("Subiste ",None),("10",LIM),(" videos",None)],54)
    runs(d,444,[("y solo ",None),("uno",LIM),(" tuvo vistas.",None)],54)
    center(d,1350,"ejemplo",f("mono",24),GRY)
    cta_pill(im,1440,"Mira el reel en el perfil")
    logo(im,"tl"); return im

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

def channels_icon(im, cx, cy):
    # mostrador con dos bolsas de compra: dos canales de venta
    s = Image.new("RGBA",(520,320),(0,0,0,0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle((10,250,510,300),14,fill=(96,66,40,255)); d.rectangle((10,250,510,262),fill=(130,92,58,255))
    for x0,col in [(80,(214,196,160)),(290,(91,91,245))]:
        d.arc((x0+35,40,x0+115,140),180,360,fill=tuple(int(v*.6) for v in col)+(255,),width=9)
        d.polygon([(x0,90),(x0+150,90),(x0+165,250),(x0-15,250)],fill=col+(255,))
        d.polygon([(x0+150,90),(x0+165,250),(x0+138,250)],fill=tuple(int(v*.7) for v in col)+(255,))
        d.line((x0,92,x0+150,92),fill=tuple(min(255,v+40) for v in col)+(255,),width=3)
    p = (cx-s.width//2, cy-s.height//2)
    sh = Image.new("L",im.size,0); sh.paste(s.getchannel("A").point(lambda v:v*2//3),(p[0]+14,p[1]+36))
    im.paste(Image.new("RGB",im.size,0),(0,0),sh.filter(ImageFilter.GaussianBlur(22))); im.paste(s,p,s)

def h03():
    im = bg((10,6,24),(540,700),(60,40,150),3)
    im = _glow(im,(240,420,840,820),(70,56,30),110)
    channels_icon(im,540,610)
    d = ImageDraw.Draw(im)
    center(d,300,"ENCUESTA",f("mono",28),LAV)
    runs(d,820,[("¿Vendes por más de",None)],52)
    runs(d,890,[("un ",None),("canal",LAV),("?",None)],52)
    center(d,980,"Responde SÍ o NO por mensaje",f("reg",36),GRY)
    option(im,(120,1080,520,1400),"SÍ",LIM)
    option(im,(560,1080,960,1400),"NO",LAV)
    center(d,1470,"Te leemos a todos",f("reg",32),GRY)
    logo(im,"tl"); return im

def h04():
    im = bg((4,10,8),(540,950),(40,60,140),4)
    im = _glow(im,(260,640,820,1240),(70,60,40),120)
    s = Image.new("RGBA",(520,600),(0,0,0,0)); d = ImageDraw.Draw(s)  # cronometro: el primer segundo
    d.rounded_rectangle((225,10,295,70),12,fill=(190,186,176,255)); d.rectangle((245,60,275,110),fill=(150,146,140,255))
    d.ellipse((20,90,500,570),fill=(120,116,110,255)); d.ellipse((34,104,486,556),fill=(236,230,216,255))
    d.ellipse((50,120,470,540),fill=(246,242,234,255))
    d.pieslice((70,140,450,520),-90,-84,fill=(198,244,50,255))
    for k in range(60):
        a = math.radians(k*6-90); r0 = 172 if k%5==0 else 190
        d.line((260+r0*math.cos(a),330+r0*math.sin(a),260+200*math.cos(a),330+200*math.sin(a)),fill=(60,56,70,255),width=5 if k%5==0 else 2)
    a = math.radians(-84); d.line((260,330,260+175*math.cos(a),330+175*math.sin(a)),fill=(91,91,245,255),width=8)
    d.ellipse((246,316,274,344),fill=(40,36,60,255))
    p = (W//2-260,640)
    sh = Image.new("L",im.size,0); sh.paste(s.getchannel("A").point(lambda v:v*3//4),(p[0]+20,p[1]+50))
    im.paste(Image.new("RGB",im.size,0),(0,0),sh.filter(ImageFilter.GaussianBlur(40))); im.paste(s,p,s)
    gl = Image.new("RGBA",s.size,(0,0,0,0)); ImageDraw.Draw(gl).pieslice((60,120,460,540),200,260,fill=(255,255,255,34))
    im.paste(gl,p,gl)
    d = ImageDraw.Draw(im)
    center(d,300,"TIP RÁPIDO",f("mono",28),LAV)
    runs(d,370,[("Hoy cambia el ",None),("primer segundo",LIM)],50)
    runs(d,440,[("de tu próximo video.",None)],50)
    center(d,1310,"Abre mostrando algo: el producto,",f("reg",36),GRY)
    center(d,1362,"el resultado o el problema.",f("reg",36),GRY)
    runs(d,1440,[("Ni saludo ni logo al ",None),("inicio",LAV),(".",None)],38)
    logo(im,"tl"); return im

if __name__ == "__main__":
    for i,fn in enumerate([h01,h02,h03,h04],1):
        im = fn(); p = os.path.join(OUT,f"historia-{i:02d}")
        im.save(p+".png"); im.save(p+".jpg",quality=95)
    print("fotogramas:",USED)
