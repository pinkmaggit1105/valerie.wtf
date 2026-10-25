"""Draws Sudo's 32x32 pixel-art sprites.

Usage: python3 tools/make_sprites.py sprites [preview.png]
Needs Pillow. The optional second argument writes a zoomed-in sheet of every sprite.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
S = 32

PAL = {
    "outline": (26, 28, 44, 255),
    "body": (52, 58, 84, 255),
    "bodyhi": (78, 86, 120, 255),
    "white": (244, 244, 240, 255),
    "shade": (200, 210, 225, 255),
    "orange": (247, 150, 60, 255),
    "orangedk": (200, 100, 40, 255),
    "pink": (255, 140, 170, 255),
    "eye": (20, 20, 30, 255),
    "blue": (120, 200, 255, 255),
    "green": (130, 200, 80, 255),
    "greendk": (80, 140, 50, 255),
    "red": (235, 60, 80, 255),
    "fish": (110, 170, 230, 255),
    "fishdk": (60, 110, 180, 255),
    "yellow": (255, 220, 90, 255),
}


class Canvas:
    def __init__(self):
        self.px = {}

    def set(self, x, y, c):
        if 0 <= x < S and 0 <= y < S:
            self.px[(x, y)] = PAL[c] if isinstance(c, str) else c

    def get(self, x, y):
        return self.px.get((x, y))

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(S):
            for x in range(S):
                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                    self.set(x, y, c)

    def outline(self, c="outline"):
        filled = set(self.px)
        for (x, y) in list(filled):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n not in filled:
                    self.set(*n, c)

    def image(self, scale=1):
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        for (x, y), c in self.px.items():
            im.putpixel((x, y), c)
        if scale > 1:
            im = im.resize((S * scale, S * scale), Image.NEAREST)
        return im


def penguin(dy=0, squish=0, fat=0):
    """Base penguin body. dy shifts the body down (bob); feet stay put."""
    c = Canvas()
    cy = 17 + dy
    # flippers
    c.ellipse(5.0 - fat, cy + 3, 2.6, 5, "body")
    c.ellipse(27.0 + fat, cy + 3, 2.6, 5, "body")
    # body
    c.ellipse(16, cy, 10.5 + fat, 12 - squish, "body")
    # back highlight
    c.ellipse(11, cy - 7, 3, 2, "bodyhi")
    # face mask + belly
    c.ellipse(12.5, cy - 4, 4.6, 4.2, "white")
    c.ellipse(19.5, cy - 4, 4.6, 4.2, "white")
    c.ellipse(16, cy + 4, 7.5 + fat, 7.5 - squish, "white")
    c.ellipse(16, cy + 9, 6 + fat, 2.5, "shade")
    # feet (fixed to floor)
    for x in range(10, 15):
        c.set(x, 29, "orange")
        c.set(x, 30, "orangedk")
    for x in range(17, 22):
        c.set(x, 29, "orange")
        c.set(x, 30, "orangedk")
    c.outline()
    return c, cy


def beak(c, cy, open_=False):
    by = cy - 1
    for x in (15, 16):
        c.set(x, by, "orange")
    for x in (14, 15, 16, 17):
        c.set(x, by + 1, "orange")
    if open_:
        for x in (15, 16):
            c.set(x, by + 2, "red")
        for x in (14, 15, 16, 17):
            c.set(x, by + 3, "orangedk")
    else:
        for x in (15, 16):
            c.set(x, by + 2, "orangedk")


def blush(c, cy):
    for x in (9, 10):
        c.set(x, cy - 1, "pink")
    for x in (21, 22):
        c.set(x, cy - 1, "pink")


def eyes(c, cy, kind):
    ey = cy - 5
    L, R = 12, 19
    if kind == "open":
        for ex in (L, R):
            for x in (ex, ex + 1):
                for y in (ey, ey + 1, ey + 2):
                    c.set(x, y, "eye")
            c.set(ex + 1, ey, "white")
    elif kind == "big":
        for ex in (L, R):
            for x in (ex - 1, ex, ex + 1, ex + 2):
                for y in (ey - 1, ey, ey + 1, ey + 2):
                    c.set(x, y, "eye")
            c.set(ex + 1, ey - 1, "white")
            c.set(ex + 2, ey, "white")
            c.set(ex - 1, ey + 2, "white")
    elif kind == "happy":  # ^ ^
        for ex in (L, R):
            c.set(ex - 1, ey + 2, "eye")
            c.set(ex, ey + 1, "eye")
            c.set(ex + 1, ey + 1, "eye")
            c.set(ex + 2, ey + 2, "eye")
    elif kind == "closed":  # - -
        for ex in (L, R):
            for x in (ex - 1, ex, ex + 1, ex + 2):
                c.set(x, ey + 2, "eye")
    elif kind == "sad":
        for ex in (L, R):
            for x in (ex, ex + 1):
                for y in (ey + 1, ey + 2):
                    c.set(x, y, "eye")
        # droopy brows
        c.set(L - 1, ey - 1, "eye"); c.set(L, ey - 1, "eye"); c.set(L + 1, ey - 2, "eye")
        c.set(R, ey - 2, "eye"); c.set(R + 1, ey - 1, "eye"); c.set(R + 2, ey - 1, "eye")
    elif kind == "sleepy":
        for ex in (L, R):
            for x in (ex - 1, ex, ex + 1, ex + 2):
                c.set(x, ey + 1, "eye")
            c.set(ex, ey + 2, "eye")
            c.set(ex + 1, ey + 2, "eye")
    elif kind == "dizzy":  # x x
        for ex in (L, R):
            for i in range(3):
                c.set(ex - 1 + i, ey + i, "eye")
                c.set(ex + 1 - i, ey + i, "eye")


def save(c, name):
    c.image().save(os.path.join(OUT, f"{name}.png"))
    return name


def mood(name, eye_kind, extras=None, frames=2, mouth_open=False, cheeks=True, fat=0):
    names = []
    for f in range(frames):
        c, cy = penguin(dy=f, squish=f * 0.5, fat=fat)
        eyes(c, cy, eye_kind)
        beak(c, cy, open_=mouth_open)
        if cheeks:
            blush(c, cy)
        if extras:
            extras(c, cy, f)
        names.append(save(c, f"{name}_{f + 1}"))
    return names


# ---------- extras ----------
def drool(c, cy, f):
    c.set(17, cy + 2, "blue")
    c.set(17, cy + 3, "blue")
    if f:
        c.set(17, cy + 4, "blue")


def tear(c, cy, f):
    c.set(11, cy - 2 + f, "blue")
    c.set(11, cy - 1 + f, "blue")
    c.set(20, cy - 2 + f, "blue")


def stink(c, cy, f):
    for i, x in enumerate((3, 7, 26, 29)):
        off = (f + i) % 2
        for y in range(4, 9):
            c.set(x + ((y + off) % 2), y + (i % 2) * 2, "green")
    # fly
    fx, fy = (24, 3) if f == 0 else (22, 2)
    c.set(fx, fy, "outline"); c.set(fx - 1, fy - 1, "shade"); c.set(fx + 1, fy - 1, "shade")


def sweat(c, cy, f):
    c.set(25, cy - 8 + f, "blue")
    c.set(25, cy - 7 + f, "blue")
    c.set(24, cy - 7 + f, "blue")


def sparkles(c, cy, f):
    pts = [(3, 4), (28, 6), (2, 14)] if f == 0 else [(29, 3), (4, 8), (29, 14)]
    for (x, y) in pts:
        c.set(x, y, "yellow")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.set(x + dx, y + dy, "yellow")


def thermometer(c, cy, f):
    # green-tinted face
    for (x, y), col in list(c.px.items()):
        if col == PAL["white"] and y < cy:
            c.set(x, y, (205, 230, 180, 255))
    for i in range(6):
        c.set(17 + i, cy + 1 + i // 2, "outline")
        c.set(17 + i, cy + 2 + i // 2, "shade")
    c.set(23, cy + 3, "red"); c.set(23, cy + 4, "red"); c.set(24, cy + 4, "red")


def z_px(c, x, y, n):
    for i in range(n):
        c.set(x + i, y, "blue")
        c.set(x + i, y + n - 1, "blue")
        c.set(x + n - 1 - i, y + i, "blue")


def zzz(c, cy, f):
    z_px(c, 23, 6 - f, 3)
    z_px(c, 26, 1 + f, 4)


def heart_px(c, x, y, col="red"):
    for dx, dy in ((0, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1),
                   (0, 2), (1, 2), (2, 2), (1, 3)):
        c.set(x + dx, y + dy, col)


def hearts(c, cy, f):
    heart_px(c, 24, 4 - f)
    if f:
        heart_px(c, 3, 6)


def fish_px(c, x, y):
    for dx in range(5):
        c.set(x + dx, y, "fish")
        c.set(x + dx, y + 1, "fishdk" if dx > 2 else "fish")
    c.set(x + 1, y - 1, "fish"); c.set(x + 2, y - 1, "fish")
    c.set(x + 5, y - 1, "fishdk"); c.set(x + 5, y + 2, "fishdk"); c.set(x + 5, y, "fishdk"); c.set(x + 5, y + 1, "fishdk")
    c.set(x + 1, y, "eye")


made = []
made += mood("idle_happy", "happy")
made += mood("idle_neutral", "open", cheeks=False)
made += mood("idle_hungry", "big", drool)
made += mood("idle_sad", "sad", tear, cheeks=False)
made += mood("idle_stinky", "sleepy", stink, cheeks=False)
made += mood("idle_sleepy", "sleepy", zzz, cheeks=False)
made += mood("idle_sick", "dizzy", thermometer, cheeks=False)
made += mood("idle_overfed", "closed", sweat, fat=2)
made += mood("idle_ecstatic", "happy", sparkles, mouth_open=True)
made += mood("blink", "closed", frames=1, cheeks=False)
made += mood("pet", "happy", hearts)

# eat: fish approaches, chomp, swallow
for f in range(3):
    c, cy = penguin(dy=1 if f == 1 else 0)
    eyes(c, cy, "big" if f == 0 else "closed" if f == 1 else "happy")
    beak(c, cy, open_=(f == 0))
    blush(c, cy)
    if f == 0:
        fish_px(c, 22, cy + 2)
    elif f == 1:
        # tail sticking out
        c.set(18, cy + 1, "fishdk"); c.set(19, cy, "fishdk"); c.set(19, cy + 2, "fishdk")
    made.append(save(c, f"eat_{f + 1}"))

# bath: bubbles all around, blissed out
def bubbles(c, cy, f):
    pts = [(4, 22), (7, 17), (25, 20), (28, 15), (3, 11), (27, 9)]
    for i, (x, y) in enumerate(pts):
        y -= f * (1 + i % 2)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            c.set(x + dx, y + dy, "blue")
        c.set(x, y, "white")
    for x in range(6, 26):
        c.set(x, 27 + (x + f) % 2, "blue")


made += mood("bath", "happy", bubbles)


def ball(c, cy, f):
    bx, by = (24, 2) if f == 0 else (25, 8)
    for y in range(by, by + 4):
        for x in range(bx, bx + 4):
            if (x - bx - 1.5) ** 2 + (y - by - 1.5) ** 2 <= 4:
                c.set(x, y, "green" if (x + y) % 3 else "yellow")


made += mood("play", "happy", ball, mouth_open=True)
made += mood("sleep", "closed", zzz, cheeks=False)

# props: 16x16 items you drag onto Sudo, plus particles
def prop(name, draw, outline=True):
    c = Canvas()
    draw(c)
    if outline:
        c.outline()
    c.image().crop((0, 0, 16, 16)).save(os.path.join(OUT, f"{name}.png"))
    made.append(name)


def soap(c):
    for y in range(8, 13):
        for x in range(2, 13):
            c.set(x, y, "pink" if y > 8 else "white")
    for x, y in ((4, 5), (8, 3), (11, 6)):
        c.set(x, y, "blue")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.set(x + dx, y + dy, "blue")
        c.set(x, y, "white")


def ball_prop(c):
    for y in range(3, 13):
        for x in range(3, 13):
            if (x - 7.5) ** 2 + (y - 7.5) ** 2 <= 21:
                c.set(x, y, "green")
    for x in range(3, 13):
        c.set(x, 7 + (1 if 5 < x < 10 else 0), "yellow")
    c.set(5, 5, "white")


def pill(c):
    for y in range(5, 11):
        for x in range(2, 14):
            if (x < 5 or x > 10) and ((x - (4.5 if x < 8 else 10.5)) ** 2 + (y - 7.5) ** 2 > 9):
                continue
            c.set(x, y, "red" if x < 8 else "white")
    c.set(4, 6, "white")


def moon(c):
    for y in range(2, 14):
        for x in range(2, 14):
            if (x - 7.5) ** 2 + (y - 7.5) ** 2 <= 30 and (x - 10) ** 2 + (y - 5.5) ** 2 > 18:
                c.set(x, y, "yellow")


def bubble(c):
    for y in range(4, 12):
        for x in range(4, 12):
            d = (x - 7.5) ** 2 + (y - 7.5) ** 2
            if 9 <= d <= 16:
                c.set(x, y, "blue")
    c.set(6, 6, "white"); c.set(6, 7, "white")


def sparkle(c):
    for i in range(-3, 4):
        c.set(8 + i, 8, "yellow")
        c.set(8, 8 + i, "yellow")
    c.set(8, 8, "white")


def big_fish(c):
    c.ellipse(7, 8, 5.5, 3.6, "fish")
    for x in range(2, 12):
        for y in range(9, 12):
            if c.get(x, y):
                c.set(x, y, "fishdk")
    for i in range(4):
        for y in range(8 - i - 1, 8 + i + 1):
            c.set(11 + i, y, "fishdk")
    c.set(4, 7, "eye")
    c.set(6, 5, "white")


prop("fish", big_fish)
prop("heart", lambda c: heart_px(c, 6, 6))
prop("soap", soap)
prop("ball", ball_prop)
prop("pill", pill)
prop("moon", moon)
prop("bubble", bubble, outline=False)
prop("sparkle", sparkle, outline=False)

# ---------- preview sheet ----------
if len(sys.argv) < 3:
    print(len(made), "sprites")
    sys.exit()
SC = 6
cols = 6
cell = S * SC + 16
rows = (len(made) + cols - 1) // cols
sheet = Image.new("RGBA", (cols * cell, rows * (cell + 18)), (18, 20, 28, 255))
d = ImageDraw.Draw(sheet)
for i, n in enumerate(made):
    im = Image.open(os.path.join(OUT, f"{n}.png"))
    im = im.resize((im.width * SC, im.height * SC), Image.NEAREST)
    x = (i % cols) * cell + 8
    y = (i // cols) * (cell + 18) + 8
    d.rectangle([x - 2, y - 2, x + S * SC + 1, y + S * SC + 1], fill=(34, 38, 52, 255))
    sheet.alpha_composite(im, (x, y))
    d.text((x, y + S * SC + 4), n, fill=(140, 255, 160, 255))
if len(sys.argv) > 2:
    sheet.save(sys.argv[2])
print(len(made), "sprites")
