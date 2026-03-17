#!/usr/bin/env python3
"""Print categorised ASN labels for Paperless-ngx on Brother QL-820NWB (17x54mm)

Categories:
    CF = Company (Fyzi)
    P  = Personal
    T  = Tax
    F  = Finance
    H  = Property/Home

Usage:
    python3 print-asn-labels.py CF 1 50       # Print CF-00001 to CF-00050
    python3 print-asn-labels.py T 1           # Print just T-00001
    python3 print-asn-labels.py P 1 20 --dry  # Generate PNGs only, no print
"""
from __future__ import annotations
import sys
import os
import subprocess
import qrcode
from PIL import Image, ImageDraw, ImageFont

PRINTER = "Brother_QL820NWB"
WIDTH = 638   # 54mm at 300 DPI
HEIGHT = 200  # 17mm at 300 DPI
OUTPUT_DIR = "/tmp/asn_labels"

CATEGORIES = {
    "CF":  "Company (Fyzi Ltd)",
    "CH":  "Company (Holme Property)",
    "P":   "Personal",
    "T":   "Tax",
    "FAR": "Farming",
    "FIN": "Finance",
    "H":   "Home",
}

def create_label(prefix: str, num: int) -> str:
    code = f"{prefix}-{num:05d}"
    cat_name = CATEGORIES.get(prefix, prefix)

    label = Image.new('RGB', (WIDTH, HEIGHT), 'white')
    draw = ImageDraw.Draw(label)

    # QR code
    qr = qrcode.QRCode(version=1, box_size=8, border=1)
    qr.add_data(code)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color='black', back_color='white')
    qr_img = qr_img.resize((170, 170))
    label.paste(qr_img, (15, 15))

    # Text
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56)
        font_med = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 44)
    except Exception:
        font_large = ImageFont.load_default()
        font_med = ImageFont.load_default()

    draw.text((200, 10), code, fill='black', font=font_large)
    draw.text((200, 70), cat_name, fill='black', font=font_med)

    path = os.path.join(OUTPUT_DIR, f"{code}.png")
    label.save(path)
    return path

def print_label(path: str) -> None:
    subprocess.run([
        "lp", "-d", PRINTER,
        "-o", "PageSize=17x54mm",
        "-o", "MediaType=Labels",
        "-o", "orientation-requested=3",
        "-o", "fit-to-page",
        path
    ], check=True)

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print(f"\nAvailable categories: {', '.join(f'{k} ({v})' for k, v in CATEGORIES.items())}")
        sys.exit(1)

    prefix = sys.argv[1].upper()
    if prefix not in CATEGORIES:
        print(f"Unknown category '{prefix}'. Available: {', '.join(CATEGORIES.keys())}")
        sys.exit(1)

    start = int(sys.argv[2])
    end = start
    if len(sys.argv) > 3 and not sys.argv[3].startswith('-'):
        end = int(sys.argv[3])
    dry_run = '--dry' in sys.argv

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = end - start + 1
    print(f"{'Generating' if dry_run else 'Printing'} {total} label(s): {prefix}-{start:05d} to {prefix}-{end:05d}")
    print(f"Category: {CATEGORIES[prefix]}")

    for i in range(start, end + 1):
        path = create_label(prefix, i)
        if dry_run:
            print(f"  Generated: {path}")
        else:
            print_label(path)
            print(f"  Printed: {prefix}-{i:05d}")

    print(f"\nDone! {total} label(s) {'generated' if dry_run else 'printed'}.")
    if dry_run:
        print(f"PNGs saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
