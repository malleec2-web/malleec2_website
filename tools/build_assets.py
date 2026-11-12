#!/usr/bin/env python3
"""Turn the designer's source files in "WEBSITE ASSETS/" into web-ready files in assets/.

The source folder is large and is not committed. Re-run this script whenever the
designer supplies updated files:

    python3 -m venv .venv && .venv/bin/pip install fonttools brotli pillow
    .venv/bin/python tools/build_assets.py

It also needs `pdftocairo` (from poppler) on the PATH; the .ai files are PDF-compatible.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from fontTools import subset
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "WEBSITE ASSETS"
OUT = ROOT / "assets"

FONT_WEIGHTS = {"Regular": 400, "Medium": 500, "Bold": 700, "ExtraBold": 800}
# Basic Latin, Latin-1, general punctuation (dashes, curly quotes, ellipsis), euro, trademark.
FONT_UNICODES = "U+0000-00FF,U+0131,U+0152-0153,U+2013-2014,U+2018-201E,U+2022,U+2026,U+20AC,U+2122"

BANNERS = ["HOME", "CAPABILITY", "APPROACH", "ABOUT", "BANNER", "PARTNERS"]
BANNER_WIDTHS = [2400, 1600, 1000]

VECTORS = {
    "LOGOS/VECTOR/Mallee C2 REV_RGB.ai": "mallee-c2-logo.svg",
    "LOGOS/VECTOR/DELL PARTNER LOGO_RGB.ai": "dell-partner.svg",
    "LOGOS/VECTOR/MS PARTNER LOGO_RGB.ai": "microsoft-partner.svg",
    "DEVICE/VECTOR/DEVICE_LIME_RGB.ai": "device-lime.svg",
}


def build_fonts() -> None:
    dest = OUT / "fonts"
    dest.mkdir(parents=True, exist_ok=True)
    for name in FONT_WEIGHTS:
        src = SRC / "FONT" / f"DMSans-{name}.ttf"
        target = dest / f"dmsans-{name.lower()}.woff2"
        subset.main([
            str(src),
            f"--unicodes={FONT_UNICODES}",
            "--layout-features=kern,liga,calt,ccmp,locl,mark,mkmk",
            "--flavor=woff2",
            f"--output-file={target}",
        ])
        print("font", target.relative_to(ROOT), target.stat().st_size // 1024, "KB")


def build_banners() -> None:
    dest = OUT / "img"
    dest.mkdir(parents=True, exist_ok=True)
    for name in BANNERS:
        src = Image.open(SRC / "IMAGERY" / f"{name}_2400x654px.jpg").convert("RGB")
        for width in BANNER_WIDTHS:
            height = round(src.height * width / src.width)
            img = src if width == src.width else src.resize((width, height), Image.LANCZOS)
            target = dest / f"{name.lower()}-{width}.webp"
            img.save(target, "WEBP", quality=72, method=6)
            print("img ", target.relative_to(ROOT), target.stat().st_size // 1024, "KB")


def build_vectors() -> None:
    dest = OUT / "img"
    dest.mkdir(parents=True, exist_ok=True)
    for src, name in VECTORS.items():
        target = dest / name
        subprocess.run(["pdftocairo", "-svg", str(SRC / src), str(target)], check=True)
        print("svg ", target.relative_to(ROOT), target.stat().st_size // 1024, "KB")


def build_social_image() -> None:
    """1200x630 share image: the home banner centred on the brand dark green."""
    src = Image.open(SRC / "IMAGERY" / "HOME_2400x654px.jpg").convert("RGB")
    banner = src.resize((1200, round(src.height * 1200 / src.width)), Image.LANCZOS)
    canvas = Image.new("RGB", (1200, 630), (0x17, 0x40, 0x31))
    logo = Image.open(SRC / "LOGOS" / "PNG" / "Mallee-C2-REV_RGB.png").convert("RGBA")
    logo = logo.resize((logo.width * 2, logo.height * 2), Image.LANCZOS)
    canvas.paste(banner, (0, 630 - banner.height))
    canvas.paste(logo, (60, (630 - banner.height - logo.height) // 2), logo)
    target = OUT / "img" / "social-share.jpg"
    canvas.save(target, "JPEG", quality=82, optimize=True, progressive=True)
    print("og  ", target.relative_to(ROOT), target.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    if not SRC.is_dir():
        raise SystemExit(f"Source folder not found: {SRC}")
    shutil.rmtree(OUT / "fonts", ignore_errors=True)
    build_fonts()
    build_banners()
    build_vectors()
    build_social_image()
