"""Sudo the penguin: baby and grown-up bodies, every mood, his egg, his accessories and his items."""
from pixels import (Canvas, PAL, z_px, heart_px, sparkles, stink, bubbles, tint_face, eggs, hatch_start,
                    shell_bottom, flying_shell, big_fish, recolor_fish, common_props)


class Geo:
    """Where the face parts are, so moods and props can be drawn on either stage."""
    def __init__(self, eye_y, beak_y, cheek_y, face_bottom, head_top, neck_y):
        self.eye_x = (11, 17)      # left edge of each 4px-wide eye area
        self.eye_y = eye_y         # middle row of the eyes
        self.beak_y = beak_y       # top row of the beak
        self.cheek_y = cheek_y
        self.face_bottom = face_bottom
        self.head_top = head_top   # first row of the head (not counting the tuft)
        self.neck_y = neck_y       # where a scarf goes


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
    return c, Geo(eye_y=10 + dy, beak_y=13 + dy, cheek_y=13 + dy, face_bottom=14 + dy, head_top=3 + dy, neck_y=16 + dy)


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
    return c, Geo(eye_y=13 + dy, beak_y=16 + dy, cheek_y=15 + dy, face_bottom=18 + dy, head_top=5 + dy, neck_y=19 + dy)


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


def sweat(c, g, f):
    for (x, y) in ((24, 5), (24, 6), (23, 6)):
        c.set(x, y + f, "blue")


def thermometer(c, g, f):
    tint_face(c, g.face_bottom, ["white"])
    y = g.beak_y + 2
    for i in range(6):
        c.set(18 + i, y + i // 2, "outline")
        c.set(18 + i, y + 1 + i // 2, "shade")
    c.set(24, y + 2, "red"); c.set(24, y + 3, "red"); c.set(25, y + 3, "red")


def zzz(c, g, f):
    z_px(c, 23, 6 - f, 3)
    z_px(c, 26, 1 + f, 4)


def hearts(c, g, f):
    heart_px(c, 25, 4 - f)
    if f:
        heart_px(c, 3, 6)


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


# ---------- accessories: one overlay per stage, lined up with that stage's head ----------

def tophat(c, g):
    t = g.head_top
    for x in range(9, 23):
        c.set(x, t + 1, "plumdk")
    for y in range(t - 4, t + 1):
        for x in range(11, 21):
            c.set(x, y, "plum")
    for x in range(11, 21):
        c.set(x, t, "beak")
    c.set(12, t - 3, "plumdk"); c.set(12, t - 2, "plumdk")


def beanie(c, g):
    t = g.head_top
    for y in range(t - 2, t + 4):
        for x in range(32):
            if ((x + 0.5 - 16) / 8.6) ** 2 + ((y + 0.5 - (t + 4)) / 6) ** 2 <= 1:
                c.set(x, y, "knitdk" if x % 3 == 0 else "knit")
    for x in range(7, 25):
        c.set(x, t + 3, "white" if x % 2 else "shade")
    for (x, y) in ((15, t - 4), (16, t - 4), (15, t - 3), (16, t - 3), (14, t - 3), (17, t - 3)):
        c.set(x, y, "white")


def bow(c, g):
    t = g.head_top
    x0, y0 = 18, t
    for (dx, dy) in ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)):
        c.set(x0 + dx, y0 + dy, "bow")
    for (dx, dy) in ((6, 0), (6, 1), (6, 2), (5, 0), (5, 1), (5, 2), (4, 1)):
        c.set(x0 + dx, y0 + dy, "bow")
    c.set(x0 + 3, y0 + 1, "bowdk")
    c.set(x0, y0, "white")


def crown(c, g):
    t = g.head_top
    for y in range(t - 1, t + 2):
        for x in range(10, 22):
            c.set(x, y, "gold")
    for x in (10, 13, 15, 16, 18, 21):
        c.set(x, t - 2, "gold")
    for x in (10, 15, 16, 21):
        c.set(x, t - 3, "gold")
    for x in range(10, 22):
        c.set(x, t + 1, "golddk")
    c.set(12, t, "red"); c.set(15, t, "blue"); c.set(16, t, "blue"); c.set(19, t, "red")


def shades(c, g):
    ey = g.eye_y
    for i, x0 in enumerate(g.eye_x):
        left = x0 - 1 if i == 0 else x0
        for y in range(ey - 1, ey + 2):
            for x in range(left, left + 5):
                c.set(x, y, "eye")
        c.set(left + 1, ey - 1, "white"); c.set(left + 2, ey, "white")
    for x in (15, 16):
        c.set(x, ey - 1, "eye")


def scarf(c, g):
    n = g.neck_y
    for y in (n, n + 1):
        for x in range(7, 25):
            c.set(x, y, "white" if x % 4 == 0 else "scarf")
    for y in range(n + 2, n + 6):
        for x in (19, 20):
            c.set(x, y, "white" if y % 3 == 0 else "scarf")


def partyhat(c, g):
    t = g.head_top
    for i, y in enumerate(range(t - 2, t + 4)):
        half = i // 2 + (1 if i == 5 else 0)
        for x in range(15 - half, 17 + half):
            c.set(x, y, "yellow" if (x + y) % 4 < 2 else "bow")
    for x in (14, 15, 16, 17):
        c.set(x, t - 3, "teal")


def flowers(c, g):
    t = g.head_top + 1
    for x in range(8, 24):
        c.set(x, t, "leaf")
    for i, x in enumerate((9, 13, 18, 22)):
        petal = ("bow", "yellow", "blue", "bow")[i]
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            c.set(x + dx, t - 1 + dy, petal)
        c.set(x, t - 1, "white")


def headphones(c, g):
    t = g.head_top
    for x in range(10, 22):
        c.set(x, t - 1, "grey")
    for (x, y) in ((8, t), (9, t), (22, t), (23, t), (7, t + 1), (24, t + 1)):
        c.set(x, y, "grey")
    for y in range(g.eye_y - 1, g.eye_y + 3):
        for x in (5, 6, 7):
            c.set(x, y, "teal")
        for x in (24, 25, 26):
            c.set(x, y, "teal")
    for y in range(t + 2, g.eye_y - 1):
        c.set(7, y, "grey"); c.set(24, y, "grey")


def bowtie(c, g):
    n = g.neck_y
    for (dx, dy) in ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)):
        c.set(12 + dx, n + dy, "bowtie")
        c.set(19 - dx, n + dy, "bowtie")
    c.set(15, n + 1, "blue"); c.set(16, n + 1, "blue")


def heartshades(c, g):
    ey = g.eye_y
    for i, x0 in enumerate(g.eye_x):
        left = x0 - 1 if i == 0 else x0
        for (dx, dy) in ((0, 0), (1, 0), (3, 0), (4, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                         (1, 2), (2, 2), (3, 2), (2, 3)):
            c.set(left + dx, ey - 2 + dy, "red")
        c.set(left + 1, ey - 2, "pink")
    for x in (15, 16):
        c.set(x, ey - 1, "red")


def fishhat(c, g):
    t = g.head_top
    for y in range(t - 2, t + 3):
        for x in range(8, 21):
            if ((x + 0.5 - 14) / 6.5) ** 2 + ((y + 0.5 - (t + 0.5)) / 2.6) ** 2 <= 1:
                c.set(x, y, "gold" if y < t + 1 else "golddk")
    for i in range(3):
        for y in range(t - i, t + 1 + i):
            c.set(21 + i, y, "golddk")
    c.set(10, t, "eye")
    c.set(12, t - 1, "white")


def wizard(c, g):
    t = g.head_top
    for x in range(8, 24):
        c.set(x, t + 1, "wizarddk")
    for i, (x0, x1) in enumerate(((11, 20), (12, 19), (13, 18), (14, 17))):
        for x in range(x0, x1 + 1):
            c.set(x, t - i, "wizard")
    c.set(17, t - 4, "wizard"); c.set(18, t - 4, "wizard")
    for (x, y) in ((13, t), (17, t - 1), (15, t - 2)):
        c.set(x, y, "yellow")


def chef(c, g):
    t = g.head_top
    for x in range(10, 22):
        c.set(x, t + 1, "shade"); c.set(x, t, "white")
    c.ellipse(16, t - 1.5, 7, 2.6, "white")
    for x in (12, 16, 19):
        c.set(x, t - 1, "shade")


def halo(c, g):
    t = g.head_top - 2
    for x in range(12, 20):
        c.set(x, t - 1, "gold"); c.set(x, t + 1, "golddk")
    c.set(11, t, "gold"); c.set(20, t, "gold")


def pirate(c, g):
    t = g.head_top
    for x in range(8, 24):
        c.set(x, t + 1, "pirate")
    for x in range(9, 23):
        c.set(x, t + 1, "gold" if x % 2 else "pirate")
    for y in range(t - 2, t + 1):
        for x in range(10 + (t - y), 22 - (t - y)):
            c.set(x, y, "pirate")
    c.set(15, t - 1, "white"); c.set(16, t - 1, "white"); c.set(15, t, "white"); c.set(16, t, "white")


def monocle(c, g):
    ey = g.eye_y
    for (x, y) in ((17, ey - 2), (18, ey - 2), (19, ey - 2), (20, ey - 2), (16, ey - 1), (21, ey - 1), (16, ey), (21, ey),
                   (16, ey + 1), (21, ey + 1), (17, ey + 2), (18, ey + 2), (19, ey + 2), (20, ey + 2)):
        c.set(x, y, "gold")
    for i in range(4):
        c.set(21 + (i + 1) // 2, ey + 3 + i, "golddk")


def pearls(c, g):
    n = g.neck_y
    for x in range(8, 24):
        y = n + (1 if 11 <= x <= 20 else 0) + (1 if 13 <= x <= 18 else 0)
        c.set(x, y, "pearl" if x % 2 else "pearlsh")


ACCESSORIES = [("wizard", wizard), ("chef", chef), ("halo", halo), ("pirate", pirate), ("monocle", monocle), ("pearls", pearls),
               ("tophat", tophat), ("beanie", beanie), ("bow", bow), ("crown", crown), ("shades", shades),
               ("scarf", scarf), ("partyhat", partyhat), ("flowers", flowers), ("headphones", headphones),
               ("bowtie", bowtie), ("heartshades", heartshades), ("fishhat", fishhat)]


# ---------- items ----------

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


def boot(c):
    for y in range(3, 12):
        for x in range(5, 10):
            c.set(x, y, "brown")
    for y in range(9, 13):
        for x in range(5, 14):
            c.set(x, y, "brown")
    for x in range(5, 14):
        c.set(x, 13, "browndk")
    for y in (5, 7):
        c.set(6, y, "browndk"); c.set(8, y, "browndk")


def seaweed(c):
    for i, x0 in enumerate((5, 8, 11)):
        for y in range(3 + i, 14):
            c.set(x0 + (1 if (y + i) % 4 < 2 else 0), y, "leaf" if i != 1 else "leafdk")


def icecube(c):
    for y in range(5, 12):
        for x in range(4, 12):
            c.set(x, y, "ice")
    for x in range(4, 12):
        c.set(x, 5, "white")
    c.set(5, 7, "white"); c.set(5, 8, "white")


def rod(c):
    for i in range(11):
        c.set(2 + i, 13 - i, "wood")
    for y in range(3, 12):
        c.set(13, y, "shade")
    c.set(13, 12, "red"); c.set(13, 13, "white")


def bobber(c):
    for y in range(5, 12):
        for x in range(5, 11):
            if (x - 7.5) ** 2 + (y - 8.5) ** 2 <= 10:
                c.set(x, y, "red" if y < 9 else "white")
    c.set(8, 4, "outline"); c.set(8, 3, "outline")
    c.set(6, 6, "white")


def bobber_dip(c):
    for y in range(9, 13):
        for x in range(5, 11):
            if (x - 7.5) ** 2 + (y - 11) ** 2 <= 8:
                c.set(x, y, "red" if y < 11 else "white")
    for (x, y) in ((3, 8), (2, 6), (12, 8), (13, 6), (4, 5), (11, 5)):
        c.set(x, y, "blue")


def sushi(c):
    for (cx, top) in ((5, 6), (10, 6)):
        c.ellipse(cx, 10, 3.2, 2.6, "rice")
        for x in range(cx - 3, cx + 3):
            c.set(x, top + 2, "salmon"); c.set(x, top + 3, "salmon")
        for y in range(top + 4, top + 7):
            c.set(cx - 1, y, "nori"); c.set(cx, y, "nori")
    for x in range(1, 15):
        c.set(x, 13, "brown")


def taco(c):
    for y in range(5, 13):
        for x in range(2, 14):
            if (x - 7.5) ** 2 / 36 + (y - 12) ** 2 / 49 <= 1 and y >= 6:
                c.set(x, y, "gold" if y > 7 else "beak")
    for x in range(3, 13):
        c.set(x, 5 + (x % 2), "leaf")
    for x in (4, 7, 10):
        c.set(x, 6, "red")
    c.set(6, 5, "fish"); c.set(9, 5, "fish")


def icecream(c):
    for i, y in enumerate(range(8, 15)):
        for x in range(4 + i // 2, 12 - i // 2):
            c.set(x, y, "cone" if (x + y) % 3 else "conedk")
    c.ellipse(8, 6, 4.4, 3.4, "icecream")
    c.set(6, 4, "white"); c.set(8, 1, "red"); c.set(8, 2, "red"); c.set(9, 1, "red")


def build(out):
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
                out.save(c, f"{prefix}{name}_{f + 1}")

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
            out.save(c, f"{prefix}eat_{f + 1}")

    # the egg, and hatching: it shakes and cracks, the top pops off, then baby Sudo says hi
    eggs(out)
    hatch_start(out)
    c, g = baby()
    eyes(c, g, "closed")
    beak(c, g, small=True)
    shell_bottom(c)
    flying_shell(c)
    out.save(c, "hatch_2")
    c, g = baby()
    eyes(c, g, "happy")
    beak(c, g, open_=True, small=True)
    blush(c, g)
    sparkles(c, g, 0)
    for (x, y) in ((4, 29), (5, 29), (5, 28), (26, 29), (27, 29), (26, 28), (9, 30), (23, 30)):
        c.set(x, y, "eggshell")
    out.save(c, "hatch_3")

    for name, draw in ACCESSORIES:
        for prefix, body in STAGES.items():
            _, g = body()
            c = Canvas()
            draw(c, g)
            c.outline("frame" if name == "shades" else "outline")
            out.save(c, f"{prefix}acc_{name}")

    common_props(out)
    out.prop("fish", big_fish)
    out.prop("soap", soap)
    out.prop("ball", ball_prop)
    out.prop("bigfish", lambda c: recolor_fish(c, "orangefish", "orangefishdk"))

    def golden(c):
        recolor_fish(c, "gold", "golddk")
        for (x, y) in ((2, 2), (13, 3), (1, 13)):
            c.set(x, y, "yellow")
    out.prop("goldfish", golden)
    out.prop("boot", boot)
    out.prop("seaweed", seaweed)
    out.prop("icecube", icecube)
    out.prop("rod", rod)
    out.prop("bobber", bobber)
    out.prop("bobber_dip", bobber_dip)
    out.prop("sushi", sushi)
    out.prop("taco", taco)
    out.prop("icecream", icecream)
