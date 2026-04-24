"""
make_responsive.py
For each image in the input directory, produces 3 responsive widths
(480, 768, 1200) in both WebP (q=85) and JPG (q=82) formats.

Uses ImageMagick's `magick` command for high-quality resizing + encoding.

Usage:
    python make_responsive.py <input_dir> <out_dir> [--magick <path>]

Naming:
    Input file "hero-rima.jpg" -> "hero-rima-480.webp", "hero-rima-480.jpg",
                                   "hero-rima-768.webp", "hero-rima-768.jpg",
                                   "hero-rima-1200.webp", "hero-rima-1200.jpg"
"""
import os
import sys
import argparse
import subprocess

WIDTHS = [480, 768, 1200]
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--magick", default=r"C:\Program Files\ImageMagick-7.0.10-Q16-HDRI\magick.exe")
    ap.add_argument("--webp-q", type=int, default=85)
    ap.add_argument("--jpg-q", type=int, default=82)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    for name in sorted(os.listdir(args.input_dir)):
        if not name.lower().endswith(IMG_EXTS):
            continue
        base = os.path.splitext(name)[0]
        ip = os.path.join(args.input_dir, name)
        for w in WIDTHS:
            webp = os.path.join(args.out_dir, f"{base}-{w}.webp")
            jpg = os.path.join(args.out_dir, f"{base}-{w}.jpg")
            # Resize preserving aspect; only downscale (>)
            try:
                run([args.magick, ip, "-auto-orient", "-strip",
                     "-resize", f"{w}x>", "-quality", str(args.webp_q), webp])
                run([args.magick, ip, "-auto-orient", "-strip",
                     "-resize", f"{w}x>", "-quality", str(args.jpg_q),
                     "-sampling-factor", "4:2:0", "-interlace", "JPEG", jpg])
                sz_w = os.path.getsize(webp) // 1024
                sz_j = os.path.getsize(jpg) // 1024
                print(f"  [OK] {base} {w}w -> webp {sz_w}KB, jpg {sz_j}KB")
            except Exception as e:
                print(f"  [FAIL] {base} {w}w: {e}")


if __name__ == "__main__":
    main()
