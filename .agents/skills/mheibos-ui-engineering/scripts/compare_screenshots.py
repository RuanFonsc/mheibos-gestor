#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image, ImageChops


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("current", type=Path)
    parser.add_argument("--diff", type=Path)
    parser.add_argument("--threshold", type=float, default=0.01)
    args = parser.parse_args()
    baseline = Image.open(args.baseline).convert("RGBA")
    current = Image.open(args.current).convert("RGBA")
    if baseline.size != current.size:
        print(f"FAIL: geometria {baseline.size} != {current.size}")
        return 1
    diff = ImageChops.difference(baseline, current)
    changed = sum(1 for pixel in diff.getdata() if pixel != (0, 0, 0, 0))
    ratio = changed / (baseline.width * baseline.height)
    if args.diff:
        diff.save(args.diff)
    print(f"changed_ratio={ratio:.6f}")
    return 1 if ratio > args.threshold else 0


if __name__ == "__main__":
    raise SystemExit(main())
