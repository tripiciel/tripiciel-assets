# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
import os, subprocess
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"_base.py"),encoding="utf-8").read())
LOGO="C:/Users/PC/tripiciel-assets/semana-01/dia-01/reels/reel-4/"
D4="C:/Users/PC/tripiciel-assets/semana-01/dia-04/"
WORK=os.path.join(OUT,"_work"); os.makedirs(WORK,exist_ok=True)
PROV=[]  # provisional frames used

def logo(im,y=1540,w=280):
    try:
        lg=Image.open(LOGO+"logo-horizontal.png").convert("RGBA"); lg=lg.resize((w,int(lg.height*w/lg.width)))
        im.paste(lg,((W-w)//2,y),lg)
    except Exception: pass

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
    p=D4+"reels/reel-1/fotograma.png"
    if os.path.exists(p): return Image.open(p)
    q=os.path.join(WORK,"reel1-provisorio.png")
    if not os.path.exists(q):
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss","20","-i","C:/Users/PC/video-editor/projects/chicho-onix/outputs/chicho-onix.final.mp4","-frames:v","1",q],check=True)
    PROV.append("reel-1"); return Image.open(q)

def frame_reel3():
    p=D4+"reels/reel-3/fotograma.png"
    if os.path.exists(p): return Image.open(p)
    PROV.append("reel-3")
    s=Image.new("RGB",(540,960),(236,229,221)); d=ImageDraw.Draw(s)
    d.rectangle((0,0,540,170),fill=(18,22,52)); d.ellipse((24,80,84,140),fill=VIO)
    d.text((100,82),"Negocio de ejemplo",font=f("bold",28),fill=CRE); d.text((100,118),"en línea",font=f("reg",22),fill=LAV)
    y=190
    for me,t in [(0,"Hola, ¿tienen pizza\nmuzzarella para hoy?"),(1,"¡Hola! Sí. ¿Grande o\nmediana?"),(0,"Grande, para retirar"),(1,"Listo, pedido anotado:\n1 grande para retirar.\n¿A nombre de quién?"),(0,"Laura"),(1,"Gracias, Laura. Te\navisamos cuando esté.")]:
        fo=f("reg",26); lines=t.split("\n"); bw=max(d.textlength(l,font=fo) for l in lines)+40; bh=len(lines)*34+26
        x=500-bw if not me else 40
        d.rounded_rectangle((x,y,x+bw,y+bh),18,fill=(217,253,211) if not me else (255,255,255))
        for i,l in enumerate(lines): d.text((x+20,y+13+i*34),l,font=fo,fill=(20,20,30))
        y+=bh+22
    d.rounded_rectangle((30,y+20,510,y+80),30,fill=(18,22,52))
    d.text((60,y+36),"Demostración · negocio de ejemplo",font=f("mono",22),fill=LIM)
    s.save(os.path.join(WORK,"reel3-provisorio.png")); return s

def h01():
    im=base((540,780),(70,40,170)); d=ImageDraw.Draw(im)
    pill(d,250,"SEMANA 01 · DÍA 04",f("mono",30),fill=CARD,col=LAV)
    star(d,540,720,300,VIO); star(d,540,720,130,CRE); star(d,830,480,46,LIM); star(d,240,950,30,LAV)
    center(d,1080,"MARTES",f("heros",190),CRE,0)
    center(d,1300,"de ideas",f("play",140),LAV,0)
    center(d,1490,"Hoy: casos reales, bots y 10 ideas.",f("reg",42),CRE)
    return im

def h02():
    im=base((540,1000),(60,40,170),stripes=True); d=ImageDraw.Draw(im)
    pill(d,215,"ANTES / DESPUÉS · CHICHO CARS",f("mono",28),fill=CARD,col=LAV)
    center(d,300,"Mismo Onix,",f("black",86),CRE,0)
    center(d,400,"otro video",f("play",100),LIM,0)
    fr=frame_reel1(); phone(im,fr,(330,560,750,1307))
    if "reel-1" in PROV:  # patente visible en el cuadro provisorio
        r=(330,1110,440,1280); im.paste(im.crop(r).filter(ImageFilter.GaussianBlur(14)),r[:2])
    d=ImageDraw.Draw(im)
    d.text((80,1180),"Final:",font=f("reg",36),fill=LAV); d.text((80,1225),"1:34",font=f("black",80),fill=LIM)
    star(d,900,700,40,LAV)
    arrow_cta(d,1420); sign(d,"tr"); return im

def h03():
    im=base((540,900),(40,50,160)); d=ImageDraw.Draw(im)
    pill(d,215,"CASO REAL · CLIENTES",f("mono",28),fill=VIO,col=CRE)
    center(d,300,"Chicho Cars",f("heros",120),CRE,0)
    y=470
    for lab,txt in [("QUIÉN ES","Concesionaria de autos usados."),("QUÉ HICIMOS","Editamos sus videos de venta.")]:
        d.rounded_rectangle((90,y,990,y+180),36,fill=CARD,outline=(50,50,120),width=3)
        d.text((140,y+32),lab,font=f("mono",30),fill=LAV); d.text((140,y+88),txt,font=f("bold",50),fill=CRE); y+=210
    d.text((90,y+20),"EL RESULTADO",font=f("mono",30),fill=LAV); y+=80
    d.rounded_rectangle((90,y,990,y+330),40,fill=CRE)
    d.text((140,y+30),"Chevrolet Aveo",font=f("play",56),fill=BG)
    d.rounded_rectangle((140,y+120,400,y+230),24,fill=BG); d.text((165,y+130),"2:57",font=f("black",80),fill=LIM)
    d.line((430,y+175,520,y+175),fill=VIO,width=10); d.polygon([(545,y+175),(515,y+150),(515,y+200)],fill=VIO)
    d.rounded_rectangle((570,y+120,830,y+230),24,fill=BG); d.text((595,y+130),"1:31",font=f("black",80),fill=LIM)
    d.text((140,y+252),"de video crudo a video final",font=f("reg",36),fill=BG)
    y+=370
    d.text((90,y),"Y el del Onix: final de",font=f("reg",44),fill=CRE); d.text((560,y-14),"1:34",font=f("black",70),fill=LIM)
    sign(d,"tr"); return im

def h04():
    im=base((540,1000),(40,60,150)); d=ImageDraw.Draw(im)
    pill(d,215,"CARRUSEL NUEVO",f("mono",28),fill=VIO,col=CRE)
    p=D4+"carrusel/slide-01.png"; box=(170,320,910,1245)
    d.rounded_rectangle((box[0]-12,box[1]-12,box[2]+12,box[3]+12),46,outline=VIO,width=6)
    if os.path.exists(p):
        s=Image.open(p).convert("RGB").resize((box[2]-box[0],box[3]-box[1]),Image.LANCZOS)
        m=Image.new("L",s.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0)+s.size,36,fill=255); im.paste(s,box[:2],m)
    else:
        PROV.append("carrusel")
        d.rounded_rectangle(box,36,fill=CRE); star(d,840,400,34,VIO)
        d.rounded_rectangle((230,420,500,700),30,fill=BG); d.text((262,420),"10",font=f("black",220),fill=LIM)
        left(d,230,760,"ideas para\npublicar\nesta semana",f("black",84),BG,6)
        d.text((230,1080),"en tu negocio",font=f("play",80),fill=VIO)
    d=ImageDraw.Draw(im)
    center(d,1300,"10 ideas para tu negocio",f("heros",64),CRE)
    arrow_cta(d,1420,"Míralo en el perfil"); sign(d,"tl"); return im

def h05():
    im=base((540,700),(80,40,160)); d=ImageDraw.Draw(im)
    pill(d,230,"TIP DEL DÍA",f("mono",30),fill=CARD,col=LAV)
    center(d,340,"Responde en video",f("black",88),CRE,0)
    center(d,460,"la pregunta que",f("play",96),LAV,0)
    center(d,580,"más te hacen",f("heros",100),CRE,0)
    d.rounded_rectangle((120,780,960,980),40,fill=CARD,outline=(50,50,120),width=3)
    d.text((170,815),"“¿Cuánto cuesta?”",font=f("bold",56),fill=CRE); d.text((170,900),"“¿Hacen envíos?”",font=f("reg",44),fill=LAV)
    y=1040
    for t in ["Te ahorra explicar lo mismo cada día.","Lo mandas como respuesta en el chat.","Muestra que conoces tu negocio."]:
        d.ellipse((130,y+8,170,y+48),fill=VIO); d.text((200,y+2),t,font=f("reg",40),fill=CRE); y+=100
    star(d,880,1420,60,LIM); sign(d,"tr"); return im

def h06():
    im=base((540,1100),(70,50,180),stripes=True); d=ImageDraw.Draw(im)
    pill(d,215,"BOTS · DEMOSTRACIÓN",f("mono",28),fill=CARD,col=LAV)
    center(d,295,"Tu negocio vende",f("black",80),CRE,0)
    center(d,395,"aunque esté cerrado",f("play",80),LIM,0)
    phone(im,frame_reel3(),(330,540,750,1287)); d=ImageDraw.Draw(im)
    star(d,180,800,34,LAV)
    center(d,1335,"Ejemplo hecho para un negocio de muestra.",f("reg",32),LAV)
    arrow_cta(d,1420); sign(d,"tr"); return im

def h07():
    im=base((540,900),(50,40,160)); d=ImageDraw.Draw(im)
    pill(d,230,"BOTS",f("mono",30),fill=VIO,col=CRE)
    center(d,320,"Un bot puede",f("play",120),CRE,0)
    y=540
    for n,t in [("01","Tomar pedidos"),("02","Dar precios"),("03","Agendar turnos")]:
        d.rounded_rectangle((90,y,990,y+180),40,fill=CARD,outline=(50,50,120),width=3)
        d.text((140,y+48),n,font=f("mono",72),fill=LAV); d.text((310,y+55),t,font=f("bold",64),fill=CRE); y+=215
    d.rounded_rectangle((90,y+10,990,y+230),40,fill=CRE)
    d.text((140,y+60),"Todo,",font=f("play",80),fill=BG)
    d.rounded_rectangle((420,y+40,940,y+200),30,fill=BG); d.text((460,y+50),"las 24 h",font=f("black",104),fill=LIM)
    bot_icon(d,880,300,50); sign(d,"tl"); return im

def mt_card(d,box,ch,name,role,col):
    x0,y0,x1,y1=box
    d.rounded_rectangle(box,44,fill=CARD,outline=col,width=5)
    cx=(x0+x1)//2; d.ellipse((cx-110,y0+60,cx+110,y0+280),fill=col)
    fo=f("black",150); d.text((cx-tw(d,ch,fo)/2,y0+80),ch,font=fo,fill=BG if col!=VIO else CRE)
    fo=f("bold",50); d.text((cx-tw(d,name,fo)/2,y0+320),name,font=fo,fill=CRE)
    fo=f("reg",34); d.text((cx-tw(d,role,fo)/2,y0+390),role,font=fo,fill=LAV)

def h08():
    im=base((540,1000),(40,40,150),stripes=True); d=ImageDraw.Draw(im)
    pill(d,230,"CÓMO TRABAJAMOS",f("mono",28),fill=VIO,col=CRE)
    center(d,330,"Somos dos",f("play",130),CRE,0)
    mt_card(d,(90,560,520,1040),"M","Maciel","persona real",VIO)
    mt_card(d,(560,560,990,1040),"T","Tripicchio","persona real",LAV)
    center(d,1120,"Hablas directo con",f("reg",52),CRE)
    center(d,1190,"quien hace tu contenido.",f("black",64),CRE)
    center(d,1320,"Sin intermediarios.",f("mono",34),LAV)
    logo(im,1500,260); sign(d,"tr"); return im

def h09():
    im=base((540,800),(80,50,190)); d=ImageDraw.Draw(im)
    star(d,540,330,70,LIM)
    center(d,440,"Esta semana",f("play",104),LAV,0)
    center(d,580,"tomamos",f("black",110),CRE,0)
    center(d,710,"marcas nuevas",f("heros",100),CRE,0)
    center(d,900,"Escribe",f("reg",56),CRE)
    fo=f("heros",170); t="TRIPI"; pw=tw(d,t,fo)+100
    d.rounded_rectangle(((W-pw)/2,980,(W+pw)/2,1210),60,fill=VIO); d.text(((W-tw(d,t,fo))/2,995),t,font=fo,fill=CRE)
    center(d,1270,"y en 24 horas te enviamos una propuesta\npara tu marca, sin costo.",f("reg",40),CRE)
    logo(im,1480,260); return im

def h10():
    im=base((540,700),(80,40,160)); d=ImageDraw.Draw(im)
    pill(d,230,"CAJA DE PREGUNTAS",f("mono",28),fill=CARD,col=LAV)
    center(d,340,"¿Qué te cuesta más",f("black",76),CRE,4)
    center(d,435,"de las redes",f("play",96),LAV,0)
    center(d,560,"de tu negocio?",f("black",76),CRE,4)
    d.rounded_rectangle((150,760,930,1240),44,outline=VIO,width=6)
    center(d,1320,"Te respondemos en historias.",f("reg",42),CRE); sign(d,"tr"); return im

def cover(icon):
    im=Image.new("RGB",(W,H),BG); g=Image.new("RGB",(W,H),0); ImageDraw.Draw(g).ellipse((140,560,940,1360),fill=(60,50,170))
    im=ImageChops.add(im,g.filter(ImageFilter.GaussianBlur(160))); d=ImageDraw.Draw(im)
    d.ellipse((290,710,790,1210),fill=VIO); icon(d); star(d,780,720,40,LIM); return im
def ic_clients(d):
    # storefront with handshake-free simple shape: shop + check
    d.rounded_rectangle((400,900,680,1080),18,outline=CRE,width=14)
    d.polygon([(380,900),(700,900),(670,830),(410,830)],fill=CRE)
    for i in range(4): d.line((410+i*80,830,400+i*93,900),fill=VIO,width=8)
    d.rectangle((510,980,570,1080),fill=LAV)
    d.ellipse((600,960,700,1060),fill=LIM); d.line([(625,1010),(645,1032),(678,990)],fill=BG,width=12)

for i,fn in enumerate([h01,h02,h03,h04,h05,h06,h07,h08,h09,h10],1): fn().save(os.path.join(OUT,f"historia-{i:02d}.png"))
cover(ic_clients).save(os.path.join(OUT,"destacada-clientes.png"))
print("PROVISORIOS:",sorted(set(PROV)) or "ninguno")
