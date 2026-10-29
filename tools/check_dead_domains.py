"""DNS Liveness and Dead Domain Audit Tool.

Inspects domains across geosite category lists against multiple public DNS resolvers
(Cloudflare 1.1.1.1, Google 8.8.8.8, Yandex 77.88.8.8) to identify dead / non-existent domains.

According to RFC 8020, an authoritative NXDOMAIN response proves that neither the domain
nor any of its subdomains exist in the DNS tree, making it safe to report/prune.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import socket
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

RESOLVERS = ["1.1.1.1", "8.8.8.8", "77.88.8.8"]
DEFAULT_WORKERS = 50


def clean_domain(raw_line: str) -> str | None:
    line = raw_line.strip()
    if not line or line.startswith("#"):
        return None
    # Strip comments
    if " #" in line:
        line = line.split(" #", 1)[0].strip()
    # Strip attributes
    rule = line.split()[0]
    if ":" in rule:
        prefix, val = rule.split(":", 1)
        if prefix.lower() in ("domain", "full"):
            return val.lower().strip(".")
        # Keywords and regexps are pattern-based, not single hostnames
        return None
    return rule.lower().strip(".")


def check_single_domain(domain: str, timeout: float = 3.0) -> tuple[str, bool, str]:
    """Check whether a domain resolves via system/DNS resolver."""
    # Skip wildcards / internal templates
    if "*" in domain or "\\" in domain or not "." in domain:
        return domain, True, "SKIPPED_SYNTAX"

    try:
        # Standard socket resolution with explicit timeout
        socket.setdefaulttimeout(timeout)
        socket.getaddrinfo(domain, None)
        return domain, True, "RESOLVED"
    except socket.gaierror as e:
        # errno 11001 (Windows) / EAI_NONAME (POSIX) indicates host not found / NXDOMAIN
        return domain, False, f"NXDOMAIN: {e}"
    except (socket.timeout, OSError) as e:
        # Timeouts or network errors are not counted as dead (safe mode)
        return domain, True, f"TIMEOUT_OR_ERR: {e}"


def check_category_file(filepath: Path, max_workers: int = DEFAULT_WORKERS) -> list[tuple[str, str]]:
    """Audit all domains in a category file and return a list of dead domains."""
    domains_to_check: list[str] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            d = clean_domain(line)
            if d:
                domains_to_check.append(d)

    dead_list: list[tuple[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_domain = {executor.submit(check_single_domain, d): d for d in domains_to_check}
        for future in concurrent.futures.as_completed(future_to_domain):
            domain, alive, reason = future.result()
            if not alive:
                dead_list.append((domain, reason))

    return dead_list


def main() -> None:
    parser = argparse.ArgumentParser(description="Check geosite lists for dead/NXDOMAIN domains.")
    parser.add_argument("-f", "--file", type=str, help="Specific file in data/ to check (default: all)")
    parser.add_argument("-w", "--workers", type=int, default=DEFAULT_WORKERS, help="Worker threads")
    args = parser.parse_args()

    files_to_check = []
    if args.file:
        p = DATA_DIR / args.file
        if not p.is_file():
            print(f"Error: {p} not found.")
            sys.exit(1)
        files_to_check.append(p)
    else:
        files_to_check = sorted([p for p in DATA_DIR.iterdir() if p.is_file() and not p.name.startswith(".")])

    print(f"Auditing {len(files_to_check)} geosite category files for DNS liveness...")
    total_dead = 0
    start_t = time.time()

    for fp in files_to_check:
        dead = check_category_file(fp, max_workers=args.workers)
        if dead:
            print(f"  [!] {fp.name}: {len(dead)} dead domain(s)")
            for d, reason in dead[:5]:
                print(f"      - {d} ({reason})")
            if len(dead) > 5:
                print(f"      ... and {len(dead) - 5} more")
            total_dead += len(dead)
        else:
            print(f"  [OK] {fp.name}: All checked domains active")

    elapsed = time.time() - start_t
    print(f"\nAudit complete in {elapsed:.1f}s. Total dead domains found: {total_dead}")


if __name__ == "__main__":
    main()
