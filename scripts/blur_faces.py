"""
blur_faces.py
Detects faces in images and applies mosaic/pixelate anonymization over each
detected face EXCEPT Rima's — Rima is never blurred.

Two modes:
  1. Identity mode (preferred): uses `face_recognition` (dlib) to load Rima's
     face encoding once from a reference portrait, then skips any detected
     face whose encoding matches Rima.
  2. Protect-zone fallback: if `face_recognition` is unavailable, reads a JSON
     file `rima_zones.json` (keys = source filenames, values = list of
     [x_frac, y_frac, w_frac, h_frac] rectangles in 0..1 coords). Any Haar
     detection whose center lands inside any zone is skipped.

Usage:
    python blur_faces.py <input_path_or_dir> <output_dir> \\
        [--rima-portrait <path>] [--zones <json>] [--pixel-size 18] [--margin 0.15]

Install for identity mode (optional):
    pip install face_recognition
"""
import os
import sys
import json
import argparse
import cv2
import numpy as np

HAAR_FRONTAL = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
HAAR_PROFILE = cv2.data.haarcascades + "haarcascade_profileface.xml"

IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

# Try to import face_recognition; fall back to zone mode if unavailable.
try:
    import face_recognition  # type: ignore
    HAS_FACE_REC = True
except Exception as _e:
    HAS_FACE_REC = False


def pixelate_region(img, x, y, w, h, pixel_size=18):
    H, W = img.shape[:2]
    x = max(0, x); y = max(0, y)
    x2 = min(W, x + w); y2 = min(H, y + h)
    if x2 <= x or y2 <= y:
        return
    roi = img[y:y2, x:x2]
    rh, rw = roi.shape[:2]
    nx = max(1, rw // pixel_size)
    ny = max(1, rh // pixel_size)
    small = cv2.resize(roi, (nx, ny), interpolation=cv2.INTER_LINEAR)
    mosaic = cv2.resize(small, (rw, rh), interpolation=cv2.INTER_NEAREST)
    img[y:y2, x:x2] = mosaic


def detect_faces_haar(gray, cascade_path, scale=1.1, neighbors=4, min_size=30):
    c = cv2.CascadeClassifier(cascade_path)
    return c.detectMultiScale(gray, scaleFactor=scale, minNeighbors=neighbors,
                              minSize=(min_size, min_size))


def merge_boxes(boxes, iou_thresh=0.2):
    result = []
    for b in boxes:
        x, y, w, h = b
        merged = False
        for i, r in enumerate(result):
            rx, ry, rw, rh = r
            xa, ya = max(x, rx), max(y, ry)
            xb, yb = min(x + w, rx + rw), min(y + h, ry + rh)
            inter = max(0, xb - xa) * max(0, yb - ya)
            ua = w * h + rw * rh - inter
            if ua > 0 and inter / ua >= iou_thresh:
                nx, ny = min(x, rx), min(y, ry)
                nx2, ny2 = max(x + w, rx + rw), max(y + h, ry + rh)
                result[i] = (nx, ny, nx2 - nx, ny2 - ny)
                merged = True
                break
        if not merged:
            result.append((x, y, w, h))
    return result


def load_rima_encoding(portrait_path):
    """Return a single 128-d face encoding for Rima, or None."""
    if not HAS_FACE_REC or not portrait_path or not os.path.exists(portrait_path):
        return None
    img = face_recognition.load_image_file(portrait_path)
    encs = face_recognition.face_encodings(img)
    if not encs:
        print(f"  [WARN] no face found in portrait: {portrait_path}")
        return None
    return encs[0]


def is_rima_by_encoding(rgb_img, box, rima_enc, tolerance=0.55):
    """box is (x,y,w,h) in pixels. Returns True if face matches Rima."""
    if rima_enc is None:
        return False
    x, y, w, h = box
    # face_recognition uses (top, right, bottom, left)
    top, right, bottom, left = y, x + w, y + h, x
    H, W = rgb_img.shape[:2]
    top = max(0, top); left = max(0, left)
    bottom = min(H, bottom); right = min(W, right)
    if bottom <= top or right <= left:
        return False
    try:
        encs = face_recognition.face_encodings(rgb_img, known_face_locations=[(top, right, bottom, left)])
    except Exception:
        return False
    if not encs:
        return False
    dist = np.linalg.norm(encs[0] - rima_enc)
    return dist <= tolerance


def is_rima_by_zone(box, img_shape, zones):
    """zones is list of [xf, yf, wf, hf]. Returns True if box center inside any zone."""
    if not zones:
        return False
    x, y, w, h = box
    cx, cy = x + w / 2.0, y + h / 2.0
    H, W = img_shape[:2]
    cxf, cyf = cx / W, cy / H
    for (zx, zy, zw, zh) in zones:
        if zx <= cxf <= zx + zw and zy <= cyf <= zy + zh:
            return True
    return False


def process_image(in_path, out_path, rima_enc=None, zones_for_file=None,
                  pixel_size=18, margin=0.20):
    img = cv2.imread(in_path)
    if img is None:
        print(f"  [SKIP] cannot read: {in_path}")
        return 0, 0
    H, W = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    min_face = max(30, min(H, W) // 25)
    all_faces = []
    for path in (HAAR_FRONTAL, HAAR_PROFILE):
        faces = detect_faces_haar(gray, path, scale=1.08, neighbors=4, min_size=min_face)
        for f in faces:
            all_faces.append(tuple(int(v) for v in f))
    flipped = cv2.flip(gray, 1)
    for f in detect_faces_haar(flipped, HAAR_PROFILE, scale=1.08, neighbors=4, min_size=min_face):
        x, y, w, h = [int(v) for v in f]
        all_faces.append((W - x - w, y, w, h))
    merged = merge_boxes(all_faces, iou_thresh=0.2)

    blurred = 0
    skipped_rima = 0
    for box in merged:
        is_rima = False
        if rima_enc is not None:
            is_rima = is_rima_by_encoding(rgb, box, rima_enc)
        if not is_rima and zones_for_file:
            is_rima = is_rima_by_zone(box, img.shape, zones_for_file)
        if is_rima:
            skipped_rima += 1
            continue
        x, y, w, h = box
        mx = int(w * margin); my = int(h * margin)
        pixelate_region(img, x - mx, y - my, w + 2 * mx, h + 2 * my, pixel_size=pixel_size)
        blurred += 1

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cv2.imwrite(out_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
    print(f"  [OK] {os.path.basename(in_path)} -> {blurred} blurred, {skipped_rima} Rima-skipped")
    return blurred, skipped_rima


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output_dir")
    ap.add_argument("--rima-portrait", default=None,
                    help="Path to a clean Rima portrait (for identity mode)")
    ap.add_argument("--zones", default=None,
                    help="Path to rima_zones.json (fallback mode)")
    ap.add_argument("--pixel-size", type=int, default=18)
    ap.add_argument("--margin", type=float, default=0.20)
    args = ap.parse_args()

    rima_enc = load_rima_encoding(args.rima_portrait) if args.rima_portrait else None
    if args.rima_portrait and rima_enc is None and not HAS_FACE_REC:
        print("  [INFO] face_recognition not installed — using zone fallback only.")
    if rima_enc is not None:
        print("  [INFO] Rima identity loaded — using face_recognition mode.")

    zones_by_file = {}
    if args.zones and os.path.exists(args.zones):
        with open(args.zones, "r", encoding="utf-8") as fh:
            zones_by_file = json.load(fh)
        print(f"  [INFO] loaded zones for {len(zones_by_file)} file(s)")

    os.makedirs(args.output_dir, exist_ok=True)
    if os.path.isdir(args.input):
        total_b = total_s = 0
        for name in sorted(os.listdir(args.input)):
            if name.lower().endswith(IMG_EXTS):
                ip = os.path.join(args.input, name)
                op = os.path.join(args.output_dir, name)
                zones = zones_by_file.get(name) or zones_by_file.get(os.path.splitext(name)[0])
                b, s = process_image(ip, op, rima_enc, zones, args.pixel_size, args.margin)
                total_b += b; total_s += s
        print(f"Done. Faces blurred: {total_b}. Rima-skipped: {total_s}.")
    else:
        name = os.path.basename(args.input)
        op = os.path.join(args.output_dir, name)
        zones = zones_by_file.get(name) or zones_by_file.get(os.path.splitext(name)[0])
        process_image(args.input, op, rima_enc, zones, args.pixel_size, args.margin)


if __name__ == "__main__":
    main()
