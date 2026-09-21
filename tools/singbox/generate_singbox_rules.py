#!/usr/bin/env python3
"""
Generate sing-box route rules JSON from a HAPP/INCY routing config.

Compatible with sing-box 1.8+ / 1.10+ based clients:
  - Throne
  - NekoRay v4.0+
  - sing-box GUI clients with JSON rule import

Converts geosite/geoip entries to rule_set URLs pointing to .srs files.
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

GEOSITE_SRS_BASE = "https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/sing-box"
GEOIP_SRS_BASE = "https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/sing-box"

GEOSITE_NAME_MAP = {
    "epicgames": "epic-games",
}

KNOWN_GEOSITE_SRS = {
    "whitelist",
    "category-ru",
    "category-geoblock-ru",
    "apple",
    "google-play",
    "google-deepmind",
    "microsoft",
    "github",
    "telegram",
    "youtube",
    "twitch",
    "twitch-ads",
    "pinterest",
    "steam",
    "epicgames",
    "epic-games",
    "riot",
    "escapefromtarkov",
    "faceit",
    "origin",
    "category-ads",
    "win-spy",
    "private",
    "torrent",
    "discord",
    "ai",
}

KNOWN_GEOIP_SRS = {
    "direct",
    "whitelist",
    "private",
    "telegram",
    "discord",
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


def _geosite_to_srs(name: str) -> str | None:
    mapped = GEOSITE_NAME_MAP.get(name, name)
    if mapped in KNOWN_GEOSITE_SRS:
        return f"{GEOSITE_SRS_BASE}/{mapped}.srs"
    return None


def _geoip_to_srs(name: str) -> str | None:
    if name in KNOWN_GEOIP_SRS:
        return f"{GEOIP_SRS_BASE}/{name}.srs"
    return None


def _parse_entries(site_entries: list, ip_entries: list) -> dict:
    rule_sets = []
    domain_suffix = []
    domain_keyword = []
    domain = []

    for entry in site_entries:
        if entry.startswith("geosite:"):
            url = _geosite_to_srs(entry[len("geosite:"):])
            if url:
                rule_sets.append(url)
            else:
                print(f"[!] Notice: no standalone .srs mapped for {entry}, preserving domain matcher.")
        elif entry.startswith("domain:"):
            domain_suffix.append(entry[len("domain:"):])
        elif entry.startswith("keyword:"):
            domain_keyword.append(entry[len("keyword:"):])
        else:
            domain.append(entry)

    for entry in ip_entries:
        if entry.startswith("geoip:"):
            url = _geoip_to_srs(entry[len("geoip:"):])
            if url:
                rule_sets.append(url)
            else:
                print(f"[!] Notice: no standalone .srs mapped for {entry}.")

    fields = {}
    if rule_sets:
        fields["rule_set"] = rule_sets
    if domain:
        fields["domain"] = domain
    if domain_suffix:
        fields["domain_suffix"] = domain_suffix
    if domain_keyword:
        fields["domain_keyword"] = domain_keyword
    return fields


def build_rules(config: dict) -> list:
    """Build the full sing-box route rules array from config."""
    rules = [
        {"action": "hijack-dns", "protocol": "dns"}
    ]

    groups = [
        ("Block", "block"),
        ("Proxy", "proxy"),
        ("Direct", "direct"),
    ]

    for group, action_type in groups:
        sites = config.get(f"{group}Sites", [])
        ips = config.get(f"{group}Ip", [])
        if not sites and not ips:
            continue

        fields = _parse_entries(sites, ips)
        if not fields:
            continue

        if action_type == "block":
            rule = {"action": "reject"}
        else:
            rule = {"action": "route", "outbound": action_type}

        rule.update(fields)
        rules.append(rule)

    return rules


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate sing-box route rules JSON from config."
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
        default=None,
        help="Output JSON file path. If omitted, prints to stdout.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    rules = build_rules(config)
    json_str = json.dumps(rules, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_str + "\n")
        print(f"\n[+] Rules saved to: {args.output}")
    else:
        print()
        print(json_str)

    print(f"\n[+] {len(rules)} rules generated.")
    print(
        "\nImport in Throne / NekoRay v4.0+:\n"
        "  Preferences -> Routing Setting -> Advanced -> Import JSON"
    )


if __name__ == "__main__":
    main()
