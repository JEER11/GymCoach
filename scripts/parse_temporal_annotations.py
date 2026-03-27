#!/usr/bin/env python3
"""
Parse FineGym temporal annotation JSON into a CSV of segments.

Output columns:
video_id,event_instance_id,event_label,event_start,event_end,subaction_id,subaction_label,subaction_start,subaction_end

Usage:
  python scripts/parse_temporal_annotations.py data/annotations/temporal_annotation_v1.1.json -o data/annotations/parsed.csv
"""
import argparse
import json
import csv
from pathlib import Path


def parse_annotation(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    # Top-level keys are video ids
    for vid, vid_info in data.items():
        for event_instance, event_data in vid_info.items():
            event_label = event_data.get("event")
            event_timestamps = event_data.get("timestamps", [])
            segments = event_data.get("segments", {})
            # iterate over subactions
            for sub_id, sub_data in segments.items():
                sub_label = sub_id  # in FineGym segments keys are codes like A_0003_0005
                sub_timestamps = sub_data.get("timestamps", [])
                # produce rows for each subaction timestamp (may have multiple stages)
                for s in sub_timestamps:
                    # s is [start, end] or list of stages; flatten to start/end if possible
                    if isinstance(s[0], (int, float)) and isinstance(s[1], (int, float)):
                        rows.append({
                            "video_id": vid,
                            "event_instance_id": event_instance,
                            "event_label": event_label,
                            "event_start": event_timestamps[0][0] if event_timestamps else "",
                            "event_end": event_timestamps[0][1] if event_timestamps else "",
                            "subaction_id": sub_id,
                            "subaction_label": sub_label,
                            "subaction_start": s[0],
                            "subaction_end": s[1],
                        })
                    else:
                        # nested stages: each entry is a stage timestamp
                        # join stages into one interval spanning min(start) to max(end)
                        starts = [t[0] for t in s if isinstance(t, (list, tuple))]
                        ends = [t[1] for t in s if isinstance(t, (list, tuple))]
                        if starts and ends:
                            rows.append({
                                "video_id": vid,
                                "event_instance_id": event_instance,
                                "event_label": event_label,
                                "event_start": event_timestamps[0][0] if event_timestamps else "",
                                "event_end": event_timestamps[0][1] if event_timestamps else "",
                                "subaction_id": sub_id,
                                "subaction_label": sub_label,
                                "subaction_start": min(starts),
                                "subaction_end": max(ends),
                            })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("annotation", help="Path to temporal annotation JSON")
    parser.add_argument("-o", "--out", default=None, help="Output CSV path")
    args = parser.parse_args()

    ann = Path(args.annotation)
    rows = parse_annotation(ann)
    out = Path(args.out) if args.out else ann.parent / (ann.stem + "_parsed.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["video_id","event_instance_id","event_label","event_start","event_end","subaction_id","subaction_label","subaction_start","subaction_end"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
