# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
# Historias dia 08 (estilo v2 oscuro premium). Usa los fotogramas de los reels si existen;
# si no, dibuja un provisorio en el mismo estilo.
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = "C:/Users/PC/tripiciel-assets/semana-01/"
REEL1 = ROOT + "dia-08/reels/reel-1/fotograma.jpg"
REEL2 = ROOT + "dia-08/reels/reel-2/fotograma.jpg"
CAP = ROOT + "dia-07/_capturas/"
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

# ---------- provisorios (si los reels aun no estan) ----------
def prov_shelves():
    w,h = 900,1000
    im = Image.new("RGB",(w,h),(8,10,14)); d = ImageDraw.Draw(im)
    def shelf(x0,lit):
        base = (70,52,36) if lit else (26,22,20)
        for i in range(5):
            y = 140+i*170
            d.polygon([(x0,y+120),(x0+360,y+120),(x0+380,y+140),(x0+20,y+140)],fill=tuple(int(v*1.4) for v in base))
            d.rectangle((x0+20,y+140,x0+380,y+152),fill=tuple(int(v*.7) for v in base))
            rnd = random.Random(i+x0)
            xx = x0+28
            while xx < x0+350:
                bwid = rnd.randint(30,52); bh = rnd.randint(60,105)
                c = rnd.choice([(200,60,60),(230,180,60),(70,140,200),(90,170,90),(230,230,220),(160,90,200)])
                if not lit: c = tuple(v//6 for v in c)
                d.rectangle((xx,y+120-bh,xx+bwid,y+120),fill=c)
                d.rectangle((xx,y+120-bh,xx+6,y+120),fill=tuple(min(255,v+40) for v in c))
                d.rectangle((xx+bwid-8,y+120-bh,xx+bwid,y+120),fill=tuple(v//2 for v in c))
                xx += bwid+6
        d.rectangle((x0,120,x0+14,900),fill=tuple(int(v*1.2) for v in base)); d.rectangle((x0+386,120,x0+400,900),fill=base)
    shelf(40,True); shelf(470,False)
    g = Image.new("RGB",(w,h),0); gd = ImageDraw.Draw(g)
    gd.ellipse((-60,-120,520,700),fill=(120,100,60)); im = ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(120)))
    d = ImageDraw.Draw(im)
    for cx in (130,250,360):  # siluetas de clientes
        d.ellipse((cx-30,760,cx+30,820),fill=(16,14,22)); d.rounded_rectangle((cx-50,815,cx+50,1000),40,fill=(16,14,22))
    return im.filter(ImageFilter.GaussianBlur(1.2))

def prov_notebook():
    w,h = 900,1000
    im = Image.new("RGB",(w,h),(10,8,20)); d = ImageDraw.Draw(im)
    g = Image.new("RGB",(w,h),0); ImageDraw.Draw(g).ellipse((150,350,750,950),fill=(90,70,40))
    im = ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(140))); d = ImageDraw.Draw(im)
    d.polygon([(160,820),(450,700),(740,820),(450,950)],fill=(0,0,0))
    im = im.filter(ImageFilter.GaussianBlur(3)); d = ImageDraw.Draw(im)
    d.polygon([(140,760),(450,640),(450,880),(160,780)],fill=(214,200,170))
    d.polygon([(450,640),(760,760),(740,780),(450,880)],fill=(232,220,190))
    for i in range(7):
        t=i/7; d.line((170+20*t+t*0,700+ -0+ i*0, 0,0),fill=(0,0,0)) if False else None
        d.line((175, 750-i*14+i*0, 440, 650+i*26),fill=(150,140,170),width=2)
        d.line((460, 660+i*26, 735, 760-i*0+i*2),fill=(150,140,170),width=2)
    d.line((450,640,450,880),fill=(120,100,80),width=4)
    rnd = random.Random(4)
    for i in range(9):  # billetes volando
        bw,bh = 150,72; b = Image.new("RGBA",(bw,bh),(0,0,0,0)); bd = ImageDraw.Draw(b)
        bd.rounded_rectangle((0,0,bw-1,bh-1),8,fill=(120,170,110,255),outline=(70,110,70,255),width=3)
        bd.ellipse((bw/2-20,bh/2-20,bw/2+20,bh/2+20),outline=(70,110,70,255),width=3)
        b = b.rotate(rnd.randint(-50,50),expand=True,resample=Image.BICUBIC)
        x = 300+rnd.randint(-160,260)+i*8; y = 600-i*62+rnd.randint(-20,20)
        if i>5: b = b.filter(ImageFilter.GaussianBlur(3))
        sh = Image.new("RGBA",b.size,(0,0,0,0)); sh.putalpha(b.getchannel("A").point(lambda v:v//3))
        im.paste(sh.filter(ImageFilter.GaussianBlur(10)),(x+10,y+30),sh.filter(ImageFilter.GaussianBlur(10)))
        im.paste(b,(x,y),b)
    return im

def get_frame(path, fallback, key):
    if os.path.exists(path):
        USED[key] = "real"; return Image.open(path).convert("RGB")
    USED[key] = "PROVISORIO"; return fallback()

def cta_pill(im, y, text):
    d = ImageDraw.Draw(im); fo = f("bold",40); pw = tw(d,text,fo)+150; x = (W-pw)/2
    d.rounded_rectangle((x,y,x+pw,y+90),45,outline=LAV,width=3,fill=(22,18,52))
    d.text((x+44,y+22),text,font=fo,fill=CRE)
    ax = x+pw-62; d.line((ax-24,y+45,ax+12,y+45),fill=LAV,width=5); d.polygon([(ax+24,y+45),(ax+4,y+30),(ax+4,y+60)],fill=LAV)

# ---------- historias ----------
def h01():
    im = bg((4,10,8),(540,900),(30,70,50),1)
    framed(im, get_frame(REEL1, prov_shelves, "reel-1"), (110,560,970,1320))
    d = ImageDraw.Draw(im)
    center(d,300,"ADELANTO DEL REEL",f("mono",28),LAV)
    runs(d,370,[("Dos almacenes venden ",None),("lo mismo.",None)],50)
    runs(d,440,[("Uno vende ",None),("el doble.",LIM)],50)
    center(d,1350,"ejemplo",f("mono",24),GRY)
    cta_pill(im,1440,"Mira el reel en el perfil")
    logo(im,"tl"); return im

def h02():
    im = bg((12,6,26),(540,900),(70,40,160),2)
    framed(im, get_frame(REEL2, prov_notebook, "reel-2"), (110,560,970,1320))
    d = ImageDraw.Draw(im)
    center(d,300,"ADELANTO DEL REEL",f("mono",28),LAV)
    runs(d,370,[("¿Cuánta ",None),("plata",LIM),(" pierdes con el fiado",None)],50)
    runs(d,440,[("que nunca cobraste?",None)],50)
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

def notebook_icon(im, cx, cy):
    s = Image.new("RGBA",(360,260),(0,0,0,0)); d = ImageDraw.Draw(s)
    d.polygon([(20,60),(180,20),(180,230),(30,250)],fill=(214,200,170,255))
    d.polygon([(180,20),(340,60),(330,250),(180,230)],fill=(236,226,198,255))
    for i in range(6):
        d.line((40,90+i*26,170,60+i*28),fill=(150,140,175,255),width=2); d.line((190,60+i*28,322,90+i*26),fill=(150,140,175,255),width=2)
    d.line((180,20,180,230),fill=(120,100,80,255),width=4)
    d.line((60,110,150,92),fill=(91,91,245,255),width=4); d.line((60,150,130,138),fill=(91,91,245,255),width=4)
    s = s.rotate(-8,expand=True,resample=Image.BICUBIC)
    p = (cx-s.width//2, cy-s.height//2)
    sh = Image.new("L",im.size,0); sh.paste(s.getchannel("A").point(lambda v:v*2//3),(p[0]+14,p[1]+40))
    im.paste(Image.new("RGB",im.size,0),(0,0),sh.filter(ImageFilter.GaussianBlur(22))); im.paste(s,p,s)

def h03():
    im = bg((10,6,24),(540,700),(60,40,150),3)
    notebook_icon(im,540,600)
    d = ImageDraw.Draw(im)
    center(d,300,"ENCUESTA",f("mono",28),LAV)
    runs(d,800,[("¿Todavía anotas el fiado",None)],52)
    runs(d,870,[("en ",None),("cuaderno?",LAV)],52)
    center(d,960,"Responde SÍ o NO por mensaje",f("reg",36),GRY)
    option(im,(120,1080,520,1400),"SÍ",LIM)
    option(im,(560,1080,960,1400),"NO",LAV)
    center(d,1470,"Te leemos a todos",f("reg",32),GRY)
    logo(im,"tl"); return im

def phone(im, shot, box):
    x0,y0,x1,y1 = box; bw,bh = x1-x0,y1-y0
    body = Image.new("RGBA",(bw+40,bh+40),(0,0,0,0)); bd = ImageDraw.Draw(body)
    for i in range(20):  # canto metalico
        c = 40+i*4; bd.rounded_rectangle((i,i,bw+39-i,bh+39-i),90-i,fill=(c,c,c+12,255))
    bd.rounded_rectangle((20,20,bw+19,bh+19),72,fill=(5,5,8,255))
    sh = Image.new("L",im.size,0); sh.paste(body.getchannel("A").point(lambda v:v*3//4),(x0+10,y0+30))
    im.paste(Image.new("RGB",im.size,0),(0,0),sh.filter(ImageFilter.GaussianBlur(40)))
    im.paste(body,(x0-20,y0-20),body)
    sx0,sy0,sw,sh2 = x0+12,y0+12,bw-24,bh-24
    s = shot.convert("RGB").crop((0,0,shot.width,2150))  # abajo esta "Powered by Netlify": fuera
    sc = max(sw/s.width, sh2/s.height); s = s.resize((int(s.width*sc+.5),int(s.height*sc+.5)),Image.LANCZOS)
    l = (s.width-sw)//2; s = s.crop((l,0,l+sw,sh2))
    m = Image.new("L",(sw,sh2),0); ImageDraw.Draw(m).rounded_rectangle((0,0,sw-1,sh2-1),60,fill=255)
    im.paste(s,(sx0,sy0),m)
    gl = Image.new("RGBA",(sw,sh2),(0,0,0,0)); gd = ImageDraw.Draw(gl)
    gd.polygon([(0,0),(sw*.55,0),(0,sh2*.45)],fill=(255,255,255,30))
    gl.putalpha(ImageChops.multiply(gl.getchannel("A"),m)); im.paste(gl,(sx0,sy0),gl)

def h04():
    im = bg((4,10,8),(540,950),(40,60,140),4)
    g = Image.new("RGB",(W,H),0); ImageDraw.Draw(g).ellipse((260,620,820,1380),fill=(70,60,170))
    im = ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(120)))
    phone(im, Image.open(CAP+"movil-inicio.png"), (330,600,750,1420))
    d = ImageDraw.Draw(im)
    center(d,300,"PRUEBA FIADITO",f("mono",28),LAV)
    runs(d,370,[("Comenta ",None),("FIADO",LIM),(" en el último reel",None)],50)
    center(d,445,"y te mandamos el link para probar",f("reg",38),GRY)
    runs(d,500,[("Fiadito ",None),("3 días gratis",LAV)],40)
    cta_pill(im,1490,"Ir al último reel")
    logo(im,"tl"); return im

if __name__ == "__main__":
    for i,fn in enumerate([h01,h02,h03,h04],1):
        im = fn(); p = os.path.join(OUT,f"historia-{i:02d}")
        im.save(p+".png"); im.save(p+".jpg",quality=95)
    print("fotogramas:",USED)
