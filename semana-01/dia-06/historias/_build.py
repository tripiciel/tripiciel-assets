# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"_base.py"),encoding="utf-8").read())
D6="C:/Users/PC/tripiciel-assets/semana-01/dia-06/"
PROV=[]
N=(20,20,30)

def phone(im,shot,box):
    x0,y0,x1,y1=box; d=ImageDraw.Draw(im); bw,bh=x1-x0,y1-y0
    d.rounded_rectangle((x0-22,y0-22,x1+22,y1+22),80,fill=(28,30,64),outline=VIO,width=6)
    s=shot.convert("RGB"); sc=max(bw/s.width,bh/s.height)
    s=s.resize((int(s.width*sc+.5),int(s.height*sc+.5)),Image.LANCZOS)
    l=(s.width-bw)//2; t=(s.height-bh)//2; s=s.crop((l,t,l+bw,t+bh))
    m=Image.new("L",(bw,bh),0); ImageDraw.Draw(m).rounded_rectangle((0,0,bw,bh),60,fill=255); im.paste(s,(x0,y0),m)
    d.rounded_rectangle(((x0+x1)//2-70,y0+16,(x0+x1)//2+70,y0+48),16,fill=(0,0,0))

def arrow_cta(d,y,t="Mira el reel en el perfil"):
    fo=f("bold",44); tx=tw(d,t,fo); bw=tx+150; x=(W-bw)/2
    d.rounded_rectangle((x,y,x+bw,y+100),50,fill=VIO); d.text((x+40,y+24),t,font=fo,fill=CRE)
    ax=x+bw-75; d.line((ax-28,y+50,ax+18,y+50),fill=CRE,width=8); d.polygon([(ax+30,y+50),(ax+6,y+30),(ax+6,y+70)],fill=CRE)

def load(n):
    for e in ("fotograma.jpg","fotograma.png"):
        p=D6+f"reels/reel-{n}/"+e
        if os.path.exists(p): return Image.open(p)
    PROV.append(f"reel-{n}"); return None

def prov1():
    s=Image.new("RGB",(540,960),BG); d=ImageDraw.Draw(s)
    pill(d,150,"Negocio de ejemplo",f("bold",24),fill=CRE,col=BG,x=150)
    d.text((40,240),"Lunes a domingo:",font=f("bold",36),fill=CRE)
    d.text((40,290),"lo mismo de siempre",font=f("play",40),fill=LAV)
    for i,(a,b) in enumerate([("Pan del día","¿Qué salió hoy?"),("Ofertas","Precio de la semana"),("Pedidos","Cómo te encargo")]):
        y=390+i*150; d.rounded_rectangle((40,y,500,y+120),24,fill=CARD,outline=VIO,width=3)
        d.text((70,y+20),a,font=f("bold",34),fill=CRE); d.text((70,y+68),b,font=f("reg",26),fill=LAV)
    star(d,450,860,40,VIO); return s

def prov2():
    s=Image.new("RGB",(540,960),BG); d=ImageDraw.Draw(s)
    pill(d,150,"Negocio de ejemplo",f("bold",24),fill=CRE,col=BG,x=150)
    d.rounded_rectangle((40,240,500,600),24,fill=CRE)
    d.rectangle((40,240,500,290),fill=(220,216,240)); d.text((60,252),"www.tunegocio.com",font=f("mono",22),fill=N)
    d.text((60,320),"Tu negocio",font=f("black",44),fill=N); d.text((60,380),"Horario · Dirección · Menú",font=f("reg",26),fill=N)
    d.rounded_rectangle((60,450,300,520),35,fill=VIO); d.text((95,467),"Pedir ahora",font=f("bold",28),fill=CRE)
    d.text((40,650),"WEB PROPIA",font=f("heros",48),fill=CRE); d.text((40,710),"vs. solo Instagram",font=f("play",42),fill=LAV)
    return s

def h01():
    im=base((540,780),(70,40,170)); d=ImageDraw.Draw(im)
    pill(d,250,"SEMANA 01 · DÍA 06",f("mono",30),fill=CARD,col=LAV)
    star(d,540,720,300,VIO); star(d,540,720,130,CRE); star(d,820,470,46,LIM); star(d,250,960,30,LAV)
    center(d,1080,"JUEVES",f("heros",190),CRE,0)
    center(d,1300,"de planificar",f("play",130),LAV,0)
    center(d,1490,"Hoy te mostramos cómo armamos\nla semana de un negocio.",f("reg",40),CRE)
    return im

def h02():
    im=base((540,900),(50,40,160),stripes=True); d=ImageDraw.Draw(im)
    pill(d,240,"ENCUESTA RÁPIDA",f("mono",32),fill=CARD,col=LAV)
    center(d,350,"¿Tienes web propia",f("black",92),CRE,0)
    center(d,470,"o solo Instagram?",f("play",104),LAV,0)
    for i,(t,sub,fill,col) in enumerate([("WEB","Tengo mi página",VIO,CRE),("SOLO IG","Todo en Instagram",CRE,BG)]):
        y=720+i*290
        d.rounded_rectangle((100,y,980,y+240),50,fill=fill)
        d.text((150,y+60),t,font=f("heros",110 if i==0 else 92),fill=col)
        d.text((560,y+70),sub,font=f("reg",38),fill=col)
        d.text((560,y+130),"Escríbelo por mensaje",font=f("mono",26),fill=(CRE if i==0 else VIO))
    center(d,1330,"Respóndenos WEB o SOLO IG",f("bold",50),CRE)
    center(d,1410,"y te contamos qué te conviene.",f("reg",42),LAV)
    sign(d,"tr"); return im

def reel(shot,prov,t1,t2,top="NUEVO REEL"):
    im=base((540,1000),(60,40,170)); d=ImageDraw.Draw(im)
    pill(d,215,top,f("mono",30),fill=CARD,col=LAV)
    center(d,300,t1,f("black",76),CRE,0)
    center(d,390,t2,f("play",76),LAV,0)
    phone(im,shot or prov(),(330,560,750,1307)); d=ImageDraw.Draw(im)
    star(d,900,700,40,LAV); star(d,170,1200,30,LIM)
    arrow_cta(d,1420); sign(d,"tr"); return im

def h03(): return reel(load(1),prov1,"¿Vendes lo mismo","todos los días?")
def h06(): return reel(load(2),prov2,"¿Web propia o","solo Instagram?")

def h04():
    im=base((540,900),(55,40,165)); d=ImageDraw.Draw(im)
    pill(d,215,"DETRÁS DE ESCENA",f("mono",30),fill=CARD,col=LAV)
    center(d,295,"Así planificamos",f("black",84),CRE,0)
    center(d,395,"la semana de un cliente",f("play",80),LAV,0)
    x0,y0,x1=80,540,1000
    d.rounded_rectangle((x0,y0,x1,y0+880),36,fill=CARD,outline=(50,54,110),width=3)
    d.rounded_rectangle((x0,y0,x1,y0+90),36,fill=VIO); d.rectangle((x0,y0+50,x1,y0+90),fill=VIO)
    d.text((x0+30,y0+24),"DÍA",font=f("mono",34),fill=CRE); d.text((x0+200,y0+24),"QUÉ HACEMOS",font=f("mono",34),fill=CRE)
    rows=[("LUN","Revisamos números","Qué funcionó y qué no.",LIM),("MAR","Armamos el calendario","Qué se publica y cuándo.",LAV),
          ("MIÉ","Grabamos","Videos y fotos del negocio.",LAV),("JUE","Editamos","Todo listo para subir.",LAV),
          ("VIE","Revisamos juntos","Nada sale sin tu visto bueno.",LAV)]
    y=y0+110
    for dd,t,s,c in rows:
        d.rounded_rectangle((x0+20,y+10,x0+160,y+130),24,fill=BG,outline=c,width=4)
        d.text((x0+90-tw(d,dd,f("heros",50))/2,y+40),dd,font=f("heros",50),fill=CRE)
        d.text((x0+200,y+22),t,font=f("bold",46),fill=CRE); d.text((x0+200,y+84),s,font=f("reg",34),fill=LAV)
        d.rounded_rectangle((x1-80,y+50,x1-40,y+90),10,outline=VIO,width=4)
        d.line((x1-72,y+70,x1-62,y+82),fill=CRE,width=5); d.line((x1-62,y+82,x1-46,y+56),fill=CRE,width=5)
        if dd!="VIE": d.line((x0+20,y+150,x1-20,y+150),fill=(40,44,96),width=2)
        y+=152
    center(d,1460,"Maciel y Tripicchio: dos personas reales.",f("mono",32),LAV)
    center(d,1510,"Maciel es contador público: los números los mira él.",f("reg",32),CRE)
    sign(d,"tl"); return im

def h05():
    im=base((540,850),(50,40,150)); d=ImageDraw.Draw(im)
    pill(d,215,"TIP RÁPIDO",f("mono",30),fill=CARD,col=LAV)
    center(d,295,"Fija tu horario",f("black",88),CRE,0)
    center(d,400,"y tu dirección",f("play",100),LAV,0)
    center(d,545,"en una historia destacada",f("bold",48),CRE,0)
    d.rounded_rectangle((130,640,950,1220),40,fill=CARD,outline=(50,54,110),width=3)
    d.ellipse((170,680,310,820),fill=(60,60,140)); star(d,240,750,40,LAV)
    d.text((340,700),"negocio de ejemplo",font=f("bold",38),fill=CRE)
    d.text((340,756),"Tu barrio · tu esquina",font=f("reg",30),fill=LAV)
    for i,(lbl,c) in enumerate([("Horario",VIO),("Dirección",VIO),("Pedidos",(60,64,130))]):
        cx=280+i*260; cy=960
        d.ellipse((cx-90,cy-90,cx+90,cy+90),outline=c,width=8); d.ellipse((cx-74,cy-74,cx+74,cy+74),fill=BG)
        if i==0:
            d.ellipse((cx-40,cy-40,cx+40,cy+40),outline=CRE,width=6); d.line((cx,cy,cx,cy-26),fill=CRE,width=6); d.line((cx,cy,cx+20,cy+10),fill=CRE,width=6)
        elif i==1:
            d.ellipse((cx-30,cy-46,cx+30,cy+14),fill=CRE); d.polygon([(cx-26,cy-6),(cx+26,cy-6),(cx,cy+44)],fill=CRE); d.ellipse((cx-12,cy-28,cx+12,cy-4),fill=BG)
        else: star(d,cx,cy,40,LAV)
        d.text((cx-tw(d,lbl,f("bold",32))/2,cy+105),lbl,font=f("bold",32),fill=CRE)
    center(d,1280,"Así quien llega por primera vez\nsabe cuándo y dónde encontrarte.",f("bold",44),CRE,14)
    center(d,1440,"Actualízala si cambias algo.",f("reg",40),LAV)
    sign(d,"tr"); return im

def h07():
    im=base((540,900),(70,40,170)); d=ImageDraw.Draw(im)
    for i,(l,c) in enumerate([("M",VIO),("T",LAV)]):
        cx=410+i*260; d.ellipse((cx-120,300,cx+120,540),fill=c,outline=CRE,width=6)
        d.text((cx-tw(d,l,f("heros",140))/2,335),l,font=f("heros",140),fill=CRE if i==0 else BG)
    center(d,580,"Maciel (contador público) y Tripicchio",f("reg",36),LAV)
    center(d,630,"dos personas reales",f("mono",30),CRE)
    center(d,720,"Escribe",f("play",110),CRE,0)
    d.rounded_rectangle((240,870,840,1070),50,fill=CRE)
    center(d,890,"TRIPI",f("heros",150),BG,0)
    center(d,1110,"y en",f("bold",54),CRE,0)
    d.rounded_rectangle((300,1190,780,1330),40,fill=BG,outline=VIO,width=4)
    center(d,1198,"24 horas",f("heros",96),LIM,0)
    center(d,1370,"tienes tu propuesta, sin costo.",f("bold",52),CRE)
    star(d,150,820,40,VIO); sign(d,"tr"); return im

def h08():
    im=base((540,600),(60,40,160)); d=ImageDraw.Draw(im)
    pill(d,215,"PREGÚNTANOS",f("mono",30),fill=CARD,col=LAV)
    center(d,300,"¿Qué pregunta",f("black",90),CRE,0)
    center(d,410,"te hacen todos los días?",f("play",80),LAV,0)
    d.rounded_rectangle((150,600,930,1220),50,outline=(60,64,130),width=4)
    center(d,1280,"Precio, horario, si hay envío...",f("reg",40),LAV)
    center(d,1340,"Te responden Maciel y Tripicchio.",f("bold",40),CRE)
    star(d,960,1500,40,VIO); return im

for i,fn in enumerate([h01,h02,h03,h04,h05,h06,h07,h08],1):
    im=fn(); p=os.path.join(OUT,f"historia-{i:02d}")
    im.save(p+".png"); im.save(p+".jpg",quality=95)
print("PROVISORIO:",PROV)
