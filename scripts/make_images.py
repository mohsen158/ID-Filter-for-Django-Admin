import os, sys
from PIL import Image, ImageDraw, ImageFont

root = sys.argv[1]
os.makedirs(f"{root}/icons", exist_ok=True)
os.makedirs(f"{root}/store", exist_ok=True)

BG = (37, 99, 235)      # blue
FG = (255, 255, 255)
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size)


def icon(size):
    s = size * 4  # supersample for smooth edges
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=s // 5, fill=BG)
    f = font(BOLD, int(s * 0.5))
    d.text((s / 2, s / 2), "?id", font=f, fill=FG, anchor="mm")
    return img.resize((size, size), Image.LANCZOS)


for n in (16, 48, 128):
    icon(n).save(f"{root}/icons/icon{n}.png")

# 440x280 small promo tile
promo = Image.new("RGB", (440, 280), (248, 250, 252))
d = ImageDraw.Draw(promo)
promo.paste(icon(96), (40, 40), icon(96))
d.text((152, 62), "ID Filter", font=font(BOLD, 34), fill=(15, 23, 42))
d.text((152, 104), "for Django Admin", font=font(REG, 22), fill=(71, 85, 105))
mono = font("/System/Library/Fonts/Menlo.ttc", 15)
d.text((40, 176), "/admin/app/model/42/change/", font=mono, fill=(100, 116, 139))
d.text((40, 204), "→ /admin/app/model/?id=42", font=mono, fill=BG)
promo.save(f"{root}/store/promo-440x280.png")
print("ok")
