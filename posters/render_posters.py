#!/usr/bin/env python3
"""
Render SVG poster templates by replacing {{PLACEHOLDER}} tokens using values
from a JSON data file. Supports embedding images for keys like PHOTO by
converting local file paths to data URIs.

Usage:
  python3 render_posters.py --data sample-data.json --outdir build

Notes:
- Scans the directory of this script for .svg templates by default.
- Placeholders are case-sensitive and must be wrapped in double braces, e.g., {{TITLE}}.
- If a placeholder value points to an existing local image file (e.g., for PHOTO),
  it will be embedded as a data URI.
"""
import argparse
import base64
import json
import mimetypes
import os
import re
import sys
from pathlib import Path

PLACEHOLDER_PATTERN = re.compile(r"\{\{([A-Z0-9_\-]+)\}\}")
IMAGE_KEYS = {"PHOTO", "IMAGE", "IMG", "BACKGROUND_IMAGE"}


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(content)


def to_data_uri(file_path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(file_path))
    if not mime:
        # Fallback by extension
        ext = file_path.suffix.lower()
        if ext == ".svg":
            mime = "image/svg+xml"
        elif ext in {".jpg", ".jpeg"}:
            mime = "image/jpeg"
        elif ext == ".png":
            mime = "image/png"
        elif ext == ".webp":
            mime = "image/webp"
        else:
            mime = "application/octet-stream"
    data = file_path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def replace_placeholders(svg_text: str, values: dict, base_dir: Path) -> str:
    def replacement(match: re.Match) -> str:
        key = match.group(1)
        if key not in values:
            return match.group(0)  # keep original token if missing
        val = values[key]
        if not isinstance(val, str):
            val = str(val)
        # Image embedding if key suggests an image and file exists
        if key in IMAGE_KEYS and val:
            candidate = (base_dir / val) if not os.path.isabs(val) else Path(val)
            if candidate.exists() and candidate.is_file():
                try:
                    return to_data_uri(candidate)
                except Exception:
                    return val  # fallback to raw string
        return val

    return PLACEHOLDER_PATTERN.sub(replacement, svg_text)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render SVG poster templates with JSON data")
    parser.add_argument("--data", required=True, help="Path to JSON file with placeholder values")
    parser.add_argument("--outdir", required=True, help="Output directory for rendered SVG files")
    parser.add_argument(
        "--in-dir",
        default=str(Path(__file__).resolve().parent),
        help="Directory containing .svg templates (default: script directory)",
    )
    args = parser.parse_args(argv)

    data_path = Path(args.data).expanduser().resolve()
    out_dir = Path(args.outdir).expanduser().resolve()
    in_dir = Path(args.in_dir).expanduser().resolve()

    if not data_path.exists():
        print(f"[ERROR] Data file not found: {data_path}", file=sys.stderr)
        return 1

    try:
        values = json.loads(read_text(data_path))
    except Exception as exc:
        print(f"[ERROR] Failed to parse JSON: {exc}", file=sys.stderr)
        return 1

    svg_files = sorted(p for p in in_dir.glob("*.svg"))
    if not svg_files:
        print(f"[WARN] No SVG templates found in {in_dir}")

    for svg_file in svg_files:
        try:
            original = read_text(svg_file)
            rendered = replace_placeholders(original, values, base_dir=in_dir)
            out_path = out_dir / svg_file.name
            write_text(out_path, rendered)
            print(f"[OK] Rendered: {svg_file.name} -> {out_path}")
        except Exception as exc:
            print(f"[ERROR] Failed to render {svg_file.name}: {exc}", file=sys.stderr)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))