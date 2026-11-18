# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"_base.py"),encoding="utf-8").read())
D5="C:/Users/PC/tripiciel-assets/semana-01/dia-05/"
WORK=os.path.join(OUT,"_work"); os.makedirs(WORK,exist_ok=True)
PROV=[]

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

def frame_reel1():
    for n in ("fotograma.jpg","fotograma.png"):
        p=D5+"reels/reel-1/"+n
        if os.path.exists(p): return Image.open(p)
    PROV.append("reel-1")
    s=Image.new("RGB",(540,960),(246,242,234)); d=ImageDraw.Draw(s); N=(20,20,30)
    d.text((30,90),"negocio.de.ejemplo",font=f("bold",30),fill=N)
    d.ellipse((30,140,170,280),fill=(200,196,230)); star(d,100,210,40,VIO)
    for i,(a,b) in enumerate([("48","publicaciones"),("312","seguidores")]):
        d.text((220+i*150,165),a,font=f("bold",34),fill=N); d.text((220+i*150,208),b,font=f("reg",20),fill=N)
    d.text((30,300),"Negocio de ejemplo",font=f("bold",28),fill=N)
    d.text((30,338),"Bienvenidos :)",font=f("reg",26),fill=N)
    y=390
    for t in ["¿Dónde estás?","¿A qué hora abres?","¿Cómo te pido?"]:
        d.rounded_rectangle((30,y,510,y+66),16,fill=(255,225,225),outline=(220,60,60),width=3)
        d.text((50,y+16),"x  "+t,font=f("bold",28),fill=(190,40,40)); y+=84
    for r in range(2):
        for c in range(3):
            d.rectangle((30+c*162,680+r*160,186+c*162,834+r*160),fill=(205,200,225))
    return s

def h01():
    im=base((540,780),(70,40,170)); d=ImageDraw.Draw(im)
    pill(d,250,"SEMANA 01 · DÍA 05",f("mono",30),fill=CARD,col=LAV)
    star(d,540,720,300,VIO); star(d,540,720,130,CRE); star(d,830,480,46,LIM); star(d,240,950,30,LAV)
    center(d,1080,"MIÉRCOLES",f("heros",160),CRE,0)
    center(d,1280,"de perfil",f("play",140),LAV,0)
    center(d,1480,"Hoy revisamos lo que tu perfil\nle dice a quien llega por primera vez.",f("reg",40),CRE)
    return im

def h02():
    im=base((540,900),(50,40,160),stripes=True); d=ImageDraw.Draw(im)
    pill(d,240,"ENCUESTA RÁPIDA",f("mono",32),fill=CARD,col=LIM)
    center(d,360,"¿Tu perfil",f("black",110),CRE,0)
    center(d,490,"dice tu horario?",f("play",104),LAV,0)
    for i,(t,sub,fill,col) in enumerate([("SÍ","Está en la biografía",VIO,CRE),("NO","Todavía no",CRE,BG)]):
        y=740+i*290
        d.rounded_rectangle((110,y,970,y+240),50,fill=fill)
        d.text((170,y+50),t,font=f("heros",130),fill=col)
        d.text((480,y+70),sub,font=f("reg",40),fill=col)
        d.text((480,y+130),"Respóndelo por mensaje",font=f("mono",28),fill=(CRE if i==0 else VIO))
    center(d,1350,"Respóndenos SÍ o NO por mensaje",f("bold",48),CRE)
    center(d,1430,"y te decimos qué agregar.",f("reg",42),LAV)
    sign(d,"tr"); return im

def h03():
    im=base((540,1000),(60,40,170)); d=ImageDraw.Draw(im)
    pill(d,215,"NUEVO REEL",f("mono",30),fill=CARD,col=LAV)
    center(d,300,"¿Tu perfil dice",f("black",76),CRE,0)
    center(d,390,"dónde, cuándo y cómo?",f("play",76),LAV,0)
    phone(im,frame_reel1(),(330,560,750,1307)); d=ImageDraw.Draw(im)
    star(d,900,700,40,LAV); star(d,170,1200,30,LIM)
    arrow_cta(d,1420); sign(d,"tr"); return im

def h04():
    im=base((540,900),(55,40,165)); d=ImageDraw.Draw(im)
    pill(d,215,"DETRÁS DE ESCENA",f("mono",30),fill=CARD,col=LAV)
    center(d,300,"Así trabajamos",f("black",86),CRE,0)
    center(d,400,"un pedido",f("play",100),LAV,0)
    steps=[("1","Escuchamos","Qué vendes y a quién."),("2","Planificamos","Qué publicar y cuándo."),
           ("3","Grabamos y editamos","Videos listos para subir."),("4","Revisamos juntos","Nada sale sin tu visto bueno.")]
    y=560
    for n,t,s in steps:
        d.rounded_rectangle((90,y,990,y+190),40,fill=CARD,outline=(40,44,96),width=3)
        d.ellipse((130,y+45,230,y+145),fill=VIO); d.text((180-tw(d,n,f("heros",60))/2,y+58),n,font=f("heros",60),fill=CRE)
        d.text((270,y+40),t,font=f("bold",52),fill=CRE); d.text((270,y+110),s,font=f("reg",36),fill=LAV)
        if n!="4": d.line((180,y+190,180,y+220),fill=VIO,width=6)
        y+=220
    center(d,1470,"Maciel y Tripicchio: dos personas reales.",f("mono",32),LAV)
    sign(d,"tr"); return im

def h05():
    im=base((540,1000),(60,40,170),stripes=True); d=ImageDraw.Draw(im)
    pill(d,215,"ANTES / DESPUÉS · NACUSI MUEBLES",f("mono",28),fill=CARD,col=LAV)
    center(d,300,"Misma cómoda,",f("black",86),CRE,0)
    center(d,400,"otro video",f("play",100),LAV,0)
    for i,(fn,lbl,fill,col) in enumerate([("antes.png","ANTES",CRE,BG),("despues.png","DESPUÉS",VIO,CRE)]):
        s=Image.open(os.path.join(WORK,fn)).convert("RGB").crop((162,340,918,1560)).resize((430,694),Image.LANCZOS)
        x0=90+i*470
        m=Image.new("L",(430,694),0); ImageDraw.Draw(m).rounded_rectangle((0,0,430,694),36,fill=255)
        d.rounded_rectangle((x0-8,552,x0+438,1262),42,outline=fill,width=6); im.paste(s,(x0,560),m)
        d=ImageDraw.Draw(im); pill(d,580,lbl,f("bold",36),fill=fill,col=col,x=x0+20)
    d.rounded_rectangle((150,1300,930,1460),40,fill=BG,outline=VIO,width=4)
    center(d,1325,"63 s  →  21 s",f("heros",100),LIM,0)
    center(d,1490,"Luz, color y ritmo ajustados.",f("reg",40),CRE)
    sign(d,"tr"); return im

def h06():
    im=base((540,800),(50,40,150)); d=ImageDraw.Draw(im)
    pill(d,215,"TIP RÁPIDO",f("mono",30),fill=CARD,col=LAV)
    center(d,300,"Fotos de producto",f("black",80),CRE,0)
    center(d,395,"con tu celular",f("play",96),LAV,0)
    d.rounded_rectangle((140,560,520,1000),20,fill=(40,46,110),outline=CRE,width=8)
    d.line((330,560,330,1000),fill=CRE,width=8); d.line((140,780,520,780),fill=CRE,width=8)
    for k in range(6): d.line((520,620+k*60,700,700+k*60),fill=(120,110,200),width=4)
    d.rounded_rectangle((690,820,900,1000),16,fill=CRE); d.rectangle((660,1000,940,1020),fill=LAV)
    d.ellipse((760,860,830,930),fill=VIO)
    center(d,1060,"Pon el producto junto a una ventana,\ncon luz de día y de costado.",f("bold",44),CRE,14)
    center(d,1210,"Sin flash. Fondo liso. Limpia la lente.",f("reg",40),LAV)
    pill(d,1360,"Más consejos en el carrusel del perfil",f("bold",40),fill=VIO,col=CRE)
    sign(d,"tr"); return im

def h07():
    im=base((540,900),(70,40,170)); d=ImageDraw.Draw(im)
    for i,(l,c) in enumerate([("M",VIO),("T",LAV)]):
        cx=410+i*260; d.ellipse((cx-120,300,cx+120,540),fill=c,outline=CRE,width=6)
        d.text((cx-tw(d,l,f("heros",140))/2,335),l,font=f("heros",140),fill=CRE if i==0 else BG)
    center(d,580,"Maciel (contador público) y Tripicchio",f("reg",36),LAV)
    center(d,700,"Escribe",f("play",110),CRE,0)
    d.rounded_rectangle((240,860,840,1060),50,fill=CRE)
    center(d,880,"TRIPI",f("heros",150),BG,0)
    center(d,1110,"y en",f("bold",54),CRE,0)
    d.rounded_rectangle((300,1190,780,1330),40,fill=BG,outline=VIO,width=4)
    center(d,1198,"24 horas",f("heros",96),LIM,0)
    center(d,1370,"tienes tu propuesta, sin costo.",f("bold",52),CRE)
    star(d,150,800,40,VIO); sign(d,"tr"); return im

def h08():
    im=base((540,600),(60,40,160)); d=ImageDraw.Draw(im)
    pill(d,215,"PREGÚNTANOS",f("mono",30),fill=CARD,col=LAV)
    center(d,310,"¿Qué dato le falta",f("black",84),CRE,0)
    center(d,410,"a tu perfil?",f("play",110),LAV,0)
    d.rounded_rectangle((150,640,930,1240),50,outline=(60,64,130),width=4)
    center(d,1290,"Dirección, horario, cómo pedir...",f("reg",40),LAV)
    center(d,1350,"Te responden Maciel y Tripicchio.",f("bold",40),CRE)
    star(d,960,1500,40,VIO); return im

for i,fn in enumerate([h01,h02,h03,h04,h05,h06,h07,h08],1):
    im=fn(); p=os.path.join(OUT,f"historia-{i:02d}")
    im.save(p+".png"); im.save(p+".jpg",quality=95)
print("PROVISORIO:",PROV)
