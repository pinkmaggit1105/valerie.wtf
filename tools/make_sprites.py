"""Draws every pet's pixel-art sprites into sprites/<pet>/.

Usage: python3 tools/make_sprites.py [preview-folder]
Needs Pillow. With a preview folder it also writes a zoomed-in sheet of each pet's sprites there.
"""
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from pixels import Out
import sudo, puck

ROOT = os.path.join(os.path.dirname(__file__), "..", "sprites")

for name, pet in (("sudo", sudo), ("puck", puck)):
    out = Out(os.path.join(ROOT, name))
    pet.build(out)
    if len(sys.argv) > 1:
        out.sheet(os.path.join(sys.argv[1], f"{name}.png"))
    print(f"{name}: {len(out.made)} sprites")
