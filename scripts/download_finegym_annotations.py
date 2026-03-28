"""
Download FineGym annotation files or any list of URLs.
Usage examples:
  python download_finegym_annotations.py --out data/finegym_annotations --urls https://example.com/temporal_annotation.json
  python download_finegym_annotations.py --out data/finegym_annotations --manifest scripts/finegym_manifest.json

Manifest format (JSON): either a list of URLs or an object mapping filenames->urls.
"""
import argparse
import json
import os
import sys
from urllib.parse import urlparse

try:
    import requests
    from tqdm import tqdm
except ImportError:
    print("Missing dependencies. Run: pip install requests tqdm")
    sys.exit(1)


def download_url(url, out_path, chunk_size=1024):
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        with open(out_path, 'wb') as f, tqdm(total=total, unit='B', unit_scale=True, desc=os.path.basename(out_path)) as pbar:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))


def load_manifest(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # If manifest is a list, return list of (filename,url)
    entries = []
    if isinstance(data, list):
        for url in data:
            entries.append((None, url))
    elif isinstance(data, dict):
        for name, url in data.items():
            entries.append((name, url))
    else:
        raise ValueError('Manifest must be a list or dict')
    return entries


def main():
    p = argparse.ArgumentParser(description='Download FineGym annotation files')
    p.add_argument('--out', '-o', default='data/finegym_annotations', help='Output directory')
    p.add_argument('--urls', nargs='*', help='One or more URLs to download')
    p.add_argument('--manifest', help='Path to a JSON manifest (list of URLs or {name:url})')
    p.add_argument('--overwrite', action='store_true', help='Overwrite existing files')
    args = p.parse_args()

    entries = []
    if args.manifest:
        entries.extend(load_manifest(args.manifest))
    if args.urls:
        for url in args.urls:
            entries.append((None, url))

    if not entries:
        print('No URLs provided. Use --urls or --manifest')
        sys.exit(1)

    for name, url in entries:
        parsed = urlparse(url)
        filename = name or os.path.basename(parsed.path) or parsed.netloc
        out_path = os.path.join(args.out, filename)
        if os.path.exists(out_path) and not args.overwrite:
            print(f'Skipping existing: {out_path} (use --overwrite to replace)')
            continue
        try:
            print(f'Downloading {url} -> {out_path}')
            download_url(url, out_path)
        except Exception as e:
            print(f'Failed to download {url}: {e}')


if __name__ == '__main__':
    main()
