#!/usr/bin/env python3
"""
FineGym downloader helper

Usage examples:
  python scripts/finegym_downloader.py --download-annotations https://raw.githubusercontent.com/.../temporal_annotation_v1.1.json --out data
  python scripts/finegym_downloader.py --download-videos --annotations data/temporal_annotation_v1.1.json --out data

Notes:
 - Requires `yt-dlp` on PATH to download videos by YouTube id.
 - This script only automates downloads given URLs or local annotation files.
"""
import argparse
import json
import os
import sys
from pathlib import Path
import requests
import subprocess
from tqdm import tqdm


def download_file(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url} -> {dest}")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def extract_video_ids_from_annotation(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data.keys())


def download_videos_by_ids(video_ids, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    for vid in tqdm(video_ids, desc="videos"):
        out_template = str(out_dir / f"{vid}.%(ext)s")
        cmd = ["yt-dlp", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best", f"https://youtu.be/{vid}", "-o", out_template]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"yt-dlp failed for {vid}: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download-annotations", nargs="*", help="URLs of annotation files to download")
    parser.add_argument("--annotations", help="Local annotation JSON file to read video ids from")
    parser.add_argument("--download-videos", action="store_true", help="Download videos referenced by annotation file (requires yt-dlp)")
    parser.add_argument("--out", default="data", help="Output base directory")
    args = parser.parse_args()

    out = Path(args.out)
    if args.download_annotations:
        for url in args.download_annotations:
            fname = url.rstrip("/\n").split("/")[-1]
            dest = out / "annotations" / fname
            download_file(url, dest)

    if args.download_videos:
        ann = args.annotations
        if not ann:
            print("--annotations is required when using --download-videos")
            sys.exit(1)
        ann_path = Path(ann)
        if not ann_path.exists():
            print(f"Annotation file not found: {ann_path}")
            sys.exit(1)
        vids = extract_video_ids_from_annotation(ann_path)
        download_videos_by_ids(vids, out / "videos")


if __name__ == "__main__":
    main()
