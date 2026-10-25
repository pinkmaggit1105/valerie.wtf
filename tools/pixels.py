"""Shared pixel-art tools for the pet sprites: the palette, a tiny canvas, eggs, items and effects."""
import os
from PIL import Image, ImageDraw

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
    "eggshell": (247, 242, 230, 255),
    "eggshade": (220, 211, 192, 255),
    "speck": (168, 182, 206, 255),
    "coldshell": (212, 231, 250, 255),
    "coldshade": (166, 198, 236, 255),
    "plum": (112, 46, 100, 255),
    "plumdk": (78, 28, 70, 255),
    "gold": (255, 206, 64, 255),
    "golddk": (212, 148, 30, 255),
    "knit": (72, 194, 176, 255),
    "knitdk": (40, 146, 134, 255),
    "bow": (255, 122, 172, 255),
    "bowdk": (210, 70, 130, 255),
    "scarf": (226, 62, 74, 255),
    "frame": (255, 96, 178, 255),
    "leaf": (92, 186, 84, 255),
    "leafdk": (52, 130, 60, 255),
    "grey": (88, 92, 110, 255),
    "teal": (64, 200, 210, 255),
    "bowtie": (86, 120, 240, 255),
    "brown": (140, 88, 52, 255),
    "browndk": (96, 58, 34, 255),
    "orangefish": (246, 128, 64, 255),
    "orangefishdk": (200, 80, 40, 255),
    "ice": (200, 236, 255, 255),
    "poop": (124, 80, 48, 255),
    "poophi": (168, 116, 72, 255),
    "wood": (176, 120, 70, 255),
    # goose colors
    "goose": (250, 250, 246, 255),
    "gooseshade": (214, 220, 232, 255),
    "goosewing": (184, 192, 208, 255),
    "gooseorange": (248, 146, 42, 255),
    "gooseorangedk": (204, 96, 28, 255),
    "gosling": (246, 214, 96, 255),
    "goslinghi": (252, 236, 158, 255),
    "goslingdk": (214, 174, 58, 255),
    "slate": (92, 98, 114, 255),
    "gooseegg": (250, 248, 238, 255),
    "gooseeggshade": (226, 222, 204, 255),
    "straw": (236, 200, 120, 255),
    "strawdk": (196, 150, 74, 255),
    "bread": (226, 170, 96, 255),
    "breaddk": (180, 120, 60, 255),
    "metal": (176, 184, 200, 255),
    "rice": (250, 250, 244, 255),
    "salmon": (250, 140, 100, 255),
    "nori": (30, 52, 40, 255),
    "cone": (214, 152, 82, 255),
    "conedk": (170, 110, 54, 255),
    "icecream": (255, 176, 206, 255),
    "cream": (255, 240, 214, 255),
    "wizard": (90, 70, 190, 255),
    "wizarddk": (60, 44, 140, 255),
    "pirate": (40, 30, 26, 255),
    "pearl": (250, 246, 240, 255),
    "pearlsh": (214, 206, 220, 255),
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


class Out:
    """Where one pet's sprites get written, and a list of what was made (for the preview sheet)."""
    def __init__(self, folder):
        self.folder = folder
        self.made = []
        os.makedirs(folder, exist_ok=True)

    def save(self, c, name):
        c.image().save(os.path.join(self.folder, f"{name}.png"))
        self.made.append(name)

    def prop(self, name, draw, outline=True):
        """A 16x16 item, drawn into the corner of a canvas and cropped."""
        c = Canvas()
        draw(c)
        if outline:
            c.outline()
        c.image().crop((0, 0, 16, 16)).save(os.path.join(self.folder, f"{name}.png"))
        self.made.append(name)

    def sheet(self, path, scale=5, cols=8):
        cell = S * scale + 12
        rows = (len(self.made) + cols - 1) // cols
        sheet = Image.new("RGBA", (cols * cell, rows * (cell + 16)), (18, 20, 28, 255))
        d = ImageDraw.Draw(sheet)
        for i, n in enumerate(self.made):
            im = Image.open(os.path.join(self.folder, f"{n}.png"))
            im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
            x = (i % cols) * cell + 6
            y = (i // cols) * (cell + 16) + 6
            d.rectangle([x - 2, y - 2, x + S * scale + 1, y + S * scale + 1], fill=(40, 46, 70, 255))
            sheet.alpha_composite(im, (x, y))
            d.text((x, y + S * scale + 3), n, fill=(140, 255, 160, 255))
        sheet.save(path)


# ---------- effects drawn around a pet ----------

def z_px(c, x, y, n):
    for i in range(n):
        c.set(x + i, y, "blue")
        c.set(x + i, y + n - 1, "blue")
        c.set(x + n - 1 - i, y + i, "blue")


def heart_px(c, x, y, col="red"):
    for dx, dy in ((0, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1),
                   (0, 2), (1, 2), (2, 2), (1, 3)):
        c.set(x + dx, y + dy, col)


def sparkles(c, g, f):
    pts = [(3, 4), (28, 6), (2, 14)] if f == 0 else [(29, 3), (4, 8), (29, 14)]
    for (x, y) in pts:
        c.set(x, y, "yellow")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.set(x + dx, y + dy, "yellow")


def stink(c, g, f):
    for i, x in enumerate((2, 6, 25, 29)):
        off = (f + i) % 2
        for y in range(5, 10):
            c.set(x + ((y + off) % 2), y + (i % 2) * 2, "green")
    fx, fy = (24, 2) if f == 0 else (22, 1)
    c.set(fx, fy, "outline"); c.set(fx - 1, fy - 1, "shade"); c.set(fx + 1, fy - 1, "shade")


def bubbles(c, g, f):
    pts = [(3, 22), (6, 16), (26, 21), (28, 14), (3, 10), (27, 8)]
    for i, (x, y) in enumerate(pts):
        y -= f * (1 + i % 2)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            c.set(x + dx, y + dy, "blue")
        c.set(x, y, "white")
    for x in range(5, 27):
        c.set(x, 27 + (x + f) % 2, "blue")


def tint_face(c, bottom, from_colors):
    """Turns a sick pet's face a little green."""
    for (x, y), col in list(c.px.items()):
        if col in [PAL[k] for k in from_colors] and y < bottom:
            c.set(x, y, (208, 232, 184, 255))


# ---------- eggs ----------

EGG = (16, 21, 7.6, 9.4)


def in_egg(x, y, lean=0, grow=0):
    cx, cy, rx, ry = EGG
    x -= round((30 - y) * lean / 10)   # lean: tilt the top of the egg sideways
    return ((x + 0.5 - cx) / (rx + grow)) ** 2 + ((y + 0.5 - cy) / (ry + grow)) ** 2 <= 1


def cracks(c, level, shift=0):
    if level >= 1:
        for (x, y) in ((12, 19), (13, 20), (14, 19), (15, 20), (16, 21), (17, 20), (18, 21)):
            c.set(x + shift, y, "outline")
    if level >= 2:
        for (x, y) in ((9, 20), (10, 21), (11, 20), (19, 20), (20, 21), (21, 20), (22, 21), (16, 22), (16, 23), (15, 24)):
            c.set(x + shift, y, "outline")


def egg(level=0, cold=False, frame=0, colors=("eggshell", "eggshade"), specks=True, grow=0):
    c = Canvas()
    shell, shade = ("coldshell", "coldshade") if cold else colors
    lean = 0 if cold else (1 if frame else 0)
    shift = 1 if (cold and frame) else 0            # a cold egg shivers instead of wobbling
    for y in range(S):
        for x in range(S):
            if in_egg(x - shift, y, lean, grow):
                inner = in_egg(x - shift + 2, y + 1, lean, grow - 0.6)
                c.set(x, y, shell if inner else shade)
    if specks:
        for (x, y) in ((13, 15), (18, 17), (11, 23), (17, 25), (20, 22), (14, 27)):
            x += shift + (round((30 - y) * lean / 10))
            c.set(x, y, "speck")
    c.set(12 + shift + lean, 16, "white"); c.set(12 + shift + lean, 17, "white")
    cracks(c, level, shift + lean)
    if cold:
        for (x, y) in ((5, 12), (26, 9), (4, 22), (27, 19)):
            c.set(x, y, "white")
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c.set(x + dx, y + dy, "blue")
    c.outline()
    return c


def eggs(out, **kw):
    for level in range(3):
        for f in range(2):
            out.save(egg(level, frame=f, **kw), f"egg_{level}_{f + 1}")
            out.save(egg(level, cold=True, frame=f, **kw), f"egg_cold_{level}_{f + 1}")


def shell_bottom(c, top=23, colors=("eggshell", "eggshade"), grow=0.4):
    """The bottom half of a hatched egg, drawn over whatever is sitting in it."""
    shell = {}
    for y in range(S):
        for x in range(S):
            edge = top + (1 if x % 3 == 1 else -1 if x % 3 == 0 else 0)
            if y >= edge and in_egg(x, y, grow=grow):
                shell[(x, y)] = colors[1] if x > 19 else colors[0]
    for (x, y), col in shell.items():
        c.set(x, y, col)
    for (x, y) in shell:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in shell:
                c.set(x + dx, y + dy, "outline")


def flying_shell(c, color="eggshell"):
    """The top of the egg, popping off to the upper left."""
    for (x, y) in ((3, 4), (4, 3), (5, 3), (6, 3), (7, 4), (4, 4), (5, 4), (6, 4)):
        c.set(x, y, color)
    for (x, y) in ((3, 5), (2, 4), (4, 2), (5, 2), (6, 2), (7, 3), (8, 4), (8, 5), (7, 5), (6, 5), (5, 5), (4, 5)):
        if not c.get(x, y):
            c.set(x, y, "outline")


def hatch_start(out, **kw):
    c = egg(2, frame=1, **kw)
    for (x, y) in ((5, 8), (27, 10), (8, 4), (24, 5)):
        c.set(x, y, kw.get("colors", ("eggshell",))[0])
    cracks(c, 2, 1)
    out.save(c, "hatch_1")


# ---------- 16x16 items and particles ----------

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


def recolor_fish(c, body, dark):
    big_fish(c)
    for (x, y), col in list(c.px.items()):
        if col == PAL["fish"]:
            c.set(x, y, body)
        elif col == PAL["fishdk"]:
            c.set(x, y, dark)


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


def poop(c):
    for (y, x0, x1) in ((14, 3, 12), (13, 3, 12), (12, 4, 11), (11, 5, 10), (10, 5, 10), (9, 6, 9), (8, 7, 8)):
        for x in range(x0, x1 + 1):
            c.set(x, y, "poop")
    for (x, y) in ((6, 12), (7, 10), (8, 9), (5, 13)):
        c.set(x, y, "poophi")
    c.set(6, 11, "white"); c.set(9, 11, "white")
    c.set(7, 13, "eye"); c.set(8, 13, "eye")


def coin(c):
    c.ellipse(7.5, 7.5, 5.6, 5.6, "golddk")
    c.ellipse(7.5, 7.5, 4.4, 4.4, "gold")
    for y in range(5, 11):
        c.set(7, y, "golddk")
    c.set(5, 5, "white"); c.set(5, 6, "white")


def common_props(out):
    """Items and particles every pet uses."""
    out.prop("heart", lambda c: heart_px(c, 6, 6))
    out.prop("pill", pill)
    out.prop("moon", moon)
    out.prop("poop", poop)
    out.prop("bubble", bubble, outline=False)
    out.prop("sparkle", sparkle, outline=False)
    out.prop("coin", coin)
