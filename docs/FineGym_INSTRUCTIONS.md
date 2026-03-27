FineGym integration notes

1) License
- FineGym annotations are published under CC BY-NC 4.0. Do not use commercially without permission.

2) Useful files to download from the FineGym page
- question annotation (json)
- set-level category list (txt)
- Gym99/Gym288/Gym530 category lists (txt)
- temporal annotation (json) (v1.0 / v1.1)
- pre-extracted features (optional)

3) Quick steps
- Download temporal annotation JSON (v1.1 recommended) to `data/annotations/`
- Generate parsed CSV: 
  ```
  python scripts/parse_temporal_annotations.py data/annotations/temporal_annotation_v1.1.json -o data/annotations/parsed.csv
  ```
- Download videos (requires `yt-dlp`):
  ```
  python scripts/finegym_downloader.py --download-videos --annotations data/annotations/temporal_annotation_v1.1.json --out data
  ```
- Extract clips using `ffmpeg`, or extract frames at N fps for training.

4) Notes on pre-extracted features
- The authors release pre-extracted features which speed up training. If you only want to train classifiers on top, prefer using those.

5) Next steps you can ask me to implement
- Clip extraction (`ffmpeg`) helper
- Minimal training loop example using pre-extracted features
- Minimal Flask inference server
