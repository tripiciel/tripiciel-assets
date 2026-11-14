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
    d.rounded_rectangle((cx-s*.35,cy+s*.3,cx+s*.35,cy+s*.42),6,fill=VIO)
def bubble(d,box,txt,fo,fill,col,me=False):
    x0,y0,x1,y1=box; d.rounded_rectangle(box,34,fill=fill)
    tx=x1-50 if me else x0+50; d.polygon([(tx-16,y1-4),(tx+16,y1-4),(tx+(24 if me else -24),y1+26)],fill=fill)
    left(d,x0+34,y0+30,txt,fo,col,8)

def h01():
    im=base((540,800),(60,40,150)); d=ImageDraw.Draw(im)
    pill(d,250,"SEMANA 01 · DÍA 02",f("mono",30),fill=CARD,col=LAV)
    star(d,540,700,250,VIO); star(d,540,700,110,LAV); star(d,790,480,50,LIM); star(d,290,900,32,CRE)
    center(d,1000,"Domingo",f("play",190),CRE,0)
    center(d,1230,"DE EDICIÓN",f("black",120),LAV)
    center(d,1410,"Hoy les mostramos cómo\nse transforma un video crudo.",f("reg",44),CRE)
    return im
def h02():
    im=base((540,1000),stripes=True); d=ImageDraw.Draw(im)
    pill(d,220,"ANTES / DESPUÉS · CHICHO CARS",f("mono",28),fill=LIM,col=BG)
    center(d,310,"¿Lo frenarías",f("heros",92),CRE,0); center(d,405,"ahora?",f("play",120),LAV)
    hole(d,(275,590,805,1532))
    center(d,1560,"Chevrolet Aveo · del crudo al reel",f("bold",36),CRE)
    sign(d,"tr"); return im
def h03():
    im=base((540,500)); d=ImageDraw.Draw(im)
    src=os.path.join(OUT,"..","reels","reel-1","antes-frame.png")
    if not os.path.exists(src): src=os.path.join(OUT,"_antes-crudo.png")
    fr=ImageOps.fit(Image.open(src).convert("RGB"),(620,1080),centering=(.5,.55))
    fr=Image.blend(fr,ImageOps.grayscale(fr).convert("RGB"),.35)
    m=Image.new("L",fr.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,620,1080),36,fill=255)
    x0,y0=230,440; d.rounded_rectangle((x0-12,y0-12,x0+632,y0+1092),46,fill=CRE)
    im.paste(fr,(x0,y0),m); d=ImageDraw.Draw(im)
    d.rounded_rectangle((x0+36,y0+36,x0+270,y0+104),14,fill=(210,45,45)); d.ellipse((x0+56,y0+56,x0+84,y0+84),fill=CRE); d.text((x0+100,y0+48),"CRUDO",font=f("mono",36),fill=CRE)
    d.text((x0+470,y0+1010),"00:03",font=f("mono",34),fill=CRE)
    center(d,225,"DETRÁS DE ESCENA",f("mono",32),LIM)
    center(d,280,"Así se ve el crudo\nantes de editar",f("bold",54),CRE,4)
    pill(d,1560,"Sin color · sin ritmo · sin texto",f("bold",36),fill=VIO)
    sign(d,"bl"); return im
def h04():
    im=base((300,1300),(50,40,140)); d=ImageDraw.Draw(im)
    pill(d,250,"TIP RÁPIDO",f("mono",32),fill=LIM,col=BG,x=90)
    cx,cy=220,520; d.polygon([(cx-90,cy-45),(cx-30,cy-45),(cx+40,cy-110),(cx+40,cy+110),(cx-30,cy+45),(cx-90,cy+45)],fill=LAV)
    d.line((cx+90,cy-60,cx+200,cy+60),fill=LIM,width=22); d.line((cx+90,cy+60,cx+200,cy-60),fill=LIM,width=22)
    left(d,90,700,"La mayoría\nmira sin\nsonido.",f("black",130),CRE,0)
    left(d,90,1140,"¿Tus videos tienen",f("play",80),LAV)
    d.rounded_rectangle((90,1270,990,1400),20,fill=CRE); center(d,1295,"SUBTÍTULOS?",f("heros",84),BG)
    left(d,90,1460,"Sin ellos, tu mensaje se pierde.",f("reg",42),CRE)
    sign(d,"tr"); return im
def h05():
    im=base((540,900),(30,50,150)); d=ImageDraw.Draw(im)
    center(d,230,"CARRUSEL NUEVO",f("mono",32),LAV)
    hole(d,(190,320,890,1195),"Pega aquí el carrusel")
    bx,by=470,1250; d.polygon([(bx,by),(bx+140,by),(bx+140,by+170),(bx+70,by+120),(bx,by+170)],fill=LIM)
    center(d,1450,"Guárdalo para tu",f("play",76),CRE,0); center(d,1555,"PRÓXIMO VIDEO",f("black",72),LAV)
    sign(d,"tr"); return im
def h06():
    im=base((540,1100),(20,20,90)); d=ImageDraw.Draw(im)
    for i in range(40): star(d,(i*197)%W,200+(i*331)%1400,3+(i%3),(60,64,120))
    center(d,215,"03:07 a. m.",f("mono",110),LIM)
    center(d,355,"tu negocio respondió solo",f("play",62),CRE)
    hole(d,(290,480,790,1369),"Pega aquí el reel 3")
    pill(d,1430,"DEMO · BOT DE RESPUESTA",f("mono",30),fill=VIO)
    sign(d,"br"); return im
def h07():
    im=base((800,600)); d=ImageDraw.Draw(im)
    bot_icon(d,200,450,110)
    left(d,360,320,"¿Qué es un",f("play",70),LAV,0); left(d,360,410,"BOT DE\nRESPUESTA?",f("black",80),CRE,0)
    items=[("1","Un asistente que contesta\ntus mensajes por ti."),("2","Funciona en WhatsApp\ne Instagram."),("3","Responde lo que siempre\nte preguntan, al instante.")]
    y=700
    for n,t in items:
        d.rounded_rectangle((90,y,990,y+230),40,fill=CARD,outline=(52,56,120),width=3)
        d.ellipse((130,y+55,250,y+175),fill=VIO); fo=f("heros",70); d.text((190-tw(d,n,fo)/2,y+70),n,font=fo,fill=CRE)
        left(d,290,y+55,t,f("bold",46),CRE,10); y+=270
    sign(d,"tr"); return im
def h08():
    im=base((540,1000),(50,30,140)); d=ImageDraw.Draw(im)
    center(d,230,"LO QUE HACE UN BOT",f("mono",32),LAV)
    bubble(d,(90,320,700,440),"¿Tienen turno mañana?",f("reg",42),CARD,CRE)
    bubble(d,(300,510,990,700),"¡Hola! Sí: 10:00 u 16:30.\n¿Cuál te reservo?",f("bold",42),VIO,CRE,True)
    d.text((300,735),"respondido en segundos",font=f("mono",28),fill=LIM)
    rows=[("Responde en","segundos",LIM,"heros"),("Atiende","24/7",LIM,"mono"),("Toma pedidos","y turnos",LAV,"play")]
    y=830
    for a,b,c,fn in rows:
        d.line((90,y,990,y),fill=(52,56,120),width=3)
        left(d,90,y+30,a,f("bold",52),CRE); left(d,90,y+95,b,f(fn,110),c); y+=255
    sign(d,"br"); return im
def h09():
    im=base((540,900)); d=ImageDraw.Draw(im)
    center(d,230,"ENCUESTA",f("mono",34),LIM)
    center(d,300,"¿Respondes los\nmensajes en menos\nde 1 hora?",f("heros",84),CRE,6)
    hole(d,(140,700,940,1160),"Sticker de encuesta aquí")
    pill(d,1220,"Sí",f("bold",44),fill=VIO,x=140); pill(d,1220,"No, se me escapan",f("bold",44),fill=CARD,col=LAV,x=360)
    center(d,1380,"Responde con sinceridad.",f("play",50),LAV)
    sign(d,"br"); return im
def h10():
    im=base((540,1300),(70,50,170)); d=ImageDraw.Draw(im)
    bot_icon(d,540,380,95)
    center(d,510,"¿Quieres uno así",f("play",86),LAV,0); center(d,610,"para tu negocio?",f("bold",72),CRE)
    center(d,750,"Escribe",f("reg",56),CRE); center(d,810,"TRIPI",f("black",200),LIM)
    hole(d,(140,1110,940,1440),"Sticker de respuesta aquí")
    center(d,1480,"Te contamos cómo funciona. Sí, usamos IA.",f("reg",36),CRE)
    sign(d,"tl"); return im
def dest():
    im=Image.new("RGB",(W,H),BG); g=Image.new("RGB",(W,H),0); ImageDraw.Draw(g).ellipse((140,560,940,1360),fill=(60,50,170))
    im=ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(160))); d=ImageDraw.Draw(im)
    d.ellipse((290,710,790,1210),fill=VIO); bot_icon(d,540,985,140); d.rounded_rectangle((491,1027,589,1044),6,fill=LIM); star(d,780,720,40,LIM); return im
for i,fn in enumerate([h01,h02,h03,h04,h05,h06,h07,h08,h09,h10],1): fn().save(os.path.join(OUT,f"historia-{i:02d}.png"))
dest().save(os.path.join(OUT,"destacada-bots.png"))
