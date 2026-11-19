# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"_base.py"),encoding="utf-8").read())
CAP="C:/Users/PC/tripiciel-assets/semana-01/dia-07/_capturas/"
FBG=(251,248,241); FGR=(31,122,77); FDK=(15,61,39); FOR=(242,163,58)

def phone(im,shot,box,cut=2150):
    # recorta la parte baja de la captura: ahi esta el boton "Powered by Netlify"
    x0,y0,x1,y1=box; d=ImageDraw.Draw(im); bw,bh=x1-x0,y1-y0
    d.rounded_rectangle((x0-24,y0-24,x1+24,y1+24),84,fill=(28,30,64),outline=VIO,width=6)
    s=shot.convert("RGB").crop((0,0,shot.width,cut)); sc=max(bw/s.width,bh/s.height)
    s=s.resize((int(s.width*sc+.5),int(s.height*sc+.5)),Image.LANCZOS)
    l=(s.width-bw)//2; s=s.crop((l,0,l+bw,bh))
    m=Image.new("L",(bw,bh),0); ImageDraw.Draw(m).rounded_rectangle((0,0,bw,bh),62,fill=255); im.paste(s,(x0,y0),m)

def h01():
    im=base((540,1000),(70,40,170)); d=ImageDraw.Draw(im)
    pill(d,220,"SEMANA 01 · DÍA 07",f("mono",30),fill=CARD,col=LAV)
    center(d,300,"Hoy te mostramos",f("black",86),CRE,0)
    center(d,400,"algo que hicimos",f("play",96),LAV,0)
    d.rounded_rectangle((40,1300,290,1380),40,fill=FGR); d.text((72,1318),"Fiadito",font=f("bold",40),fill=FBG)
    phone(im,Image.open(CAP+"movil-inicio.png"),(330,560,800,1400)); d=ImageDraw.Draw(im)
    star(d,920,700,46,LAV); star(d,180,700,34,FOR); star(d,900,1300,26,LIM)
    center(d,1470,"Una app para el fiado del negocio,",f("bold",42),CRE)
    center(d,1530,"hecha por Maciel y Tripicchio.",f("reg",40),LAV)
    sign(d,"tl"); return im

def h02():
    im=base((540,900),(50,40,160),stripes=True); d=ImageDraw.Draw(im)
    pill(d,215,"FIADITO EN 3 PASOS",f("mono",30),fill=CARD,col=LAV)
    center(d,295,"Así funciona",f("black",96),CRE,0)
    x0,x1=80,1000; d.rounded_rectangle((x0,440,x1,1360),44,fill=FBG)
    rows=[("1","Anotas el fiado","en ",("5 segundos",)),("2","Recuerdas por WhatsApp","con un toque",None),("3","Marcas \"Pagado\"","y el saldo baja solo",None)]
    y=480
    for n,t,s,num in rows:
        d.ellipse((x0+40,y+20,x0+190,y+170),fill=FDK if n!="2" else FGR)
        d.text((x0+115-tw(d,n,f("heros",100))/2,y+30),n,font=f("heros",100),fill=FBG)
        d.text((x0+230,y+30),t,font=f("bold",50),fill=FDK)
        if num:
            d.text((x0+230,y+100),"en",font=f("play",50),fill=FGR)
            bx=x0+300; d.rounded_rectangle((bx,y+94,bx+310,y+174),18,fill=BG); d.text((bx+22,y+104),"5 segundos",font=f("heros",50),fill=LIM)
        else: d.text((x0+230,y+100),s,font=f("play",50),fill=FGR)
        if n!="3": d.line((x0+40,y+260,x1-40,y+260),fill=(225,220,205),width=3)
        y+=290
    d.rounded_rectangle((x1-240,1270,x1-40,1340),35,fill=FOR); d.text((x1-210,1283),"Fiadito",font=f("bold",38),fill=FDK)
    fo=f("bold",46); t="Mira el reel en el perfil"; bw=tw(d,t,fo)+150; x=(W-bw)/2; yy=1440
    d.rounded_rectangle((x,yy,x+bw,yy+100),50,fill=VIO); d.text((x+40,yy+24),t,font=fo,fill=CRE)
    ax=x+bw-75; d.line((ax-28,yy+50,ax+18,yy+50),fill=CRE,width=8); d.polygon([(ax+30,yy+50),(ax+6,yy+30),(ax+6,yy+70)],fill=CRE)
    sign(d,"tr"); return im

def h03():
    im=base((540,900),(60,40,165)); d=ImageDraw.Draw(im)
    pill(d,215,"ENCUESTA RÁPIDA",f("mono",30),fill=CARD,col=LAV)
    center(d,300,"¿En tu negocio",f("black",90),CRE,0)
    center(d,410,"todavía se anota",f("play",96),LAV,0)
    center(d,530,"en cuaderno?",f("heros",110),CRE,0)
    for i,(t,sub,fill,col) in enumerate([("SÍ","Uso cuaderno",CRE,BG),("NO","Ya lo dejé",VIO,CRE)]):
        y=760+i*300; d.rounded_rectangle((100,y,980,y+250),50,fill=fill)
        d.text((160,y+50),t,font=f("heros",140),fill=col)
        d.text((520,y+70),sub,font=f("bold",44),fill=col)
        d.text((520,y+140),"Escríbelo por mensaje",font=f("mono",28),fill=(VIO if i==0 else CRE))
    # cuaderno dibujado
    d.rounded_rectangle((340,810,430,960),12,fill=FOR); [d.line((352,840+k*30,418,840+k*30),fill=FDK,width=4) for k in range(4)]
    center(d,1380,"Responde SÍ o NO por mensaje.",f("bold",50),CRE)
    center(d,1450,"Te leemos nosotros dos.",f("reg",42),LAV)
    sign(d,"tl"); return im

def h04():
    im=base((540,900),(70,40,170)); d=ImageDraw.Draw(im)
    center(d,230,"¿Tu negocio necesita",f("black",76),CRE,0)
    center(d,320,"su propia app o web?",f("play",84),LAV,0)
    for i,(l,c) in enumerate([("M",VIO),("T",LAV)]):
        cx=410+i*260; d.ellipse((cx-115,460,cx+115,690),fill=c,outline=CRE,width=6)
        d.text((cx-tw(d,l,f("heros",130))/2,495),l,font=f("heros",130),fill=CRE if i==0 else BG)
    center(d,720,"Maciel y Tripicchio",f("bold",44),CRE)
    center(d,780,"dos personas reales",f("mono",32),LAV)
    center(d,860,"Escribe",f("play",100),CRE,0)
    d.rounded_rectangle((240,990,840,1180),50,fill=CRE); center(d,1005,"TRIPI",f("heros",145),BG,0)
    center(d,1210,"por mensaje y en",f("bold",50),CRE,0)
    d.rounded_rectangle((300,1285,780,1415),40,fill=BG,outline=VIO,width=4); center(d,1292,"24 horas",f("heros",92),LIM,0)
    center(d,1445,"te enviamos una propuesta\npara tu marca, sin costo.",f("bold",48),CRE,8)
    star(d,140,900,40,VIO); star(d,950,560,30,FOR); sign(d,"br"); return im

OUT2=OUT
for i,fn in enumerate([h01,h02,h03,h04],1):
    im=fn(); p=os.path.join(OUT2,f"historia-{i:02d}"); im.save(p+".png"); im.save(p+".jpg",quality=95)
