"""
extract_frames.py
For each video file in the input directory (recursive), extracts N frames at
percentages of total duration (default 25%, 50%, 75%) using ffmpeg.

Usage:
    python extract_frames.py <videos_dir> <out_dir> [--percents 25,50,75] [--ffmpeg <path>]
"""
import os
import sys
import argparse
import subprocess
import json


VIDEO_EXTS = (".mp4", ".mov", ".avi", ".mkv", ".webm")


def ffprobe_duration(ffprobe, path):
    cmd = [ffprobe, "-v", "error", "-show_entries", "format=duration",
           "-of", "json", path]
    out = subprocess.check_output(cmd)
    data = json.loads(out.decode("utf-8", errors="ignore"))
    return float(data["format"]["duration"])


def extract_frame(ffmpeg, video, t_sec, out_path):
    cmd = [ffmpeg, "-y", "-ss", f"{t_sec:.2f}", "-i", video,
           "-frames:v", "1", "-q:v", "2", out_path]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--percents", default="25,50,75")
    ap.add_argument("--ffmpeg", default=r"C:\Program Files\ImageMagick-7.0.10-Q16-HDRI\ffmpeg.exe")
    ap.add_argument("--ffprobe", default=None,
                    help="Path to ffprobe; defaults to sibling of ffmpeg")
    args = ap.parse_args()

    ffmpeg = args.ffmpeg
    ffprobe = args.ffprobe or os.path.join(os.path.dirname(ffmpeg), "ffprobe.exe")
    percents = [float(p) / 100.0 for p in args.percents.split(",")]
    os.makedirs(args.out_dir, exist_ok=True)

    videos = []
    for root, _, files in os.walk(args.videos_dir):
        for f in files:
            if f.lower().endswith(VIDEO_EXTS):
                videos.append(os.path.join(root, f))

    print(f"Found {len(videos)} videos")
    for v in videos:
        name = os.path.splitext(os.path.basename(v))[0]
        try:
            dur = ffprobe_duration(ffprobe, v)
        except Exception as e:
            print(f"  [SKIP] {name}: probe failed: {e}")
            continue
        for i, p in enumerate(percents):
            t = dur * p
            out = os.path.join(args.out_dir, f"{name}_p{int(p*100)}.jpg")
            try:
                extract_frame(ffmpeg, v, t, out)
                print(f"  [OK] {name} @ {t:.1f}s -> {os.path.basename(out)}")
            except Exception as e:
                print(f"  [FAIL] {name} @ {t:.1f}s: {e}")


if __name__ == "__main__":
    main()
