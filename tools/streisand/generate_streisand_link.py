#!/usr/bin/env python3
"""
Generate a Streisand (iOS) routing import link from a routing config.

Fetches or reads HAPP/DEFAULT.JSON (or custom config/URL), converts it to the
Xray V2 routing schema, serialises it as a binary plist, and produces
a ready-to-use streisand:// deep-link.

Dependencies: Python 3.8+ (standard library only, no third-party packages).
"""

import argparse
import base64
import json
import os
import plistlib
import sys
import urllib.request
import uuid

DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "HAPP",
    "DEFAULT.JSON",
)
DEFAULT_CONFIG_URL = "https://raw.githubusercontent.com/mvrvntn/routing/main/HAPP/DEFAULT.JSON"


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


def convert_to_v2(config: dict) -> dict:
    """Convert HAPP config to Xray/Streisand V2 routing schema."""
    block_sites = config.get("BlockSites", [])
    proxy_sites = config.get("ProxySites", [])
    direct_sites = config.get("DirectSites", [])
    block_ips = config.get("BlockIp", [])
    proxy_ips = config.get("ProxyIp", [])
    direct_ips = config.get("DirectIp", [])

    v2 = {
        "name": config.get("Name", "VPN Routing"),
        "uuid": str(uuid.uuid4()).upper(),
        "domainStrategy": "AsIs",
        "domainMatcher": "hybrid",
        "rules": [],
    }

    # Block
    if block_sites or block_ips:
        rule = {"domainMatcher": "hybrid", "outboundTag": "block"}
        if block_sites:
            rule["domain"] = block_sites
        if block_ips:
            rule["ip"] = block_ips
        v2["rules"].append(rule)

    # Proxy
    if proxy_sites or proxy_ips:
        rule = {"domainMatcher": "hybrid", "outboundTag": "proxy"}
        if proxy_sites:
            rule["domain"] = proxy_sites
        if proxy_ips:
            rule["ip"] = proxy_ips
        v2["rules"].append(rule)

    # Direct
    if direct_sites or direct_ips:
        rule = {"domainMatcher": "hybrid", "outboundTag": "direct"}
        if direct_sites:
            rule["domain"] = direct_sites
        if direct_ips:
            rule["ip"] = direct_ips
        v2["rules"].append(rule)

    return v2


def generate_link(v2_config: dict) -> str:
    """Pack V2 config into a streisand:// deep-link."""
    plist_bytes = plistlib.dumps(v2_config, fmt=plistlib.FMT_BINARY)
    inner_b64 = base64.b64encode(plist_bytes).decode("utf-8")
    import_url = f"import/route://{inner_b64}"
    outer_b64 = base64.b64encode(import_url.encode("utf-8")).decode("utf-8")
    return f"streisand://{outer_b64}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Streisand routing import link from HAPP/INCY config."
    )
    parser.add_argument(
        "--config",
        "-c",
        default=DEFAULT_CONFIG_PATH if os.path.exists(DEFAULT_CONFIG_PATH) else DEFAULT_CONFIG_URL,
        help="Local file path or URL to config JSON.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    v2 = convert_to_v2(config)
    link = generate_link(v2)

    print()
    print("=" * 60)
    print("Streisand V2 Import Link")
    print("=" * 60)
    print(link)
    print("=" * 60)
    print()
    print(
        "[!] Update geoip.dat and geosite.dat in\n"
        "    Streisand -> Settings -> Routing -> Assets\n"
        "    before applying this routing profile."
    )


if __name__ == "__main__":
    main()
