# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"_base.py"),encoding="utf-8").read())
LOGO="C:/Users/PC/tripiciel-assets/semana-01/dia-01/reels/reel-4/"
def logo(im,y=1560,w=300):
    try:
        lg=Image.open(LOGO+"logo-horizontal.png").convert("RGBA"); lg=lg.resize((w,int(lg.height*w/lg.width)))
        im.paste(lg,((W-w)//2,y),lg)
    except Exception: pass
def globe(d,cx,cy,r,col=CRE,w=14):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=col,width=w); d.ellipse((cx-r*.45,cy-r,cx+r*.45,cy+r),outline=col,width=w)
    d.line((cx-r,cy,cx+r,cy),fill=col,width=w); d.line((cx,cy-r,cx,cy+r),fill=col,width=w)

def h01():
    im=base((540,760),(70,40,170)); d=ImageDraw.Draw(im)
    pill(d,250,"SEMANA 01 · DÍA 03",f("mono",30),fill=CARD,col=LAV)
    star(d,540,720,300,VIO); star(d,540,720,130,CRE); star(d,820,470,46,LIM); star(d,250,960,30,LAV)
    center(d,1080,"LUNES",f("heros",200),CRE,0)
    center(d,1300,"de arranque",f("play",130),LAV,0)
    center(d,1480,"Nueva semana, nuevos videos.",f("reg",42),CRE)
    return im
def share(tag,title,ft,box,fill=CARD,col=LAV,glow=(540,1100)):
    im=base(glow,stripes=True); d=ImageDraw.Draw(im)
    pill(d,215,tag,f("mono",28),fill=fill,col=col)
    center(d,300,title,ft,CRE,4)
    hole(d,box); sign(d,"br"); return im
def h02():
    im=share("ANTES / DESPUÉS · NACUSI MUEBLES","Mismo mueble,",f("black",88),(270,580,810,1540))
    d=ImageDraw.Draw(im); center(d,400,"otro video",f("play",104),LIM,0)
    d.text((70,1480),"ANTES",font=f("mono",30),fill=LAV); d.text((840,600),"DESPUÉS",font=f("mono",30),fill=LIM); return im
def h03():
    im=base((540,1000),(40,60,150)); d=ImageDraw.Draw(im)
    pill(d,215,"CARRUSEL NUEVO",f("mono",28),fill=VIO,col=CRE)
    d.text((90,280),"7",font=f("black",230),fill=LIM)
    left(d,280,320,"ganchos para\ncopiar hoy",f("heros",84),CRE,4)
    hole(d,(160,580,920,1530),"Pega aquí el carrusel"); sign(d,"tr"); return im
def h04():
    im=base((540,700),(80,40,160)); d=ImageDraw.Draw(im)
    pill(d,230,"CAJA DE PREGUNTAS",f("mono",28),fill=CARD,col=LAV)
    center(d,340,"¿Qué te cuesta más",f("black",76),CRE,4)
    center(d,435,"de grabar videos",f("play",92),LAV,0)
    center(d,560,"para tu negocio?",f("black",76),CRE,4)
    d.rounded_rectangle((150,760,930,1240),44,outline=VIO,width=6)
    center(d,980,"Sticker de preguntas aquí",f("mono",30),(80,80,140))
    center(d,1320,"Te respondemos en historias.",f("reg",42),CRE); sign(d,"tr"); return im
def h05():
    im=share("WEB · ANTES / DESPUÉS","¿Tus clientes te",f("heros",80),(270,580,810,1540),glow=(540,900))
    d=ImageDraw.Draw(im); center(d,395,"preguntan el precio?",f("play",86),LIM,0); return im
def h06():
    im=base((540,900),(50,40,160)); d=ImageDraw.Draw(im)
    pill(d,230,"WEBS",f("mono",30),fill=VIO,col=CRE)
    center(d,330,"Una web",f("black",120),CRE,0); center(d,470,"hace por ti",f("play",104),LAV,0)
    y=700
    for n,t in [("01","Muestra el catálogo"),("02","Responde precios"),("03","Recibe pedidos")]:
        d.rounded_rectangle((90,y,990,y+190),40,fill=CARD,outline=(50,50,120),width=3)
        d.text((140,y+50),n,font=f("mono",72),fill=LIM); d.text((310,y+60),t,font=f("bold",60),fill=CRE); y+=230
    d.text((700,1400),"24/7",font=f("black",120),fill=LIM)
    globe(d,210,1470,70,LAV,10); sign(d,"tr"); return im
def phone(im,shot,box):
    x0,y0,x1,y1=box; d=ImageDraw.Draw(im)
    d.rounded_rectangle((x0-22,y0-22,x1+22,y1+22),90,fill=(28,30,64),outline=VIO,width=6)
    s=Image.open(shot).convert("RGB"); sw=x1-x0; s=s.resize((sw,int(s.height*sw/s.width))).crop((0,0,sw,y1-y0))
    m=Image.new("L",(sw,y1-y0),0); ImageDraw.Draw(m).rounded_rectangle((0,0,sw,y1-y0),70,fill=255); im.paste(s,(x0,y0),m)
    d.rounded_rectangle(((x0+x1)//2-80,y0+16,(x0+x1)//2+80,y0+52),18,fill=(0,0,0))
def h07():
    im=base((540,1100),(70,50,180)); d=ImageDraw.Draw(im)
    pill(d,215,"DETRÁS DE ESCENA",f("mono",28),fill=CARD,col=LAV)
    center(d,295,"Así se ve en el celular",f("heros",64),CRE)
    p="C:/Users/PC/tripiciel-assets/semana-01/dia-03/reels/reel-3/web-celular.png"
    shot=p if os.path.exists(p) else os.path.join(OUT,"_web-captura.png")
    phone(im,shot,(290,420,790,1450)); d=ImageDraw.Draw(im)
    star(d,890,560,50,LIM); star(d,170,1300,34,LAV)
    center(d,1510,"Hecha por nosotros dos.",f("reg",38),LAV); sign(d,"tl"); return im
def h08():
    im=share("CÓMO TRABAJAMOS","Lunes nos escribes,",f("black",78),(270,580,810,1540),glow=(540,1000))
    d=ImageDraw.Draw(im); center(d,395,"jueves tienes tus videos",f("play",76),LIM,0); return im
def h09():
    im=base((540,1000),(40,40,150),stripes=True); d=ImageDraw.Draw(im)
    pill(d,230,"CÓMO TRABAJAMOS",f("mono",28),fill=VIO,col=CRE)
    center(d,330,"Paso a paso",f("play",120),CRE,0)
    y=560
    for i,(a,b) in enumerate([("Escribes","TRIPI"),("Te hacemos","3 preguntas"),("Propuesta en","24 h"),("","Arrancamos")],1):
        d.ellipse((110,y,250,y+140),fill=VIO); n=str(i); fo=f("black",80); d.text((180-tw(d,n,fo)/2,y+20),n,font=fo,fill=CRE)
        if i<4: d.line((180,y+150,180,y+225),fill=LAV,width=6)
        if a: d.text((300,y+8),a,font=f("reg",44),fill=LAV)
        d.text((300,y+(60 if a else 30)),b,font=f("heros",70),fill=LIM if i in(1,3) else CRE); y+=240
    sign(d,"tr"); return im
def h10():
    im=base((540,800),(80,50,190)); d=ImageDraw.Draw(im)
    star(d,540,330,70,LIM)
    center(d,450,"¿Lo quieres para",f("play",96),LAV,0); center(d,580,"tu negocio?",f("black",110),CRE,0)
    center(d,760,"Escribe",f("reg",56),CRE)
    fo=f("heros",170); t="TRIPI"; pw=tw(d,t,fo)+100
    d.rounded_rectangle(((W-pw)/2,840,(W+pw)/2,1070),60,fill=VIO); d.text(((W-tw(d,t,fo))/2,855),t,font=fo,fill=CRE)
    d.rounded_rectangle((180,1130,900,1450),40,outline=LAV,width=4)
    center(d,1270,"Sticker de respuesta aquí",f("mono",28),(90,90,150))
    logo(im,1500,280); return im
def cover(icon):
    im=Image.new("RGB",(W,H),BG); g=Image.new("RGB",(W,H),0); ImageDraw.Draw(g).ellipse((140,560,940,1360),fill=(60,50,170))
    im=ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(160))); d=ImageDraw.Draw(im)
    d.ellipse((290,710,790,1210),fill=VIO); icon(d); star(d,780,720,40,LIM); return im
def ic_web(d):
    d.rounded_rectangle((395,835,685,1085),26,outline=CRE,width=14); d.line((395,890,685,890),fill=CRE,width=14)
    for i,c in enumerate((LIM,LAV,LAV)): d.ellipse((425+i*38,852,447+i*38,874),fill=c)
    d.rounded_rectangle((430,920,560,1050),14,fill=LAV)
    for yy,c,x1 in ((925,CRE,655),(970,CRE,655),(1015,LIM,640)): d.rounded_rectangle((585,yy,x1,yy+20),8,fill=c)
def ic_steps(d):
    pts=[(420,1050),(540,960),(660,870)]
    d.line(pts,fill=CRE,width=14)
    for i,(x,y) in enumerate(pts): d.ellipse((x-38,y-38,x+38,y+38),fill=LIM if i==2 else CRE)
for i,fn in enumerate([h01,h02,h03,h04,h05,h06,h07,h08,h09,h10],1): fn().save(os.path.join(OUT,f"historia-{i:02d}.png"))
cover(ic_web).save(os.path.join(OUT,"destacada-webs.png")); cover(ic_steps).save(os.path.join(OUT,"destacada-como-trabajamos.png"))
