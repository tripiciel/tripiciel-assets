# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
# Historias dia 10 (estilo v2 oscuro premium). Usa los fotogramas de los reels si existen;
# si no, dibuja un provisorio en el mismo estilo.
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = "C:/Users/PC/tripiciel-assets/semana-01/"
REEL1 = ROOT + "dia-10/reels/reel-1/fotograma.jpg"
REEL2 = ROOT + "dia-10/reels/reel-2/fotograma.jpg"
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
def prov_city():
    # barrio de noche desde arriba, un haz de luz calida que enciende celulares
    w,h = 900,1000; rnd = random.Random(10)
    im = Image.new("RGB",(w,h),(5,7,14)); d = ImageDraw.Draw(im)
    for by in range(0,h,150):
        for bx in range(0,w,170):
            ox,oy = bx+18,by+18
            d.rectangle((ox,oy,ox+130,oy+110),fill=(16,16,28))
            for _ in range(5):
                rx,ry = ox+rnd.randint(6,90),oy+rnd.randint(6,70); rw,rh = rnd.randint(22,40),rnd.randint(22,40)
                d.rectangle((rx,ry,rx+rw,ry+rh),fill=(24+rnd.randint(0,10),24,40),outline=(34,34,54))
                if rnd.random()<.25: d.rectangle((rx+6,ry+6,rx+12,ry+12),fill=(150,120,70))
    for x in range(0,w,170): d.rectangle((x,0,x+18,h),fill=(10,10,18))
    for y in range(0,h,150): d.rectangle((0,y,w,y+18),fill=(10,10,18))
    im = _glow(im,(260,380,640,860),(120,96,52),120)
    beam = Image.new("L",(w,h),0); ImageDraw.Draw(beam).polygon([(420,0),(480,0),(640,820),(260,820)],fill=70)
    im.paste(Image.new("RGB",(w,h),(246,226,180)),(0,0),beam.filter(ImageFilter.GaussianBlur(40)))
    for cx,cy,on in [(330,640,1),(450,560,1),(560,690,1),(420,760,1),(160,300,0),(760,420,0),(700,860,0),(120,820,0)]:
        ph = Image.new("RGBA",(60,100),(0,0,0,0)); pd = ImageDraw.Draw(ph)
        pd.rounded_rectangle((0,0,59,99),12,fill=(30,30,40,255))
        pd.rounded_rectangle((5,7,54,92),8,fill=(198,244,50,255) if on else (22,22,34,255))
        if on: im = _glow(im,(cx-60,cy-70,cx+60,cy+70),(70,90,20),30)
        im.paste(ph,(cx-30,cy-50),ph)
    return vignette_s(im.filter(ImageFilter.GaussianBlur(.7)))

def prov_shutter():
    # persiana metalica a medio bajar; enfrente un local encendido y gente cruzando
    w,h = 900,1000
    im = Image.new("RGB",(w,h),(8,8,14)); d = ImageDraw.Draw(im)
    d.rectangle((0,820,w,h),fill=(18,18,24))
    d.rectangle((520,250,880,800),fill=(40,32,22)); im = _glow(im,(480,220,920,840),(150,120,60),90)
    d = ImageDraw.Draw(im); d.rectangle((540,280,860,780),fill=(214,190,140)); d.rectangle((540,280,860,320),fill=(91,91,245))
    for x in range(560,860,60): d.rectangle((x,360,x+40,520),fill=(180,150,100))
    d.rectangle((30,200,470,800),fill=(30,28,34))
    for y in range(200,560,22):
        d.rectangle((40,y,460,y+20),fill=(150,152,160)); d.line((40,y+2,460,y+2),fill=(205,208,214),width=2)
    d.rectangle((40,560,460,800),fill=(60,48,34)); im = _glow(im,(40,560,460,820),(70,50,26),40)
    d = ImageDraw.Draw(im)
    for x,s in [(560,1.0),(650,.9),(740,1.05)]:
        d.ellipse((x-16*s,620,x+16*s,652),fill=(20,18,26)); d.rounded_rectangle((x-26*s,655,x+26*s,780),18,fill=(20,18,26))
    return vignette_s(im.filter(ImageFilter.GaussianBlur(.7)))

def store_clock(im, cx, cy):
    s = Image.new("RGBA",(520,360),(0,0,0,0)); d = ImageDraw.Draw(s)
    d.rectangle((60,120,460,340),fill=(214,196,160,255)); d.rectangle((60,120,460,170),fill=(91,91,245,255))
    for x in range(60,460,50): d.polygon([(x,170),(x+50,170),(x+25,200)],fill=(169,156,255,255))
    d.rectangle((110,220,250,340),fill=(150,128,96,255)); d.rectangle((290,220,420,300),fill=(246,242,234,255))
    d.ellipse((330,10,470,150),fill=(120,116,110,255)); d.ellipse((340,20,460,140),fill=(246,242,234,255))
    d.line((400,80,400,40),fill=(40,36,60,255),width=6); d.line((400,80,430,95),fill=(91,91,245,255),width=6)
    p = (cx-260,cy-180)
    sh = Image.new("L",im.size,0); sh.paste(s.getchannel("A").point(lambda v:v*2//3),(p[0]+14,p[1]+36))
    im.paste(Image.new("RGB",im.size,0),(0,0),sh.filter(ImageFilter.GaussianBlur(24))); im.paste(s,p,s)

def map_pin(im, cx, cy):
    s = Image.new("RGBA",(560,560),(0,0,0,0)); d = ImageDraw.Draw(s)
    d.polygon([(30,380),(530,380),(470,540),(90,540)],fill=(236,230,216,255))
    for k in range(5): d.line((90+k*95,380,60+k*110,540),fill=(200,192,176,255),width=6)
    d.line((60,460,500,450),fill=(198,180,140,255),width=12)
    d.ellipse((150,40,410,300),fill=(91,91,245,255)); d.polygon([(170,220),(390,220),(280,440)],fill=(91,91,245,255))
    d.ellipse((205,95,355,245),fill=(246,242,234,255))
    d.line((280,170,280,120),fill=(40,36,60,255),width=8); d.line((280,170,318,186),fill=(198,244,50,255),width=8)
    d.arc((170,50,400,280),200,260,fill=(169,156,255,255),width=6)
    p = (cx-280,cy-280)
    sh = Image.new("L",im.size,0); sh.paste(s.getchannel("A").point(lambda v:v*3//4),(p[0]+20,p[1]+50))
    im.paste(Image.new("RGB",im.size,0),(0,0),sh.filter(ImageFilter.GaussianBlur(40))); im.paste(s,p,s)

def h01():
    im = bg((6,8,18),(540,900),(40,40,130),11)
    framed(im, get_frame(REEL1, prov_city, "reel-1"), (110,600,970,1320))
    d = ImageDraw.Draw(im)
    center(d,300,"ADELANTO DEL REEL",f("mono",28),LAV)
    runs(d,370,[("¿Sabes qué decide si tu",None)],50)
    runs(d,438,[("negocio aparece en el",None)],50)
    runs(d,506,[("celular",LIM),(" de tus vecinos?",None)],50)
    cta_pill(im,1440,"Mira el reel en el perfil")
    logo(im,"tl"); return im

def h02():
    im = bg((12,6,26),(540,900),(70,40,160),12)
    framed(im, get_frame(REEL2, prov_shutter, "reel-2"), (110,600,970,1320))
    d = ImageDraw.Draw(im)
    center(d,300,"ADELANTO DEL REEL",f("mono",28),LAV)
    runs(d,370,[("¿Cambiaste el ",None),("horario",LIM)],50)
    runs(d,438,[("y no lo avisaste?",None)],50)
    center(d,516,"Tus clientes se van al local de enfrente.",f("reg",34),GRY)
    cta_pill(im,1440,"Mira el reel en el perfil")
    logo(im,"tl"); return im

def h03():
    im = bg((10,6,24),(540,700),(60,40,150),13)
    im = _glow(im,(240,420,840,820),(70,56,30),110)
    store_clock(im,540,620)
    d = ImageDraw.Draw(im)
    center(d,300,"ENCUESTA",f("mono",28),LAV)
    runs(d,830,[("¿Tu ",None),("horario",LIM),(" está actualizado",None)],50)
    runs(d,898,[("en Google Maps?",None)],50)
    center(d,985,"Responde SÍ o NO por mensaje",f("reg",36),GRY)
    option(im,(120,1080,520,1400),"SÍ",LIM)
    option(im,(560,1080,960,1400),"NO",LAV)
    center(d,1470,"Te leemos a todos",f("reg",32),GRY)
    logo(im,"tl"); return im

def h04():
    im = bg((4,10,8),(540,950),(40,60,140),14)
    im = _glow(im,(260,640,820,1240),(70,60,40),120)
    map_pin(im,540,920)
    d = ImageDraw.Draw(im)
    center(d,300,"TIP RÁPIDO",f("mono",28),LAV)
    runs(d,370,[("Revisa ",None),("hoy",LIM),(" tu horario",None)],52)
    runs(d,442,[("en Google Maps.",None)],52)
    center(d,1290,"Si Google Maps dice abierto y está cerrado,",f("reg",36),GRY)
    center(d,1342,"el cliente llega y encuentra la persiana baja.",f("reg",36),GRY)
    runs(d,1430,[("Feriados y ",None),("horario especial",LAV),(" también.",None)],36)
    logo(im,"tl"); return im

if __name__ == "__main__":
    for i,fn in enumerate([h01,h02,h03,h04],1):
        im = fn(); p = os.path.join(OUT,f"historia-{i:02d}")
        im.save(p+".png"); im.save(p+".jpg",quality=95)
    print("fotogramas:",USED)
