#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import sys

W, H = 2480, 3508  # A4 @300dpi
ROSE = (183, 126, 142)
GREY = (90, 92, 88)
GREEN = (108, 118, 96)
LINE = (183, 160, 150)

FONT = "fonts/Assistant.ttf"

def f(size, weight=400):
    ft = ImageFont.truetype(FONT, size)
    try:
        ft.set_variation_by_axes([weight])
    except Exception:
        pass
    return ft

bg = Image.open("out/bg1.png").convert("RGB").resize((W, H), Image.LANCZOS)
d = ImageDraw.Draw(bg)

def center(txt, y, font, fill, spacing=0):
    if spacing:
        # manual letter spacing, RTL: draw per char right-to-left
        chars = list(txt)
        widths = [d.textlength(c, font=font, direction="rtl") for c in chars]
        total = sum(widths) + spacing * (len(chars) - 1)
        x = W / 2 + total / 2
        for c, wd in zip(chars, widths):
            x -= wd
            d.text((x, y), c, font=font, fill=fill, direction="rtl", anchor="la")
            x -= spacing
        return
    d.text((W / 2, y), txt, font=font, fill=fill, direction="rtl", anchor="ma")

# 1 intro
center("אנחנו נרגשים להזמינכם לחגוג את החתונה של", 300, f(74, 300), GREY)

# 2 names
center("מיכל ואופיר", 430, f(215, 350), ROSE)

# 3 line drawing
art = Image.open("out/line_trim.png").convert("RGB")
ar = art.width / art.height
ah = 1330
aw = int(ah * ar)
art = art.resize((aw, ah), Image.LANCZOS)
# multiply onto paper so white stays paper-coloured
box = (W // 2 - aw // 2, 760)
region = bg.crop((box[0], box[1], box[0] + aw, box[1] + ah))
from PIL import ImageChops
bg.paste(ImageChops.multiply(region, art), box)

# 4 date
center("03.11.2026", 2160, f(175, 350), ROSE)

# 5 day / venue
center("יום שלישי", 2395, f(70, 300), GREY)
center("ביער, חדרה", 2520, f(78, 300), GREY)

# 6 three time columns (RTL: rightmost = first)
cols = [("נפגשים", "19:30"), ("מתחתנים", "__:__"), ("חוגגים", "עד 02:00")]
ytop, ylab, ytime = 2740, 2755, 2880
xs = [W / 2 + 620, W / 2, W / 2 - 620]
flab, ftime = f(66, 300), f(76, 350)
for (lab, tm), x in zip(cols, xs):
    d.text((x, ylab), lab, font=flab, fill=GREEN, direction="rtl", anchor="ma")
    d.text((x, ytime), tm, font=ftime, fill=GREY, direction="rtl", anchor="ma")
for x in (W / 2 + 310, W / 2 - 310):
    d.line([(x, ytop), (x, ytop + 300)], fill=LINE, width=3)

# 7 parents
fp = f(62, 300)
d.text((W - 330, 3110), "הורי החתן:", font=fp, fill=GREY, direction="rtl", anchor="ra")
d.text((W - 330, 3210), "______ ו______", font=fp, fill=GREY, direction="rtl", anchor="ra")
d.text((330, 3110), "הורי הכלה:", font=fp, fill=GREY, direction="rtl", anchor="la")
d.text((330, 3210), "______ ו______", font=fp, fill=GREY, direction="rtl", anchor="la")

bg.save("out/invitation.png")
bg.resize((W // 3, H // 3), Image.LANCZOS).save("out/invitation_preview.jpg", quality=90)
print("ok")
