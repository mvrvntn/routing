#!/usr/bin/env python3
"""
Generate a v2RayNG custom routing rules QR code and JSON from routing config.

Fetches or reads HAPP/DEFAULT.JSON, converts it to v2RayNG custom routing-rules
format, generates a QR code image if qrcode is installed, and prints JSON.
"""

import argparse
import json
import os
import sys
import urllib.request

DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "HAPP",
    "DEFAULT.JSON",
)
DEFAULT_CONFIG_URL = "https://raw.githubusercontent.com/mvrvntn/routing/main/HAPP/DEFAULT.JSON"

OUTBOUND_MAP = {
    "Block": "block",
    "Proxy": "proxy",
    "Direct": "direct",
}

REMARKS_MAP = {
    "Block": "BLOCK (Ads & Tracking)",
    "Proxy": "PROXY (VPN Required)",
    "Direct": "DIRECT (Russia & LAN)",
}


def load_config(source: str) -> dict:
    """Load config from a local file path or remote URL."""
    if source.startswith("http://") or source.startswith("https://"):
        print(f"[*] Fetching config from {source} ...")
        req = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    else:
        print(f"[*] Reading config from {source} ...")
        with open(source, "r", encoding="utf-8") as f:
            return json.load(f)


def convert_to_v2rayng_rules(config: dict) -> list[dict]:
    """Convert HAPP config to v2RayNG custom routing rules JSON."""
    rules = []
    idx = 1
    for group in ("Block", "Proxy", "Direct"):
        sites = config.get(f"{group}Sites", [])
        ips = config.get(f"{group}Ip", [])
        if not sites and not ips:
            continue
        rule: dict = {
            "remarks": f"{idx}. {REMARKS_MAP.get(group, group)}",
            "outboundTag": OUTBOUND_MAP.get(group, group.lower()),
            "enabled": True,
        }
        if sites:
            rule["domain"] = sites
        if ips:
            rule["ip"] = ips
        rules.append(rule)
        idx += 1
    return rules


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a v2RayNG routing rules QR code and JSON from config."
    )
    parser.add_argument(
        "--config",
        "-c",
        default=DEFAULT_CONFIG_PATH if os.path.exists(DEFAULT_CONFIG_PATH) else DEFAULT_CONFIG_URL,
        help="Local file path or URL to config JSON.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="v2rayng_routing_qr.png",
        help="Output QR code image path (default: v2rayng_routing_qr.png).",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    rules = convert_to_v2rayng_rules(config)

    json_compact = json.dumps(rules, separators=(",", ":"), ensure_ascii=False)
    json_pretty = json.dumps(rules, indent=2, ensure_ascii=False)

    try:
        import qrcode
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json_compact)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(args.output)
        print(f"\n[+] QR code saved to: {os.path.abspath(args.output)}")
    except ImportError:
        print("\n[!] 'qrcode' package is not installed (pip install qrcode[pil]). Skipping image generation.")

    print(f"[+] Data length: {len(json_compact)} chars")
    print()
    print("JSON rules (copy to clipboard for manual import):")
    print("-" * 50)
    print(json_pretty)
    print("-" * 50)
    print()
    print(
        "[!] Set Domain Strategy to 'IPIfNonMatch' in\n"
        "    v2RayNG Settings before importing these rules."
    )


if __name__ == "__main__":
    main()
