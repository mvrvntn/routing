#!/usr/bin/env python3
"""
Generate QR codes for importing geoasset URLs into v2RayNG.

Two QR codes are produced — one for geoip.dat and one for geosite.dat.
Users can scan these in v2RayNG -> Settings -> Geoasset update.

By default, the script uses branch-based jsdelivr CDN URLs.
You can also pass `--source releases` to use the GitHub Releases URLs.
"""

import argparse
import os
import sys

CDN_URLS = {
    "geoip.dat": "https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/geoip.dat",
    "geosite.dat": "https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/geosite.dat",
}

RELEASES_URLS = {
    "geoip.dat": "https://github.com/mvrvntn/routing/releases/latest/download/geoip.dat",
    "geosite.dat": "https://github.com/mvrvntn/routing/releases/latest/download/geosite.dat",
}


def get_urls(source: str) -> dict:
    """Return geoasset URLs based on the chosen source."""
    if source == "releases":
        return dict(RELEASES_URLS)
    return dict(CDN_URLS)


def generate_qr(data: str, output_path: str) -> bool:
    """Generate a QR code PNG from a string."""
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        return True
    except ImportError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate QR codes for v2RayNG geoasset URLs."
    )
    parser.add_argument(
        "--source",
        choices=["cdn", "releases"],
        default="cdn",
        help=(
            "'cdn' — jsdelivr CDN URLs (default). "
            "'releases' — GitHub Releases URLs."
        ),
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        default=".",
        help="Directory to save QR code images (default: current dir).",
    )
    args = parser.parse_args()

    urls = get_urls(args.source)
    os.makedirs(args.output_dir, exist_ok=True)

    has_qr = False
    for filename, url in urls.items():
        out_path = os.path.join(args.output_dir, f"{filename}.png")
        saved = generate_qr(url, out_path)
        if saved:
            has_qr = True
            print(f"[+] {filename} QR: {os.path.abspath(out_path)}")
        print(f"    URL ({filename}): {url}")

    if not has_qr:
        print("\n[!] 'qrcode' package is not installed (pip install qrcode[pil]). QR images were not saved.")

    print()
    print(
        "Scan these QR codes (or enter the URLs) in v2RayNG -> Settings -> Geoasset update\n"
        "to configure automated geoasset downloads."
    )


if __name__ == "__main__":
    main()
