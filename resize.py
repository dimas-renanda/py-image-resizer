#!/usr/bin/env python3
"""Batch image resizer using Pillow."""
import sys, argparse
from pathlib import Path

def resize(path, width, height, quality, suffix):
    try:
        from PIL import Image
    except ImportError:
        print("Install Pillow: pip install Pillow"); sys.exit(1)
    img = Image.open(path)
    orig = img.size
    if width and height:
        img = img.resize((width, height), Image.LANCZOS)
    elif width:
        ratio = width / img.width
        img = img.resize((width, int(img.height * ratio)), Image.LANCZOS)
    elif height:
        ratio = height / img.height
        img = img.resize((int(img.width * ratio), height), Image.LANCZOS)
    out = path.parent / f"{path.stem}{suffix}{path.suffix}"
    img.save(out, quality=quality, optimize=True)
    print(f"  {path.name}: {orig} → {img.size} → {out.name}")

p = argparse.ArgumentParser()
p.add_argument("files", nargs="+")
p.add_argument("--width","-W",type=int)
p.add_argument("--height","-H",type=int)
p.add_argument("--quality","-q",type=int,default=85)
p.add_argument("--suffix","-s",default="_resized")
args = p.parse_args()

if not args.width and not args.height: print("Specify --width and/or --height"); sys.exit(1)
for f in args.files: resize(Path(f), args.width, args.height, args.quality, args.suffix)
print("Done!")
