#!/usr/bin/env python3
"""A4 invitation variations built on the APPROVED wedding-brand mark."""
from PIL import Image, ImageDraw, ImageFont, ImageChops
import random

W, H = 2480, 3508
CREAM = (251, 248, 243)
INK = (35, 39, 38)
SOFT = (122, 116, 108)
RULE = (60, 58, 54)

FRL = "fonts/FrankRuhlLibre.ttf"
CG = "fonts/CormorantGaramond.ttf"
ASS = "fonts/Assistant.ttf"

def f(path, size, w=None):
    ft = ImageFont.truetype(path, size)
    if w:
        try: ft.set_variation_by_axes([w])
        except Exception: pass
    return ft

PLANTS = Image.open("out/mark_plants.png").convert("RGB")
ROOTS = Image.open("out/mark_roots.png").convert("RGB")

def paper():
    img = Image.new("RGB", (W, H), CREAM)
    random.seed(7); px = img.load()
    for _ in range(90000):
        x, y = random.randrange(W), random.randrange(H)
        r, g, b = px[x, y]; k = random.randint(-3, 3)
        px[x, y] = (r+k, g+k, b+k)
    return img

def place(img, art, cx, top, width, fade=None):
    """multiply-composite art (white bg) onto paper; fade = alpha 0..1"""
    h = int(art.height * width / art.width)
    a = art.resize((width, h), Image.LANCZOS)
    box = (cx - width//2, top)
    reg = img.crop((box[0], box[1], box[0]+width, box[1]+h))
    m = ImageChops.multiply(reg, a)
    if fade is not None:
        m = Image.blend(reg, m, fade)
    img.paste(m, box)
    return h

def taper_rule(d, y, cx, half, weight=5, col=RULE):
    """horizontal rule at full weight in the centre, tapering to nothing at both ends"""
    steps = 260
    for i in range(steps):
        t = i / (steps - 1)
        x0 = cx - half + (2*half) * t
        # weight profile: full in middle, 0 at ends
        k = (1 - abs(t - .5) * 2) ** .55
        wgt = weight * k
        if wgt < .4: continue
        d.line([(x0, y), (x0 + (2*half/steps) + 1, y)], fill=col, width=max(1, int(round(wgt))))

def times_block(d, y, rows, fl, ft_, gap=118, xlab=None, xval=None):
    for lab, tm in rows:
        d.text((xlab, y), lab, font=fl, fill=SOFT, direction="rtl", anchor="ra")
        d.text((xval, y), tm, font=ft_, fill=INK, direction="rtl", anchor="la")
        y += gap
    return y

TIMES = [("קבלת פנים", "19:00"), ("חופה", "20:30"), ("ארוחת ערב", "21:15"),
         ("ריקודים", "22:00"), ("מתוקים", "22:30"), ("מעגל סיום", "02:00")]

# ══════════════════ V1 — waterline as the organising line ══════════════════
img = paper(); d = ImageDraw.Draw(img)
ph = place(img, PLANTS, W//2, 300, 1180)
wl = 300 + ph + 20
taper_rule(d, wl, W//2, 1020, 6)
# names sit ON the line, letterspaced, either side of the stems
fn = f(CG, 108, 500)
def sp_text(d, txt, x, y, font, fill, sp, anchor="la"):
    tot = sum(d.textlength(c, font=font) for c in txt) + sp*(len(txt)-1)
    if anchor == "ra": x -= tot
    for c in txt:
        d.text((x, y), c, font=font, fill=fill, anchor="ls")
        x += d.textlength(c, font=font) + sp
sp_text(d, "MICHAL", W//2 - 230, wl - 34, fn, INK, 22, "ra")
sp_text(d, "OPHIR", W//2 + 230, wl - 34, fn, INK, 22)
place(img, ROOTS, W//2, wl + 14, 900, fade=.95)
y = 2130
d.text((W/2, y), "3 . 11 . 26", font=f(CG, 150, 400), fill=INK, direction="ltr", anchor="ma")
d.text((W/2, y+230), "כ״ג בחשון תשפ״ז", font=f(FRL, 62, 400), fill=SOFT, direction="rtl", anchor="ma")
d.text((W/2, y+340), "״ביער״ · חדרה", font=f(FRL, 78, 400), fill=INK, direction="rtl", anchor="ma")
times_block(d, y+540, TIMES[:3] , f(FRL, 58, 400), f(CG, 62, 400), xlab=W/2+300, xval=W/2-300)
d.text((W/2, 3210), "רונן ונירית פלד־חדד   ·   רודי וחגית חרותקה", font=f(FRL, 48, 400), fill=SOFT, direction="rtl", anchor="ma")
img.save("out/V1_waterline.png"); img.resize((W//4, H//4), Image.LANCZOS).save("out/V1_p.jpg", quality=92)

# ══════════════════ V2 — herbarium sheet ══════════════════
img = paper(); d = ImageDraw.Draw(img)
# specimen mounted off-centre, sheet mostly empty
ph = place(img, PLANTS, int(W*0.44), 420, 1080)
wl = 420 + ph + 18
taper_rule(d, wl, int(W*0.44), 760, 5)
place(img, ROOTS, int(W*0.44), wl + 12, 820, fade=.95)
# thin rule box for the corner label
lx, ly, lw, lh = W-1180, H-980, 900, 560
d.rectangle([lx, ly, lx+lw, ly+lh], outline=(150,144,134), width=3)
fl = f(CG, 44, 400); fv = f(CG, 50, 500); fh = f(FRL, 40, 400)
d.text((lx+40, ly-30), "HERBARIUM  ·  GRUTEKE / PELED-HADAD", font=f(CG,40,500), fill=SOFT, anchor="ls")
rows = [("Taxon", "Epipremnum aureum ×"),
        ("", "Monstera deliciosa"),
        ("Locality", "״ביער״, Hadera, IL"),
        ("Collected", "3 . 11 . 2026"),
        ("Heb. date", "כ״ג בחשון תשפ״ז"),
        ("Collectors", "Michal & Ophir"),
        ("Accession", "No. 03112026")]
yy = ly + 56
for k, v in rows:
    if k: d.text((lx+40, yy), k, font=fl, fill=SOFT, direction="ltr", anchor="la")
    heb = any("\u0590" <= c <= "\u05ff" for c in v)
    d.text((lx+lw-40, yy), v, font=(f(FRL, 46, 500) if heb else fv), fill=INK,
           direction=("rtl" if heb else "ltr"), anchor="ra")
    yy += 62
d.text((int(W*0.44), 300), "MICHAL   ×   OPHIR", font=f(CG, 86, 500), fill=INK, anchor="ma")
img.save("out/V2_herbarium.png"); img.resize((W//4, H//4), Image.LANCZOS).save("out/V2_p.jpg", quality=92)

# ══════════════════ V3 — nursery care tag ══════════════════
img = paper(); d = ImageDraw.Draw(img)
ph = place(img, PLANTS, W//2, 360, 1000)
wl = 360 + ph + 16
taper_rule(d, wl, W//2, 880, 5)
place(img, ROOTS, W//2, wl+12, 760, fade=.95)
yy = wl + 560
d.text((W/2+40, yy), "MICHAL × OPHIR", font=f(CG, 92, 500), fill=INK, direction="ltr", anchor="ra")
d.text((W/2+80, yy+6), "’חדרה‘", font=f(FRL, 80, 500), fill=INK, direction="rtl", anchor="la")
yy += 190
d.line([(W/2-760, yy), (W/2+760, yy)], fill=(180,174,164), width=2)
care = [("אור", "עקיף, בשפע"),
        ("השקיה", "כשהאדמה יבשה"),
        ("עמידות", "אזור 10 — חם, יבש, ביחד"),
        ("פריחה", "3.11.2026, 19:00"),
        ("גובה בבגרות", "בלתי ידוע")]
yy += 70
flab = f(FRL, 56, 400); fval = f(FRL, 60, 500)
for k, v in care:
    d.text((W/2+720, yy), k, font=flab, fill=SOFT, direction="rtl", anchor="ra")
    d.text((W/2-720, yy), v, font=fval, fill=INK, direction="rtl", anchor="la")
    yy += 108
d.line([(W/2-760, yy+20), (W/2+760, yy+20)], fill=(180,174,164), width=2)
d.text((W/2, yy+90), "״ביער״ · חדרה   ·   חופה 20:30", font=f(FRL, 56, 400), fill=INK, direction="rtl", anchor="ma")
d.text((W/2, 3300), "רונן ונירית פלד־חדד   ·   רודי וחגית חרותקה", font=f(FRL, 46, 400), fill=SOFT, direction="rtl", anchor="ma")
img.save("out/V3_caretag.png"); img.resize((W//4, H//4), Image.LANCZOS).save("out/V3_p.jpg", quality=92)

# ══════════════════ V4 — vellum overlay simulation (two sheets) ══════════════════
img = paper(); d = ImageDraw.Draw(img)
ph = place(img, PLANTS, W//2, 560, 1150)
wl = 560 + ph + 20
taper_rule(d, wl, W//2, 980, 6)
sp_text(d, "MICHAL", W//2 - 220, wl - 32, f(CG, 100, 500), INK, 20, "ra")
sp_text(d, "OPHIR", W//2 + 220, wl - 32, f(CG, 100, 500), INK, 20)
# vellum sheet: lighter, slightly cooler, with a visible edge and shadow
vel_top = wl - 40
vel = img.crop((0, vel_top, W, H)).copy()
vel = Image.blend(vel, Image.new("RGB", vel.size, (255, 255, 253)), .55)
img.paste(vel, (0, vel_top))
d.line([(0, vel_top), (W, vel_top)], fill=(214, 208, 198), width=4)
d.line([(0, vel_top+7), (W, vel_top+7)], fill=(235, 231, 223), width=5)
place(img, ROOTS, W//2, wl + 10, 940, fade=.72)
yy = 2500
d.text((W/2, yy), "3 . 11 . 26", font=f(CG, 132, 400), fill=(70,66,60), direction="ltr", anchor="ma")
d.text((W/2, yy+220), "״ביער״ · חדרה", font=f(FRL, 70, 400), fill=(70,66,60), direction="rtl", anchor="ma")
d.text((W/2, yy+340), "קבלת פנים 19:00 · חופה 20:30", font=f(FRL, 54, 400), fill=(110,104,96), direction="rtl", anchor="ma")
d.text((W/2, 3300), "רונן ונירית פלד־חדד   ·   רודי וחגית חרותקה", font=f(FRL, 46, 400), fill=(130,124,116), direction="rtl", anchor="ma")
img.save("out/V4_vellum.png"); img.resize((W//4, H//4), Image.LANCZOS).save("out/V4_p.jpg", quality=92)
print("ok")
