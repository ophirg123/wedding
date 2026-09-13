#!/usr/bin/env python3
"""Modern comps — Jacquemus/Prada register: type-led, no decoration."""
from PIL import Image, ImageDraw, ImageFont, ImageChops
import sys

W, H = 2480, 3508
PAPER = (247, 245, 240)
INK = (26, 26, 26)
SOFT = (120, 120, 118)

def f(path, size, weight=None):
    ft = ImageFont.truetype(path, size)
    if weight:
        try: ft.set_variation_by_axes([weight])
        except Exception: pass
    return ft

RUBIK = "fonts/Rubik.ttf"
ASSIST = "fonts/Assistant.ttf"

def track(d, txt, y, font, fill, sp, W=W):
    chars = list(txt)
    ws = [d.textlength(c, font=font, direction="rtl") for c in chars]
    total = sum(ws) + sp * (len(chars) - 1)
    x = W / 2 + total / 2
    for c, w in zip(chars, ws):
        x -= w
        d.text((x, y), c, font=font, fill=fill, direction="rtl", anchor="la")
        x -= sp

def base():
    img = Image.new("RGB", (W, H), PAPER)
    # subtle paper grain
    import random
    random.seed(4)
    px = img.load()
    for i in range(60000):
        x, y = random.randrange(W), random.randrange(H)
        r, g, b = px[x, y]
        k = random.randint(-4, 4)
        px[x, y] = (max(0,min(255,r+k)), max(0,min(255,g+k)), max(0,min(255,b+k)))
    return img

# ---------------- M1 : pure type, Jacquemus ----------------
img = base(); d = ImageDraw.Draw(img)
track(d, "מיכל ואופיר", 1180, f(RUBIK, 330, 600), INK, 6)
d.line([(W/2-520, 1700), (W/2+520, 1700)], fill=INK, width=4)
fs = f(ASSIST, 74, 400)
d.text((W/2, 1790), "03.11.2026", font=f(RUBIK, 90, 400), fill=INK, direction="rtl", anchor="ma")
d.text((W/2, 1940), "יום שלישי  ·  ביער, חדרה", font=fs, fill=SOFT, direction="rtl", anchor="ma")
fl = f(ASSIST, 58, 400)
rows = [("קבלת פנים", "19:30"), ("חופה", "__:__"), ("עד", "02:00")]
y = 2700
for lab, tm in rows:
    d.text((W/2+380, y), lab, font=fl, fill=SOFT, direction="rtl", anchor="ra")
    d.text((W/2-380, y), tm, font=fl, fill=INK, direction="rtl", anchor="la")
    y += 110
d.text((W/2, 3180), "______ ו______   ·   ______ ו______", font=f(ASSIST, 46, 400), fill=SOFT, direction="rtl", anchor="ma")
img.save("out/modern_M1.png")
img.resize((W//3, H//3), Image.LANCZOS).save("out/modern_M1_p.jpg", quality=90)

# ---------------- M2 : big type + line drawing as a mark ----------------
img = base(); d = ImageDraw.Draw(img)
art = Image.open("out/line_trim.png").convert("RGB")
ah = 1150; aw = int(ah * art.width / art.height)
art = art.resize((aw, ah), Image.LANCZOS)
box = (W//2 - aw//2, 640)
reg = img.crop((box[0], box[1], box[0]+aw, box[1]+ah))
img.paste(ImageChops.multiply(reg, art), box)
track(d, "מיכל ואופיר", 1960, f(RUBIK, 250, 600), INK, 4)
d.text((W/2, 2330), "03.11.2026", font=f(RUBIK, 78, 400), fill=SOFT, direction="rtl", anchor="ma")
d.line([(W/2-420, 2500), (W/2+420, 2500)], fill=(200,198,192), width=3)
d.text((W/2, 2570), "יום שלישי  ·  ביער, חדרה", font=f(ASSIST, 66, 400), fill=SOFT, direction="rtl", anchor="ma")
y = 2820
for lab, tm in rows:
    d.text((W/2+340, y), lab, font=f(ASSIST, 54, 400), fill=SOFT, direction="rtl", anchor="ra")
    d.text((W/2-340, y), tm, font=f(ASSIST, 54, 400), fill=INK, direction="rtl", anchor="la")
    y += 100
d.text((W/2, 3220), "______ ו______   ·   ______ ו______", font=f(ASSIST, 44, 400), fill=SOFT, direction="rtl", anchor="ma")
img.save("out/modern_M2.png")
img.resize((W//3, H//3), Image.LANCZOS).save("out/modern_M2_p.jpg", quality=90)
print("ok")
