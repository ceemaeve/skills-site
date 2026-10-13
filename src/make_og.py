# Draws og.png (social preview card) in the ceema.dev look shared by every ceema.dev site.
# Fonts: Orbitron, Rajdhani and Share Tech Mono (Google Fonts, SIL Open Font License, see fonts/OFL-*.txt).
# The counts on the bottom line come from data.json, so after adding a sprint, track or cert:
#   python3 make_og.py      (needs Pillow), then commit src/og.png. The Actions build only copies it.
import os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.environ.get("FONTS", os.path.join(HERE, "fonts"))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "og.png")
W, H = 1200, 630
void = (20, 12, 43); cyan = (52, 240, 192); magenta = (255, 79, 163)
dim = (170, 157, 210); mid = (231, 222, 252); white = (255, 255, 255); primary = (139, 92, 246)

def orbitron(size, weight=800):
    f = ImageFont.truetype(os.path.join(FONTS, "Orbitron[wght].ttf"), size)
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f
mono = lambda s: ImageFont.truetype(os.path.join(FONTS, "ShareTechMono-Regular.ttf"), s)
raj = lambda s: ImageFont.truetype(os.path.join(FONTS, "Rajdhani-Bold.ttf"), s)

im = Image.new("RGB", (W, H), void)
# background glows, as on the sites: purple top right, magenta left
g = Image.new("RGB", (W, H), void); gd = ImageDraw.Draw(g)
gd.ellipse((620, -380, 1500, 260), fill=(70, 40, 150))
gd.ellipse((-420, 140, 380, 720), fill=(80, 20, 70))
im = Image.blend(im, g.filter(ImageFilter.GaussianBlur(140)), 0.85)
d = ImageDraw.Draw(im, "RGBA")
for x in range(0, W, 24): d.line([(x, 0), (x, H)], fill=primary + (16,))
for y in range(0, H, 24): d.line([(0, y), (W, y)], fill=primary + (16,))

# ring-and-dot wordmark, with a soft glow
cx, cy, r = 118, 118, 30
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((cx-r, cy-r, cx+r, cy+r), outline=(167, 139, 250, 200), width=8)
glow = glow.filter(ImageFilter.GaussianBlur(9)); im.paste(glow, (0, 0), glow)
d = ImageDraw.Draw(im, "RGBA")
d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=cyan, width=7)
d.ellipse((cx-9, cy-9, cx+9, cy+9), fill=magenta)
d.text((172, cy), "CEEMA", font=orbitron(30), fill=white, anchor="lm")
w = d.textlength("CEEMA", font=orbitron(30))
d.text((172 + w, cy), ".DEV", font=orbitron(30), fill=magenta, anchor="lm")

# eyebrow
ey = 236
d.ellipse((90, ey-7, 104, ey+7), fill=magenta)
d.ellipse((85, ey-12, 109, ey+12), outline=magenta + (70,), width=3)
d.text((124, ey), "SKILLS FIRST, CERTS OPTIONAL", font=mono(28), fill=cyan, anchor="lm")

# title, with the glow the sites put on h1
title = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(title)
td.text((86, 355), "SKILL TRAINING", font=orbitron(84), fill=(167, 139, 250, 150), anchor="ls")
td.text((86, 455), "COMPLETED", font=orbitron(84), fill=(255, 79, 163, 150), anchor="ls")
title = title.filter(ImageFilter.GaussianBlur(14)); im.paste(title, (0, 0), title)
d = ImageDraw.Draw(im, "RGBA")
d.text((86, 355), "SKILL TRAINING", font=orbitron(84), fill=white, anchor="ls")
d.text((86, 455), "COMPLETED", font=orbitron(84), fill=magenta, anchor="ls")

# footer strip
d.line([(90, 520), (1110, 520)], fill=primary + (110,), width=2)
data = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))
n = lambda k, one, many: f"{len(data[k])} {one if len(data[k]) == 1 else many}"
counts = "  ·  ".join([n("sprints", "sprint", "sprints"), n("tracks", "track", "tracks"), n("certs", "certification", "certifications")])
d.text((90, 572), counts, font=raj(32), fill=mid, anchor="ls")
d.text((1110, 572), "skills.ceema.dev", font=mono(28), fill=white, anchor="rs")
im.save(OUT, optimize=True)
print("wrote", OUT)
