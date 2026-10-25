"""Draws Sudo's 32x32 pixel-art sprites, for both baby and grown-up Sudo.

Usage: python3 tools/make_sprites.py sprites [preview.png]
Needs Pillow. The optional second argument writes a zoomed-in sheet of every sprite.

Grown-up sprites are named like idle_happy_1.png, baby ones like baby_idle_happy_1.png.
"""
import os, sys
from PIL import Image, ImageDraw

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
S = 32

PAL = {
    "outline": (20, 20, 28, 255),
    "tux": (34, 35, 46, 255),
    "tuxhi": (66, 70, 92, 255),
    "white": (246, 246, 242, 255),
    "shade": (204, 212, 226, 255),
    "beak": (252, 196, 54, 255),
    "beakdk": (232, 124, 34, 255),
    "down": (150, 156, 172, 255),
    "downhi": (196, 201, 213, 255),
    "pink": (255, 140, 170, 255),
    "eye": (16, 16, 24, 255),
    "blue": (120, 200, 255, 255),
    "green": (130, 200, 80, 255),
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

    def image(self):
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        for (x, y), c in self.px.items():
            im.putpixel((x, y), c)
        return im


class Geo:
    """Where the face parts are, so moods and props can be drawn on either stage."""
    def __init__(self, eye_y, beak_y, cheek_y, face_bottom):
        self.eye_x = (11, 17)      # left edge of each 4px-wide eye area
        self.eye_y = eye_y         # middle row of the eyes
        self.beak_y = beak_y       # top row of the beak
        self.cheek_y = cheek_y
        self.face_bottom = face_bottom


def feet(c, rows, spans):
    for i, y in enumerate(rows):
        color = "beakdk" if i == len(rows) - 1 else "beak"
        for (x0, x1) in spans:
            for x in range(x0 + (1 if i == 0 else 0), x1 + 1 - (1 if i == 0 else 0)):
                c.set(x, y, color)


def adult(dy=0, fat=0):
    """Grown-up Sudo: a pear-shaped Tux-ish penguin with a little head tuft and blush."""
    c = Canvas()
    c.ellipse(5.4 - fat, 19 + dy, 2.4, 6, "tux")
    c.ellipse(26.6 + fat, 19 + dy, 2.4, 6, "tux")
    c.ellipse(16, 11 + dy, 8.2, 7.6, "tux")
    c.ellipse(16, 20.5 + dy, 11 + fat, 9.2, "tux")
    c.ellipse(11.5, 6 + dy, 2.4, 1.5, "tuxhi")
    # his own touch: a little curl of a tuft
    for (x, y) in ((16, 3), (17, 2), (18, 2), (19, 3)):
        c.set(x, y + dy, "tux")
    # pear-shaped belly and two separate eye whites, like Tux
    c.ellipse(16, 21.8 + dy, 8 + fat, 7.4, "white")
    c.ellipse(16, 26.2 + dy, 6.4 + fat, 2.4, "shade")
    c.ellipse(13, 10 + dy, 2.2, 3.4, "white")
    c.ellipse(19, 10 + dy, 2.2, 3.4, "white")
    feet(c, (28, 29, 30), ((7, 14), (17, 24)))
    c.outline()
    return c, Geo(eye_y=10 + dy, beak_y=13 + dy, cheek_y=13 + dy, face_bottom=14 + dy)


def baby(dy=0, fat=0):
    """Baby Sudo: a fluffy grey chick with a dark cap, a white face and a huge head."""
    c = Canvas()
    c.ellipse(6.6 - fat, 22 + dy, 2, 3.6, "down")
    c.ellipse(25.4 + fat, 22 + dy, 2, 3.6, "down")
    c.ellipse(16, 22.5 + dy, 9.6 + fat, 7, "down")
    c.ellipse(16, 23.5 + dy, 6.4 + fat, 5, "downhi")
    c.ellipse(16, 12.5 + dy, 8.8, 7.8, "tux")
    c.ellipse(12, 8 + dy, 2.2, 1.4, "tuxhi")
    c.ellipse(16, 14.4 + dy, 6.8, 4.8, "white")
    # a fluffy tuft sticking straight up
    for (x, y) in ((15, 4), (16, 3), (16, 2), (17, 4), (18, 3)):
        c.set(x, y + dy, "tux")
    # fuzz: nubs of down poking out of the body's edge
    for (x, y) in ((6, 19), (5, 24), (26, 19), (27, 24), (9, 28), (22, 28), (8, 26), (24, 26)):
        c.set(x, y + dy, "down")
    feet(c, (29, 30), ((11, 14), (17, 20)))
    c.outline()
    return c, Geo(eye_y=13 + dy, beak_y=16 + dy, cheek_y=15 + dy, face_bottom=18 + dy)


STAGES = {"": adult, "baby_": baby}


# ---------- face parts ----------

def beak(c, g, open_=False, small=False):
    y = g.beak_y
    if small:
        for x in (15, 16):
            c.set(x, y, "beak")
        for x in (14, 15, 16, 17):
            c.set(x, y + 1, "beak" if not open_ else "red" if x in (15, 16) else "beak")
        for x in (15, 16):
            c.set(x, y + 2, "beakdk")
        return
    for x in range(14, 18):
        c.set(x, y, "beak")
    for x in range(12, 20):
        c.set(x, y + 1, "beak")
    if open_:
        for x in range(14, 18):
            c.set(x, y + 2, "red")
        for x in range(13, 19):
            c.set(x, y + 3, "beakdk")
    else:
        for x in range(13, 19):
            c.set(x, y + 2, "beakdk")


def blush(c, g):
    for x in (9, 10, 21, 22):
        c.set(x, g.cheek_y, "pink")


def eyes(c, g, kind):
    ey = g.eye_y
    for i, x0 in enumerate(g.eye_x):
        inner = (x0 + 2, x0 + 3) if i == 0 else (x0, x0 + 1)   # pupils look slightly inward
        if kind == "open":
            for x in inner:
                for y in (ey - 1, ey, ey + 1):
                    c.set(x, y, "eye")
            c.set(inner[0] if i == 0 else inner[1], ey - 1, "white")
        elif kind == "big":
            for x in range(x0, x0 + 4):
                for y in range(ey - 2, ey + 2):
                    c.set(x, y, "eye")
            c.set(x0 + 2, ey - 2, "white")
            c.set(x0 + 3, ey - 1, "white")
            c.set(x0, ey + 1, "white")
        elif kind == "happy":   # ^ ^
            c.set(x0, ey + 1, "eye"); c.set(x0 + 1, ey, "eye")
            c.set(x0 + 2, ey, "eye"); c.set(x0 + 3, ey + 1, "eye")
        elif kind == "closed":  # - -
            for x in range(x0, x0 + 4):
                c.set(x, ey + 1, "eye")
        elif kind == "sad":
            for x in inner:
                for y in (ey, ey + 1):
                    c.set(x, y, "eye")
            # droopy lids, lower on the outer side
            outer = x0 if i == 0 else x0 + 3
            mid = x0 + 1 if i == 0 else x0 + 2
            c.set(outer, ey - 2, "tux"); c.set(outer, ey - 1, "tux"); c.set(mid, ey - 2, "tux")
        elif kind == "sleepy":  # heavy lids
            for x in range(x0, x0 + 4):
                c.set(x, ey - 1, "tux")
                c.set(x, ey, "eye")
            for x in inner:
                c.set(x, ey + 1, "eye")
        elif kind == "dizzy":   # x x
            for k in range(3):
                c.set(x0 + k, ey - 1 + k, "eye")
                c.set(x0 + 2 - k, ey - 1 + k, "eye")


# ---------- extras ----------

def drool(c, g, f):
    for k in range(2 + f):
        c.set(18, g.beak_y + 3 + k, "blue")


def tear(c, g, f):
    c.set(g.eye_x[0], g.eye_y + 2 + f, "blue")
    c.set(g.eye_x[0], g.eye_y + 3 + f, "blue")
    c.set(g.eye_x[1] + 3, g.eye_y + 2 + f, "blue")


def stink(c, g, f):
    for i, x in enumerate((2, 6, 25, 29)):
        off = (f + i) % 2
        for y in range(5, 10):
            c.set(x + ((y + off) % 2), y + (i % 2) * 2, "green")
    fx, fy = (24, 2) if f == 0 else (22, 1)
    c.set(fx, fy, "outline"); c.set(fx - 1, fy - 1, "shade"); c.set(fx + 1, fy - 1, "shade")


def sweat(c, g, f):
    for (x, y) in ((24, 5), (24, 6), (23, 6)):
        c.set(x, y + f, "blue")


def sparkles(c, g, f):
    pts = [(3, 4), (28, 6), (2, 14)] if f == 0 else [(29, 3), (4, 8), (29, 14)]
    for (x, y) in pts:
        c.set(x, y, "yellow")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.set(x + dx, y + dy, "yellow")


def thermometer(c, g, f):
    for (x, y), col in list(c.px.items()):
        if col == PAL["white"] and y < g.face_bottom:
            c.set(x, y, (208, 232, 184, 255))
    y = g.beak_y + 2
    for i in range(6):
        c.set(18 + i, y + i // 2, "outline")
        c.set(18 + i, y + 1 + i // 2, "shade")
    c.set(24, y + 2, "red"); c.set(24, y + 3, "red"); c.set(25, y + 3, "red")


def z_px(c, x, y, n):
    for i in range(n):
        c.set(x + i, y, "blue")
        c.set(x + i, y + n - 1, "blue")
        c.set(x + n - 1 - i, y + i, "blue")


def zzz(c, g, f):
    z_px(c, 23, 6 - f, 3)
    z_px(c, 26, 1 + f, 4)


def heart_px(c, x, y, col="red"):
    for dx, dy in ((0, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1),
                   (0, 2), (1, 2), (2, 2), (1, 3)):
        c.set(x + dx, y + dy, col)


def hearts(c, g, f):
    heart_px(c, 25, 4 - f)
    if f:
        heart_px(c, 3, 6)


def bubbles(c, g, f):
    pts = [(3, 22), (6, 16), (26, 21), (28, 14), (3, 10), (27, 8)]
    for i, (x, y) in enumerate(pts):
        y -= f * (1 + i % 2)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            c.set(x + dx, y + dy, "blue")
        c.set(x, y, "white")
    for x in range(5, 27):
        c.set(x, 27 + (x + f) % 2, "blue")


def ball(c, g, f):
    bx, by = (25, 1) if f == 0 else (26, 7)
    for y in range(by, by + 4):
        for x in range(bx, bx + 4):
            if (x - bx - 1.5) ** 2 + (y - by - 1.5) ** 2 <= 4:
                c.set(x, y, "green" if (x + y) % 3 else "yellow")


def fish_px(c, x, y):
    for dx in range(5):
        c.set(x + dx, y, "fish")
        c.set(x + dx, y + 1, "fishdk" if dx > 2 else "fish")
    c.set(x + 1, y - 1, "fish"); c.set(x + 2, y - 1, "fish")
    for dy in (-1, 0, 1, 2):
        c.set(x + 5, y + dy, "fishdk")
    c.set(x + 1, y, "eye")


# ---------- sprites ----------

made = []


def save(c, name):
    c.image().save(os.path.join(OUT, f"{name}.png"))
    made.append(name)


def mood(name, eye_kind, extras=None, frames=2, mouth_open=False, cheeks=True, fat=0):
    for prefix, draw in STAGES.items():
        for f in range(frames):
            c, g = draw(dy=f, fat=fat)
            eyes(c, g, eye_kind)
            beak(c, g, open_=mouth_open, small=bool(prefix))
            if cheeks:
                blush(c, g)
            if extras:
                extras(c, g, f)
            save(c, f"{prefix}{name}_{f + 1}")


mood("idle_happy", "happy")
mood("idle_neutral", "open", cheeks=False)
mood("idle_hungry", "big", drool)
mood("idle_sad", "sad", tear, cheeks=False)
mood("idle_stinky", "sleepy", stink, cheeks=False)
mood("idle_sleepy", "sleepy", zzz, cheeks=False)
mood("idle_sick", "dizzy", thermometer, cheeks=False)
mood("idle_overfed", "closed", sweat, fat=2)
mood("idle_ecstatic", "happy", sparkles, mouth_open=True)
mood("blink", "closed", frames=1, cheeks=False)
mood("pet", "happy", hearts)
mood("bath", "happy", bubbles)
mood("play", "happy", ball, mouth_open=True)
mood("sleep", "closed", zzz, cheeks=False)

# eat: sees the fish, chomps, happy with the tail sticking out
for prefix, draw in STAGES.items():
    for f in range(3):
        c, g = draw(dy=1 if f == 1 else 0)
        eyes(c, g, "big" if f == 0 else "closed" if f == 1 else "happy")
        beak(c, g, open_=(f == 0), small=bool(prefix))
        blush(c, g)
        if f == 0:
            fish_px(c, 22, g.beak_y + 2)
        elif f == 1:
            y = g.beak_y + 1
            c.set(19, y, "fishdk"); c.set(20, y - 1, "fishdk"); c.set(20, y + 1, "fishdk")
        save(c, f"{prefix}eat_{f + 1}")


# props: 16x16 items you drag onto Sudo, plus particles
def prop(name, draw, outline=True):
    c = Canvas()
    draw(c)
    if outline:
        c.outline()
    c.image().crop((0, 0, 16, 16)).save(os.path.join(OUT, f"{name}.png"))
    made.append(name)


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


def soap(c):
    for y in range(8, 13):
        for x in range(2, 13):
            c.set(x, y, "pink" if y > 8 else "white")
    for x, y in ((4, 5), (8, 3), (11, 6)):
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
            if 9 <= (x - 7.5) ** 2 + (y - 7.5) ** 2 <= 16:
                c.set(x, y, "blue")
    c.set(6, 6, "white"); c.set(6, 7, "white")


def sparkle(c):
    for i in range(-3, 4):
        c.set(8 + i, 8, "yellow")
        c.set(8, 8 + i, "yellow")
    c.set(8, 8, "white")


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

SC = 5
cols = 8
cell = S * SC + 12
rows = (len(made) + cols - 1) // cols
sheet = Image.new("RGBA", (cols * cell, rows * (cell + 16)), (18, 20, 28, 255))
d = ImageDraw.Draw(sheet)
for i, n in enumerate(made):
    im = Image.open(os.path.join(OUT, f"{n}.png"))
    im = im.resize((im.width * SC, im.height * SC), Image.NEAREST)
    x = (i % cols) * cell + 6
    y = (i // cols) * (cell + 16) + 6
    d.rectangle([x - 2, y - 2, x + S * SC + 1, y + S * SC + 1], fill=(40, 46, 70, 255))
    sheet.alpha_composite(im, (x, y))
    d.text((x, y + S * SC + 3), n, fill=(140, 255, 160, 255))
sheet.save(sys.argv[2])
print(len(made), "sprites")
