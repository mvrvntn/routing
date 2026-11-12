#!/usr/bin/env python3
"""
Export routing rules to .lst format for OpenWrt (dnsmasq, pbr, LuCI/Splify2).

Directories:
  OPENWRT/domains/koridor_<name>.lst
  OPENWRT/ips/koridor_<name>.lst
"""

import argparse
import ipaddress
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = REPO_ROOT / "data"
GEOIP_DIR = REPO_ROOT / "geoip"
OPENWRT_DIR = REPO_ROOT / "OPENWRT"
DOMAINS_OUT_DIR = OPENWRT_DIR / "domains"
IPS_OUT_DIR = OPENWRT_DIR / "ips"

HEADER = """# Project: «коридор роутинг»
# Source: https://github.com/mvrvntn/routing
# Сервис «коридор»: https://tinyurl.com/koridor-start
"""

DOMAIN_LABEL_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")
ALLOW_BARE_TLD_FILES = {"category-ru", "private"}


def clean_domain(raw_line: str) -> str:
    """Strip prefixes, tags, comments, and normalize domain string."""
    line = raw_line.strip()
    if not line or line.startswith("#"):
        return ""
    # Strip inline comment
    line = line.split("#", 1)[0].strip()
    # Strip prefixes
    for prefix in ("domain:", "full:", "keyword:", "regexp:"):
        if line.lower().startswith(prefix):
            line = line[len(prefix):].strip()
            break
    # Strip attributes/tags like @ads, @telemetry, @!cn
    line = re.sub(r"\s*@\S+", "", line)
    # Strip URL schemes, paths, query, ports if present
    if "://" in line:
        line = line.split("://", 1)[1]
    line = line.split("/", 1)[0].split(":", 1)[0].split("?", 1)[0]
    return line.strip(".").lower()


def is_valid_domain(domain: str, allow_bare_tld: bool = False) -> bool:
    """Validate that domain is a valid FQDN / domain label.
    
    If allow_bare_tld is False, domain must contain at least one dot (e.g. example.com).
    Bare single labels (like 'youtube', 'xbox') are rejected for router lists,
    except in category-ru and private lists where national ccTLDs (ru, su, by, kz)
    and internal zones (lan, local) are required.
    """
    if not domain or len(domain) > 253:
        return False
    # Reject IPv4 address
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain):
        return False
    # Reject regex characters
    if any(c in domain for c in "^$*+?()[]{}|\\"):
        return False
    labels = domain.split(".")
    # Unless explicitly allowed, bare single labels without dot are rejected
    if not allow_bare_tld and len(labels) < 2:
        return False
    # Single label cannot be numeric
    if len(labels) == 1 and labels[0].isdigit():
        return False
    # TLD cannot be numeric
    if len(labels) > 1 and labels[-1].isdigit():
        return False
    for label in labels:
        if not DOMAIN_LABEL_RE.match(label):
            return False
    return True


def resolve_domain_file(
    file_path: Path,
    data_dir: Path = DATA_DIR,
    visited: set[Path] | None = None,
    allow_bare_tld: bool | None = None,
) -> set[str]:
    """Recursively parse domain file expanding all include: references."""
    if visited is None:
        visited = set()

    file_path = file_path.resolve()
    if file_path in visited:
        return set()
    visited.add(file_path)

    if allow_bare_tld is None:
        allow_bare_tld = file_path.name in ALLOW_BARE_TLD_FILES

    domains: set[str] = set()
    if not file_path.exists():
        print(f"[!] Warning: domain file {file_path} does not exist.")
        return domains

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                continue
            if line_str.startswith("include:"):
                inc_target = line_str[len("include:"):].strip()
                inc_path = data_dir / inc_target
                domains.update(resolve_domain_file(inc_path, data_dir, visited.copy(), allow_bare_tld))
            else:
                cleaned = clean_domain(line_str)
                if cleaned and is_valid_domain(cleaned, allow_bare_tld=allow_bare_tld):
                    domains.add(cleaned)

    return domains


def clean_ip_file(file_path: Path) -> list[str]:
    """Parse geoip .txt file and return sorted unique valid IPv4/IPv6 CIDRs."""
    cidrs: set[str] = set()
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                continue
            line_str = line_str.split("#", 1)[0].strip()
            try:
                net = ipaddress.ip_network(line_str, strict=False)
                cidrs.add(str(net))
            except ValueError:
                continue

    def ip_sort_key(net_str: str):
        net = ipaddress.ip_network(net_str)
        return (net.version, int(net.network_address), net.prefixlen)

    return sorted(cidrs, key=ip_sort_key)


def build_domains(data_dir: Path = DATA_DIR, out_dir: Path = DOMAINS_OUT_DIR) -> list[Path]:
    """Build domain lists for OpenWrt."""
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = []
    for file_path in sorted(data_dir.iterdir()):
        if not file_path.is_file():
            continue
        base_name = file_path.name
        domains = sorted(resolve_domain_file(file_path, data_dir))
        out_file = out_dir / f"koridor_{base_name}.lst"
        content = HEADER + "\n".join(domains) + ("\n" if domains else "")
        with open(out_file, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        generated.append(out_file)
    return generated


def build_ips(geoip_dir: Path = GEOIP_DIR, out_dir: Path = IPS_OUT_DIR) -> list[Path]:
    """Build IP lists for OpenWrt."""
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = []
    for file_path in sorted(geoip_dir.glob("*.txt")):
        if not file_path.is_file():
            continue
        base_name = file_path.stem.lower()
        cidrs = clean_ip_file(file_path)
        out_file = out_dir / f"koridor_{base_name}.lst"
        content = HEADER + "\n".join(cidrs) + ("\n" if cidrs else "")
        with open(out_file, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        generated.append(out_file)
    return generated


def main() -> None:
    parser = argparse.ArgumentParser(description="Export routing rules to .lst format for OpenWrt.")
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR, help="Path to data directory")
    parser.add_argument("--geoip-dir", type=Path, default=GEOIP_DIR, help="Path to geoip directory")
    parser.add_argument("--domains-out", type=Path, default=DOMAINS_OUT_DIR, help="Output directory for domain lists")
    parser.add_argument("--ips-out", type=Path, default=IPS_OUT_DIR, help="Output directory for IP lists")
    args = parser.parse_args()

    print("[*] Generating OpenWrt domain lists...")
    domain_files = build_domains(args.data_dir, args.domains_out)
    print(f"[+] Generated {len(domain_files)} domain lists in {args.domains_out}")

    print("[*] Generating OpenWrt IP lists...")
    ip_files = build_ips(args.geoip_dir, args.ips_out)
    print(f"[+] Generated {len(ip_files)} IP lists in {args.ips_out}")


if __name__ == "__main__":
    main()
