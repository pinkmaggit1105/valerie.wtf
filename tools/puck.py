"""Puck the goose: a fluffy gosling and a grown-up goose seen from the side, every mood, his egg,
his accessories and his items."""
from pixels import (Canvas, z_px, heart_px, sparkles, stink, bubbles, tint_face, eggs, hatch_start,
                    shell_bottom, flying_shell, common_props)

EGG_LOOK = dict(colors=("gooseegg", "gooseeggshade"), specks=False, grow=0.6)


class Geo:
    """Where Puck's face and neck are, so moods and accessories land in the right spot."""
    def __init__(self, eye_x, eye_y, beak_x, beak_y, cheek, head_top, hc, face_bottom, neck, bow_x, brow):
        self.eye_x, self.eye_y = eye_x, eye_y   # top-left of his 2x2 eye
        self.beak_x, self.beak_y = beak_x, beak_y
        self.cheek = cheek
        self.head_top = head_top
        self.hc = hc                            # middle of his head, for hats
        self.face_bottom = face_bottom
        self.neck = neck                        # (first x, last x, row) for a scarf
        self.bow_x = bow_x                      # front of the neck, for a bow tie
        self.brow = brow                        # grown-up Puck always looks a little suspicious


def adult(dy=0, fat=0, beak_open=False):
    """Grown-up Puck: a white goose with a long neck, a big orange beak and a lot of attitude."""
    c = Canvas()
    for (x, y) in ((2, 14), (3, 14), (3, 15), (4, 15), (4, 16), (5, 16), (5, 17), (6, 17), (6, 18)):
        c.set(x, y + dy, "goosewing")
    c.ellipse(13, 21 + dy, 10 + fat, 6.4, "goose")
    c.ellipse(13, 25 + dy, 8 + fat, 2.2, "gooseshade")
    c.ellipse(10.5, 19.6 + dy, 6.6, 3.3, "goosewing")
    for x in (7, 10, 13):
        c.set(x, 21 + dy, "gooseshade")
    for y in range(9, 18):
        for x in (range(20, 24) if y < 12 else range(19, 23)):
            c.set(x, y + dy, "goose")
    c.ellipse(22.5, 6.8 + dy, 4.4, 3.6, "goose")
    b = 6 + dy
    if beak_open:
        for x in range(27, 30):
            c.set(x, b - 1, "gooseorange")
        for x in range(27, 31):
            c.set(x, b, "gooseorange")
        c.set(27, b + 1, "red"); c.set(28, b + 1, "red")
        for x in range(27, 30):
            c.set(x, b + 2, "gooseorangedk")
    else:
        for x in range(27, 30):
            c.set(x, b, "gooseorange")
        for x in range(27, 31):
            c.set(x, b + 1, "gooseorange")
        for x in range(27, 30):
            c.set(x, b + 2, "gooseorangedk")
    for y in (28, 29):
        c.set(10, y, "gooseorange"); c.set(15, y, "gooseorange")
    for x in (8, 9, 10, 11, 13, 14, 15, 16):
        c.set(x, 30, "gooseorangedk")
    c.outline()
    return c, Geo(eye_x=23, eye_y=5 + dy, beak_x=27, beak_y=b, cheek=(21, 8 + dy), head_top=3 + dy, hc=22,
                  face_bottom=11 + dy, neck=(18, 23, 11 + dy), bow_x=21, brow=True)


def baby(dy=0, fat=0, beak_open=False):
    """Baby Puck: a round yellow gosling with a big fluffy head and a little grey beak."""
    c = Canvas()
    for (x, y) in ((5, 19), (6, 20), (5, 20)):
        c.set(x, y + dy, "gosling")
    c.ellipse(15, 22.6 + dy, 8.6 + fat, 5.9, "gosling")
    c.ellipse(15.5, 24.5 + dy, 6 + fat, 3.4, "goslinghi")
    c.ellipse(11.5, 21.5 + dy, 3.8, 2.4, "goslingdk")
    c.ellipse(19.5, 12.5 + dy, 5.6, 5.2, "gosling")
    for (x, y) in ((19, 6), (20, 5), (21, 6)):
        c.set(x, y + dy, "gosling")
    b = 12 + dy
    if beak_open:
        for x in (25, 26):
            c.set(x, b - 1, "slate")
        for x in (25, 26, 27):
            c.set(x, b, "slate")
        c.set(25, b + 1, "red"); c.set(26, b + 1, "red")
        for x in (25, 26):
            c.set(x, b + 2, "slate")
    else:
        for x in (25, 26):
            c.set(x, b, "slate")
        for x in (25, 26, 27):
            c.set(x, b + 1, "slate")
        for x in (25, 26):
            c.set(x, b + 2, "grey")
    c.set(12, 29, "slate"); c.set(17, 29, "slate")
    for x in (11, 12, 13, 16, 17, 18):
        c.set(x, 30, "slate")
    c.outline()
    return c, Geo(eye_x=20, eye_y=10 + dy, beak_x=25, beak_y=b, cheek=(18, 13 + dy), head_top=7 + dy, hc=19,
                  face_bottom=16 + dy, neck=(15, 23, 17 + dy), bow_x=20, brow=False)


STAGES = {"": adult, "baby_": baby}


def eyes(c, g, kind):
    x, y = g.eye_x, g.eye_y
    if kind == "open":
        for dx in (0, 1):
            for dy in (0, 1):
                c.set(x + dx, y + dy, "eye")
        c.set(x + 1, y, "white")
        if g.brow:
            for (bx, by) in ((x - 1, y - 2), (x, y - 2), (x + 1, y - 1), (x + 2, y - 1)):
                c.set(bx, by, "eye")
    elif kind == "big":
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                c.set(x + dx, y + dy, "eye")
        c.set(x, y - 1, "white"); c.set(x - 1, y + 1, "white")
    elif kind == "happy":
        for (ex, ey) in ((x - 1, y + 1), (x, y), (x + 1, y), (x + 2, y + 1)):
            c.set(ex, ey, "eye")
    elif kind == "closed":
        for ex in range(x - 1, x + 3):
            c.set(ex, y + 1, "eye")
    elif kind == "sad":
        c.set(x, y + 1, "eye"); c.set(x + 1, y + 1, "eye")
        for (bx, by) in ((x - 1, y - 1), (x, y - 2), (x + 1, y - 2)):
            c.set(bx, by, "eye")
    elif kind == "sleepy":
        for ex in range(x - 1, x + 3):
            c.set(ex, y, "eye")
        c.set(x, y + 1, "eye"); c.set(x + 1, y + 1, "eye")
    elif kind == "dizzy":
        for k in range(3):
            c.set(x - 1 + k, y - 1 + k, "eye")
            c.set(x + 1 - k, y - 1 + k, "eye")


def blush(c, g):
    cx, cy = g.cheek
    c.set(cx, cy, "pink"); c.set(cx + 1, cy, "pink")


# ---------- extras ----------

def drool(c, g, f):
    for k in range(2 + f):
        c.set(g.beak_x + 1, g.beak_y + 3 + k, "blue")


def tear(c, g, f):
    c.set(g.eye_x, g.eye_y + 2 + f, "blue")
    c.set(g.eye_x, g.eye_y + 3 + f, "blue")


def sweat(c, g, f):
    t = g.head_top
    for (x, y) in ((g.hc - 4, t + 1), (g.hc - 4, t + 2), (g.hc - 5, t + 2)):
        c.set(x, y + f, "blue")


def thermometer(c, g, f):
    tint_face(c, g.face_bottom, ["goose", "gosling", "goslinghi"])
    y = g.beak_y + 3
    for i in range(4):
        c.set(g.beak_x + i, y + i // 2, "outline")
        c.set(g.beak_x + i, y + 1 + i // 2, "shade")
    c.set(g.beak_x + 4, y + 2, "red"); c.set(g.beak_x + 4, y + 3, "red")


def zzz(c, g, f):
    z_px(c, 10, 10 - f, 3)
    z_px(c, 5, 4 + f, 4)


def hearts(c, g, f):
    heart_px(c, 13, 8 - f)
    if f:
        heart_px(c, 3, 9)


def bell(c, g, f):
    s = -f   # the bell swings
    for x in (28, 29):
        c.set(x + s, 1, "golddk")
    for x in range(27, 31):
        c.set(x + s, 2, "gold"); c.set(x + s, 3, "gold")
    for x in range(26, 32):
        c.set(x + s, 4, "golddk")
    c.set(28 + s, 5, "brown")


def leaf_px(c, x, y):
    for (dx, dy) in ((1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2), (2, 2)):
        c.set(x + dx, y + dy, "leaf")
    c.set(x + 1, y + 1, "leafdk"); c.set(x + 2, y + 1, "leafdk")


# ---------- accessories ----------

def tophat(c, g):
    t, h = g.head_top, g.hc
    for x in range(h - 4, h + 5):
        c.set(x, t, "plumdk")
    for y in range(t - 4, t):
        for x in range(h - 3, h + 4):
            c.set(x, y, "plum")
    for x in range(h - 3, h + 4):
        c.set(x, t - 1, "beak")


def bow(c, g):
    t, x0 = g.head_top + 1, g.hc - 6
    for (dx, dy) in ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)):
        c.set(x0 + dx, t + dy, "bow")
    for (dx, dy) in ((6, 0), (6, 1), (6, 2), (5, 0), (5, 1), (5, 2), (4, 1)):
        c.set(x0 + dx, t + dy, "bow")
    c.set(x0 + 3, t + 1, "bowdk")
    c.set(x0, t, "white")


def partyhat(c, g):
    t, h = g.head_top, g.hc
    for i, y in enumerate(range(t - 4, t + 1)):
        half = i // 2 + (1 if i == 4 else 0)
        for x in range(h - half, h + half + 1):
            c.set(x, y, "yellow" if (x + y) % 4 < 2 else "bow")
    for x in (h - 1, h, h + 1):
        c.set(x, t - 5, "teal")


def flowers(c, g):
    t, h = g.head_top + 1, g.hc
    for x in range(h - 4, h + 5):
        c.set(x, t, "leaf")
    for i, x in enumerate((h - 3, h, h + 3)):
        petal = ("bow", "yellow", "blue")[i]
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            c.set(x + dx, t - 1 + dy, petal)
        c.set(x, t - 1, "white")


def crown(c, g):
    t, h = g.head_top, g.hc
    for y in (t, t + 1):
        for x in range(h - 3, h + 4):
            c.set(x, y, "gold" if y == t else "golddk")
    for x in (h - 3, h, h + 3):
        c.set(x, t - 1, "gold")
    c.set(h, t - 2, "gold")
    c.set(h - 2, t, "red"); c.set(h, t, "blue"); c.set(h + 2, t, "red")


def sunhat(c, g):
    t, h = g.head_top, g.hc
    for x in range(h - 6, h + 7):
        c.set(x, t + 1, "straw")
    for y in range(t - 2, t + 1):
        for x in range(h - 3, h + 4):
            c.set(x, y, "straw")
    for x in range(h - 3, h + 4):
        c.set(x, t, "bow")
    for x in (h - 5, h - 1, h + 3):
        c.set(x, t + 1, "strawdk")


def shades(c, g):
    x, y = g.eye_x, g.eye_y
    for ex in range(x - 1, x + 3):
        for ey in (y, y + 1):
            c.set(ex, ey, "eye")
    c.set(x, y, "white")
    for ex in range(g.hc - 4, x - 1):
        c.set(ex, y, "eye")


def heartshades(c, g):
    x, y = g.eye_x - 2, g.eye_y - 1
    for (dx, dy) in ((0, 0), (1, 0), (3, 0), (4, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                     (1, 2), (2, 2), (3, 2), (2, 3)):
        c.set(x + dx, y + dy, "red")
    c.set(x + 1, y, "pink")
    for ex in range(g.hc - 4, x):
        c.set(ex, y + 1, "red")


def scarf(c, g):
    x0, x1, n = g.neck
    for y in (n, n + 1):
        for x in range(x0, x1 + 1):
            c.set(x, y, "white" if x % 4 == 0 else "scarf")
    for y in range(n + 2, n + 6):
        for x in (x0, x0 + 1):
            c.set(x, y, "white" if y % 3 == 0 else "scarf")


def bowtie(c, g):
    _, _, n = g.neck
    b = g.bow_x
    for (dx, dy) in ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)):
        c.set(b - 3 + dx, n + 1 + dy, "bowtie")
        c.set(b + 3 - dx, n + 1 + dy, "bowtie")
    c.set(b, n + 2, "blue")


ACCESSORIES = [("tophat", tophat), ("bow", bow), ("partyhat", partyhat), ("flowers", flowers), ("crown", crown),
               ("sunhat", sunhat), ("shades", shades), ("heartshades", heartshades), ("scarf", scarf), ("bowtie", bowtie)]


# ---------- items ----------

def lettuce(c):
    c.ellipse(7.5, 8, 5.5, 4.6, "green")
    c.ellipse(7.5, 8.5, 4.2, 3.4, "leaf")
    for y in range(5, 12):
        c.set(7, y, "leafdk")
    for (x, y) in ((5, 7), (6, 8), (9, 7), (8, 8), (5, 10), (9, 10)):
        c.set(x, y, "leafdk")


def watering_can(c):
    for y in range(7, 13):
        for x in range(3, 10):
            c.set(x, y, "teal")
    for x in range(4, 9):
        c.set(x, 5, "teal")
    c.set(3, 6, "teal"); c.set(9, 6, "teal")
    for i in range(5):
        c.set(10 + i, 10 - i, "teal")
    c.set(14, 5, "metal"); c.set(15, 5, "metal")
    c.set(14, 7, "blue"); c.set(15, 9, "blue"); c.set(13, 8, "blue")
    c.set(4, 8, "white")


def bell_prop(c):
    c.set(7, 2, "golddk"); c.set(8, 2, "golddk")
    for y, (x0, x1) in zip(range(3, 10), ((7, 8), (6, 9), (5, 10), (5, 10), (4, 11), (4, 11), (4, 11))):
        for x in range(x0, x1 + 1):
            c.set(x, y, "gold")
    for x in range(3, 13):
        c.set(x, 10, "golddk")
    c.set(7, 11, "brown"); c.set(8, 11, "brown"); c.set(7, 12, "brown"); c.set(8, 12, "brown")
    c.set(6, 5, "white"); c.set(5, 6, "white")


def basket(c):
    for (x, y) in ((4, 7), (4, 6), (5, 5), (5, 4), (6, 3), (7, 3), (8, 3), (9, 3), (10, 4), (10, 5), (11, 6), (11, 7)):
        c.set(x, y, "strawdk")
    for x in range(4, 12):
        c.set(x, 7, "red" if x % 2 else "white")
    for y in range(8, 14):
        for x in range(2, 14):
            c.set(x, y, "strawdk" if (x + y) % 3 == 0 else "straw")


def eye_watch(c, look=0):
    c.ellipse(7.5, 8, 6.4, 3.6, "white")
    c.ellipse(7.5 + look, 8, 2.4, 2.4, "teal")
    c.ellipse(7.5 + look, 8, 1.2, 1.2, "eye")
    c.set(7 + look, 7, "white")
    for x in (3, 6, 9, 12):
        c.set(x, 3, "outline")


def strawberry(c):
    for y, (x0, x1) in zip(range(5, 13), ((4, 11), (3, 12), (3, 12), (4, 11), (4, 11), (5, 10), (6, 9), (7, 8))):
        for x in range(x0, x1 + 1):
            c.set(x, y, "red")
    for (x, y) in ((5, 7), (8, 6), (10, 8), (6, 10), (9, 10), (7, 8)):
        c.set(x, y, "yellow")
    for (x, y) in ((5, 4), (6, 4), (7, 3), (8, 4), (9, 4), (10, 4), (7, 2)):
        c.set(x, y, "leaf")


def sandwich(c):
    for y, color in zip(range(4, 13), ("bread", "bread", "leaf", "red", "yellow", "bread", "bread", "breaddk", "breaddk")):
        for x in range(2 + max(0, 6 - y), 14 - max(0, 6 - y)):
            c.set(x, y, color)
    c.set(5, 5, "white")


def sunhat_item(c):
    c.ellipse(7.5, 10, 7, 2.2, "straw")
    c.ellipse(7.5, 7, 3.6, 3, "straw")
    for x in range(4, 12):
        c.set(x, 8, "bow")
    for x in (2, 6, 10, 13):
        c.set(x, 10, "strawdk")


def keys(c):
    for (x, y) in ((3, 3), (4, 2), (5, 2), (6, 3), (6, 4), (5, 5), (4, 5), (3, 4)):
        c.set(x, y, "metal")
    for i in range(7):
        c.set(6 + i, 5 + i, "gold")
    c.set(10, 10, "gold"); c.set(11, 9, "gold")
    for i in range(6):
        c.set(4 + i // 3, 6 + i, "metal")
    c.set(6, 10, "metal"); c.set(6, 11, "metal")


def phone(c):
    for y in range(2, 14):
        for x in range(5, 11):
            c.set(x, y, "grey")
    for y in range(3, 12):
        for x in range(6, 10):
            c.set(x, y, "blue")
    c.set(6, 3, "white"); c.set(7, 12, "metal"); c.set(8, 12, "metal")


def sock(c):
    for y in range(2, 11):
        for x in range(5, 9):
            c.set(x, y, "scarf" if y % 3 else "white")
    for y in range(10, 13):
        for x in range(5, 12):
            c.set(x, y, "scarf" if (x + y) % 4 else "white")
    for x in range(5, 9):
        c.set(x, 2, "white")


def build(out):
    def mood(name, eye_kind, extras=None, frames=2, mouth_open=False, cheeks=True, fat=0):
        for prefix, draw in STAGES.items():
            for f in range(frames):
                c, g = draw(dy=f, fat=fat, beak_open=mouth_open)
                eyes(c, g, eye_kind)
                if cheeks:
                    blush(c, g)
                if extras:
                    extras(c, g, f)
                out.save(c, f"{prefix}{name}_{f + 1}")

    mood("idle_happy", "happy")
    mood("idle_neutral", "open", cheeks=False)
    mood("idle_hungry", "big", drool, mouth_open=True)
    mood("idle_sad", "sad", tear, cheeks=False)
    mood("idle_stinky", "sleepy", stink, cheeks=False)
    mood("idle_sleepy", "sleepy", zzz, cheeks=False)
    mood("idle_sick", "dizzy", thermometer, cheeks=False)
    mood("idle_overfed", "closed", sweat, fat=2)
    mood("idle_ecstatic", "happy", sparkles, mouth_open=True)
    mood("blink", "closed", frames=1, cheeks=False)
    mood("pet", "happy", hearts)
    mood("bath", "happy", bubbles)
    mood("play", "happy", bell, mouth_open=True)
    mood("sleep", "closed", zzz, cheeks=False)

    # eat: spots the lettuce, chomps, happy with a crumb left over
    for prefix, draw in STAGES.items():
        for f in range(3):
            c, g = draw(dy=1 if f == 1 else 0, beak_open=(f == 0))
            eyes(c, g, "big" if f == 0 else "closed" if f == 1 else "happy")
            blush(c, g)
            if f == 0:
                leaf_px(c, g.beak_x, g.beak_y + 4)
            elif f == 1:
                c.set(g.beak_x + 1, g.beak_y + 3, "leafdk"); c.set(g.beak_x + 3, g.beak_y + 4, "leaf")
            out.save(c, f"{prefix}eat_{f + 1}")

    eggs(out, **EGG_LOOK)
    hatch_start(out, **EGG_LOOK)
    c, g = baby()
    eyes(c, g, "closed")
    shell_bottom(c, colors=EGG_LOOK["colors"], grow=1.0)
    flying_shell(c, "gooseegg")
    out.save(c, "hatch_2")
    c, g = baby(beak_open=True)
    eyes(c, g, "happy")
    blush(c, g)
    sparkles(c, g, 0)
    for (x, y) in ((4, 29), (5, 29), (5, 28), (26, 29), (27, 29), (26, 28), (9, 30), (23, 30)):
        c.set(x, y, "gooseegg")
    out.save(c, "hatch_3")

    for name, draw in ACCESSORIES:
        for prefix, body in STAGES.items():
            _, g = body()
            c = Canvas()
            draw(c, g)
            c.outline("frame" if name == "shades" else "outline")
            out.save(c, f"{prefix}acc_{name}")

    common_props(out)
    out.prop("lettuce", lettuce)
    out.prop("can", watering_can)
    out.prop("bell", bell_prop)
    out.prop("basket", basket)
    out.prop("eye_watch", eye_watch)
    out.prop("eye_away", lambda c: eye_watch(c, look=-3))
    out.prop("strawberry", strawberry)
    out.prop("sandwich", sandwich)
    out.prop("sunhat", sunhat_item)
    out.prop("keys", keys)
    out.prop("phone", phone)
    out.prop("sock", sock)
