# /// script
# dependencies = ["pillow"]
# [tool.uv]
# exclude-newer = "14 days"
# ///
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.dirname(os.path.abspath(__file__))
F = "C:/Users/PC/video-editor/assets/fonts/"
W, H = 1080, 1920
BG = (7, 10, 28); VIO = (91, 91, 245); LAV = (169, 156, 255); CRE = (246, 242, 234); LIM = (198, 244, 50)
CARD = (18, 22, 52)

def font(name, size):
    p = {"inter-black": F + "Inter-Black.otf", "inter-bold": F + "Inter-Bold.otf", "inter": F + "Inter-Regular.otf",
         "play": F + "PlayfairDisplay-Italic-VF.ttf", "mono": F + "IBMPlexMono-Bold.ttf", "heros": F + "texgyreheros-bold.otf"}[name]
    return ImageFont.truetype(p, size)

def base(glow=(540, 700)):
    im = Image.new("RGB", (W, H), BG)
    g = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(g)
    d.ellipse((glow[0] - 520, glow[1] - 520, glow[0] + 520, glow[1] + 520), fill=(40, 36, 130))
    g = g.filter(ImageFilter.GaussianBlur(220))
    im = Image.blend(im, Image.eval(Image.composite(g, im, Image.new("L", (W, H), 255)), lambda v: v), 0.0)
    im = Image.fromarray if False else im
    from PIL import ImageChops
    im = ImageChops.add(im, g)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 60):  # subtle dot grid
        for y in range(0, H, 60):
            d.point((x, y), fill=(28, 32, 70))
    return im

def star(d, cx, cy, r, col=VIO):
    pts = []
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.28
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)

def sign(d, corner="tr"):
    pos = {"tr": (960, 290), "tl": (120, 290), "br": (960, 1540), "bl": (120, 1540)}[corner]
    star(d, *pos, 42)

def center(d, y, text, f, col=CRE, spacing=10):
    lines = text.split("\n"); yy = y
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((W - w) / 2, yy), ln, font=f, fill=col)
        yy += f.size + spacing
    return yy

def left(d, x, y, text, f, col=CRE, spacing=10):
    for ln in text.split("\n"):
        d.text((x, y), ln, font=f, fill=col); y += f.size + spacing
    return y

def card(d, box, r=40, fill=CARD, outline=(52, 56, 120), w=3):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=w)

def pill(d, x, y, text, f, fill=VIO, col=CRE, center_x=False):
    tw = d.textlength(text, font=f); pw = tw + 60
    if center_x: x = (W - pw) / 2
    d.rounded_rectangle((x, y, x + pw, y + f.size + 34), (f.size + 34) // 2, fill=fill)
    d.text((x + 30, y + 15), text, font=f, fill=col)
    return pw

# ---------------- icons ----------------
def ic_play(d, cx, cy, s, col=CRE):
    d.rounded_rectangle((cx - s, cy - s * .7, cx + s, cy + s * .7), s * .2, outline=col, width=int(s * .1))
    d.polygon([(cx - s * .25, cy - s * .35), (cx - s * .25, cy + s * .35), (cx + s * .4, cy)], fill=LIM)

def ic_pen(d, cx, cy, s, col=CRE):
    d.ellipse((cx - s, cy - s, cx + s, cy + s), outline=col, width=int(s * .1))
    d.ellipse((cx - s * .55, cy - s * .55, cx + s * .05, cy + s * .05), fill=VIO)
    d.ellipse((cx - s * .05, cy - s * .05, cx + s * .6, cy + s * .6), fill=LAV)
    d.ellipse((cx + s * .05, cy - s * .6, cx + s * .5, cy - s * .15), fill=LIM)

def ic_web(d, cx, cy, s, col=CRE):
    d.rounded_rectangle((cx - s, cy - s * .75, cx + s, cy + s * .75), s * .15, outline=col, width=int(s * .1))
    d.line((cx - s, cy - s * .4, cx + s, cy - s * .4), fill=col, width=int(s * .08))
    for i in range(3): d.ellipse((cx - s * .8 + i * s * .2, cy - s * .62, cx - s * .7 + i * s * .2, cy - s * .52), fill=LAV)
    d.rounded_rectangle((cx - s * .75, cy - s * .2, cx + s * .1, cy + s * .05), 8, fill=VIO)
    d.rounded_rectangle((cx - s * .75, cy + s * .2, cx - s * .1, cy + s * .5), 8, fill=LIM)

def ic_bot(d, cx, cy, s, col=CRE):
    d.rounded_rectangle((cx - s, cy - s * .6, cx + s, cy + s * .7), s * .3, outline=col, width=int(s * .1))
    d.line((cx, cy - s * .6, cx, cy - s), fill=col, width=int(s * .08)); d.ellipse((cx - s * .14, cy - s * 1.14, cx + s * .14, cy - s * .86), fill=LIM)
    d.ellipse((cx - s * .55, cy - s * .2, cx - s * .2, cy + s * .15), fill=LAV); d.ellipse((cx + s * .2, cy - s * .2, cx + s * .55, cy + s * .15), fill=LAV)
    d.rounded_rectangle((cx - s * .35, cy + s * .3, cx + s * .35, cy + s * .42), 6, fill=VIO)

def ic_redes(d, cx, cy, s, col=CRE):
    d.rounded_rectangle((cx - s, cy - s, cx + s, cy + s), s * .4, outline=col, width=int(s * .1))
    d.ellipse((cx - s * .45, cy - s * .45, cx + s * .45, cy + s * .45), outline=LAV, width=int(s * .1))
    d.ellipse((cx + s * .5, cy - s * .7, cx + s * .7, cy - s * .5), fill=LIM)

def ic_beforeafter(d, cx, cy, s, col=CRE):
    d.rounded_rectangle((cx - s, cy - s * .8, cx - s * .08, cy + s * .8), s * .15, fill=(60, 60, 90))
    d.rounded_rectangle((cx + s * .08, cy - s * .8, cx + s, cy + s * .8), s * .15, fill=CRE)
    d.polygon([(cx + s * .4, cy - s * .25), (cx + s * .4, cy + s * .25), (cx + s * .75, cy)], fill=VIO)
    d.line((cx - s * .75, cy, cx - s * .33, cy), fill=col, width=int(s * .08))

ICONS = {"video": ic_play, "diseno": ic_pen, "web": ic_web, "bots": ic_bot, "redes": ic_redes}

# ---------------- 01 hola ----------------
def person(d, cx, cy, skin, hair, shirt, hair_style):
    # torso
    d.rounded_rectangle((cx - 150, cy + 150, cx + 150, cy + 520), 120, fill=shirt)
    d.rectangle((cx - 40, cy + 110, cx + 40, cy + 170), fill=skin)  # neck
    d.ellipse((cx - 115, cy - 130, cx + 115, cy + 150), fill=skin)  # head
    if hair_style == "short":
        d.chord((cx - 125, cy - 150, cx + 125, cy + 60), 180, 360, fill=hair)
        d.ellipse((cx - 125, cy - 70, cx - 85, cy + 30), fill=hair)
    else:  # curly/top bun
        for a in range(-170, 10, 30):
            r = math.radians(a)
            x, y = cx + 105 * math.cos(r), cy - 20 + 105 * math.sin(r)
            d.ellipse((x - 55, y - 55, x + 55, y + 55), fill=hair)
        d.ellipse((cx - 55, cy - 230, cx + 55, cy - 120), fill=hair)
    # face: simple flat eyes + smile
    d.ellipse((cx - 55, cy + 10, cx - 30, cy + 40), fill=BG); d.ellipse((cx + 30, cy + 10, cx + 55, cy + 40), fill=BG)
    d.arc((cx - 50, cy + 30, cx + 50, cy + 105), 20, 160, fill=BG, width=10)

def h01():
    im = base((540, 1000)); d = ImageDraw.Draw(im)
    pill(d, 0, 250, "AGENCIA DIGITAL · 2 PERSONAS", font("mono", 30), fill=CARD, col=LAV, center_x=True)
    center(d, 340, "Hola,", font("play", 120), LAV)
    center(d, 470, "somos\nTripiciel", font("inter-black", 150), CRE, spacing=0)
    # illustration
    card(d, (110, 830, 970, 1440), 60, fill=(22, 24, 70), outline=VIO, w=4)
    d.ellipse((260, 900, 820, 1460), fill=(36, 36, 110))
    im2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d2 = ImageDraw.Draw(im2)
    person(d2, 380, 1060, (232, 190, 160), (40, 30, 60), VIO, "short")
    person(d2, 700, 1060, (200, 150, 120), (90, 50, 140), LAV, "curly")
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rounded_rectangle((110, 830, 970, 1440), 60, fill=255)
    a = im2.split()[3]; from PIL import ImageChops; a = ImageChops.multiply(a, mask); im2.putalpha(a)
    im.paste(im2, (0, 0), im2); d = ImageDraw.Draw(im)
    d.rounded_rectangle((110, 830, 970, 1440), 60, outline=VIO, width=4)
    pill(d, 170, 1370, "Maciel", font("inter-bold", 40), fill=CRE, col=BG)
    pill(d, 690, 1370, "Tripicchio", font("inter-bold", 40), fill=CRE, col=BG)
    center(d, 1500, "Videos, diseño, webs, bots y redes.\nTodo lo digital de tu marca.", font("inter", 46), CRE)
    sign(d, "tr")
    return im

# ---------------- 02-06 servicios ----------------
SERV = [
    ("video", "01 / 05", "Video", "Reels y videos editados\npara que tu marca se vea\ny se escuche bien.",
     ["Más gente frena a mirarte", "Explicas tu producto en 30 s", "Contenido listo cada semana"], "inter-black"),
    ("diseno", "02 / 05", "Diseño", "Logo, colores y piezas\npara redes con una sola\nidentidad.",
     ["Te reconocen al primer vistazo", "Tu marca se ve profesional", "Plantillas listas para usar"], "heros"),
    ("web", "03 / 05", "Web", "Una página rápida que\nexplica qué vendes y\ncómo contactarte.",
     ["Te encuentran en Google", "Consultas las 24 h", "Un link serio para tu bio"], "play"),
    ("bots", "04 / 05", "Bots", "Respuestas automáticas\nen WhatsApp e Instagram\nque atienden por ti.",
     ["Nadie queda sin respuesta", "Filtras curiosos de clientes", "Ganas horas cada semana"], "mono"),
    ("redes", "05 / 05", "Redes", "Planificamos, publicamos\ny respondemos para que\ntu cuenta no se apague.",
     ["Publicas constante sin pensar", "Una estrategia con objetivo", "Tiempo para tu negocio"], "inter-bold"),
]

def hserv(i):
    key, num, title, what, gains, tf = SERV[i]
    glows = [(900, 500), (180, 600), (540, 400), (850, 800), (200, 450)]
    im = base(glows[i]); d = ImageDraw.Draw(im)
    left(d, 90, 250, "SERVICIO " + num, font("mono", 34), LAV)
    # icon tile
    card(d, (90, 330, 330, 570), 50, fill=(30, 30, 90), outline=VIO, w=4)
    ICONS[key](d, 210, 450, 70)
    tsize = {"play": 210, "mono": 190}.get(tf, 200)
    left(d, 90, 600, title, font(tf, tsize), CRE)
    left(d, 90, 850, "QUÉ ES", font("mono", 30), LAV)
    left(d, 90, 900, what, font("inter", 50), CRE, spacing=14)
    card(d, (90, 1130, 990, 1600), 44)
    left(d, 140, 1170, "QUÉ GANA TU NEGOCIO", font("mono", 30), LAV)
    y = 1240
    for g in gains:
        d.ellipse((140, y + 8, 180, y + 48), fill=LIM)
        d.line((150, y + 28, 158, y + 37, 172, y + 19), fill=BG, width=6)
        d.text((210, y), g, font=font("inter-bold", 44), fill=CRE); y += 110
    sign(d, "tr")
    return im

# ---------------- 07-08 compartir reel ----------------
def hreel(title_top, title_main, tag, fnt, accent_lines, glow):
    im = base(glow); d = ImageDraw.Draw(im)
    pill(d, 0, 230, tag, font("mono", 30), fill=CARD, col=LAV, center_x=True)
    y = center(d, 310, title_main, fnt, CRE, spacing=0)
    # reel hole 9:16 area
    hw, hh = 520, 924; x0 = (W - hw) // 2; y0 = 620
    d.rounded_rectangle((x0 - 14, y0 - 14, x0 + hw + 14, y0 + hh + 14), 54, outline=VIO, width=6)
    d.rounded_rectangle((x0, y0, x0 + hw, y0 + hh), 44, fill=(14, 17, 42))
    center(d, y0 + hh // 2 - 30, "pega el reel aquí", font("inter", 34), (70, 76, 130))
    for (txt, side, yy) in accent_lines:
        f = font("inter-black", 40); tw = d.textlength(txt, font=f)
        xx = 40 if side == "l" else W - 40 - tw - 50
        d.rounded_rectangle((xx, yy, xx + tw + 50, yy + 80), 40, fill=LIM if side == "r" else LAV)
        d.text((xx + 25, yy + 16), txt, font=f, fill=BG)
    center(d, y0 + hh + 40, title_top, font("inter-bold", 42), LAV)
    sign(d, "tl")
    return im

def h07():
    return hreel("Chicho Cars · mira el cambio", "¿Antes o\ndespués?", "CASO REAL", font("inter-black", 120),
                 [("ANTES", "l", 760), ("DESPUÉS", "r", 1300)], (540, 1000))

def h08():
    return hreel("Nacusi Muebles · mismo producto", "Mismos muebles,\notro video", "CASO REAL", font("play", 108),
                 [("MISMOS", "l", 760), ("OTRO VIDEO", "r", 1260)], (540, 1100))

# ---------------- 09 encuesta ----------------
def h09():
    im = base((540, 1150)); d = ImageDraw.Draw(im)
    pill(d, 0, 250, "ENCUESTA · 10 SEGUNDOS", font("mono", 30), fill=CARD, col=LAV, center_x=True)
    center(d, 360, "¿Qué te\ncuesta más", font("heros", 140), CRE, spacing=0)
    center(d, 660, "de tus redes?", font("play", 110), LAV)
    # sticker zone
    d.rounded_rectangle((140, 900, 940, 1360), 50, outline=(70, 76, 150), width=4)
    center(d, 1110, "sticker de encuesta aquí", font("inter", 34), (70, 76, 130))
    f = font("inter-bold", 40)
    pill(d, 140, 1420, "Tener ideas", f, fill=VIO); w2 = d.textlength("Editar videos", font=f) + 60
    pill(d, 940 - w2, 1420, "Editar videos", f, fill=LAV, col=BG)
    center(d, 1540, "Vota y te contamos cómo lo resolvemos", font("inter", 36), CRE)
    sign(d, "tr")
    return im

# ---------------- 10 cierre ----------------
def h10():
    im = base((540, 900)); d = ImageDraw.Draw(im)
    left(d, 90, 250, "¿LO RESOLVEMOS?", font("mono", 34), LAV)
    y = left(d, 90, 320, "Escribe", font("inter-black", 150), CRE, spacing=0)
    d.rounded_rectangle((80, y + 10, 720, y + 210), 40, fill=VIO)
    d.text((115, y + 10), "TRIPI", font=font("inter-black", 190), fill=CRE)
    y = left(d, 90, y + 250, "y te decimos cómo\nresolverlo.", font("inter-bold", 64), CRE, spacing=8)
    card(d, (90, 1010, 990, 1200), 40)
    d.text((140, 1040), "Propuesta gratis", font=font("inter-bold", 52), fill=CRE)
    d.text((140, 1110), "en", font=font("inter-bold", 52), fill=CRE)
    d.text((220, 1095), "24 h", font=font("inter-black", 76), fill=LIM)
    d.rounded_rectangle((140, 1250, 940, 1500), 50, outline=(70, 76, 150), width=4)
    center(d, 1350, "sticker de respuesta aquí", font("inter", 34), (70, 76, 130))
    center(d, 1545, "Somos dos personas reales.", font("inter", 34), LAV)
    sign(d, "tr")
    return im

# ---------------- destacadas ----------------
def cover(icon_fn, label):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.ellipse((240, 660, 840, 1260), fill=VIO)
    icon_fn(d, 540, 960, 170)
    star(d, 800, 700, 50, LAV)
    return im

def ic_grid(d, cx, cy, s, col=CRE):
    for i, c in enumerate([CRE, LAV, LIM, CRE]):
        x = cx - s * .75 + (i % 2) * s * .85; y = cy - s * .75 + (i // 2) * s * .85
        d.rounded_rectangle((x, y, x + s * .65, y + s * .65), s * .15, fill=c)

if __name__ == "__main__":
    out = [h01()] + [hserv(i) for i in range(5)] + [h07(), h08(), h09(), h10()]
    for n, im in enumerate(out, 1): im.save(os.path.join(OUT, f"historia-{n:02d}.png"))
    cover(ic_grid, "SERVICIOS").save(os.path.join(OUT, "destacada-servicios.png"))
    cover(ic_beforeafter, "ANTES/DESPUÉS").save(os.path.join(OUT, "destacada-antes-despues.png"))
    print("ok")
