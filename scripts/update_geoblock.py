#!/usr/bin/env python3
"""
Smart Ingestion & Sanitization Pipeline for category-geoblock-ru
Asynchronous architecture using native asyncio + thread executor:
1. Loads protected RU domains and whitelist (Safety Gate).
2. Preserves baseline custom domains.
3. Fetches community curated blocked domains concurrently across all mirrors.
4. Normalizes, validates syntax, and eliminates redundant subdomains.
5. Performs atomic update of data/category-geoblock-ru.
"""

import os
import sys
import re
import concurrent.futures
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Coroutine

# Paths relative to repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
GEOBLOCK_FILE = DATA_DIR / "category-geoblock-ru"
CATEGORY_RU_FILE = DATA_DIR / "category-ru"
WHITELIST_FILE = DATA_DIR / "whitelist"
TORRENT_FILE = DATA_DIR / "torrent"
DIRECT_GAMING_FILES = (
    DATA_DIR / "epicgames",
    DATA_DIR / "steam",
    DATA_DIR / "riot",
    DATA_DIR / "escapefromtarkov",
    DATA_DIR / "origin",
    DATA_DIR / "faceit",
)

# Antifilter & Re-filter community curated blocked domains (supports multiple concurrent mirrors)
COMMUNITY_URLS = [
    "https://community.antifilter.download/list/domains.lst",
    "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/refs/heads/main/community.lst",
]

# Regex for valid domain name (RFC 1035 / RFC 1123)
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)

# Protected Top-Level Domains (Strict Safety Gate)
PROTECTED_TLDS = (".ru", ".рф", ".su", ".xn--p1ai")

# Bare public suffixes / direct Microsoft CDN domains that must never enter geoblock
BARE_PROTECTED_SUFFIXES = {"co.nz", "com.ua", "live.net"}

# Explicit overrides permitted through safety gate (e.g. services that geoblock RU)
EXPLICIT_PROXY_OVERRIDES = {
    "lava.ru",
    "airbnb.ru",
    "freedom-travel.kz",
    "freedom-travel.at",
    "auth.xboxlive.com",
    "gssv-play-prod.xboxlive.com",
    "bestchange.ru",
    "appstorrent.ru",
    "vlast.kz",
    "orda.kz",
    "colta.ru",
    "agentura.ru",
    "4pda.ru",
}

# Baseline Apple Pay, Apple Wallet & Apple Cash endpoints (fixes regional lockouts on iOS)
APPLE_WALLET_DOMAINS = {
    "apple-pay-gateway.apple.com",
    "cn-apple-pay-gateway.apple.com",
    "apple-pay.com",
    "applepay.apple.com",
    "applepay.com",
    "applepaycash.net",
    "applepaycash.tv",
    "applewallet.com",
    "applewallet.tv",
    "pass-services.apple.com",
    "passbook.apple.com",
    "paymentpass.apple.com",
    "smp-device.apple.com",
    "smp-device-content.apple.com",
    "smp-payment.apple.com",
    "wallet.apple.com",
    "pos-device.apple.com",
    "smp-paymentservices.apple.com",
    "applepay.cdn-apple.com",
    "applepay.info",
    "applepaycash.com",
    "token.americanexpress.com",
    "network-services.americanexpress.com",
    "smoothpebble.apple.com",
    "pds.apple.com",
    "vts.visa.com",
    "token.visa.com",
    "mdes.mastercard.com",
}

for _prefix in ("pr", "nc", "tj"):
    _max_pod = 3 if _prefix == "tj" else 15
    for _i in range(1, _max_pod + 1):
        APPLE_WALLET_DOMAINS.add(f"{_prefix}-pod{_i}-smp-device.apple.com")
        APPLE_WALLET_DOMAINS.add(f"apple-pay-gateway-{_prefix}-pod{_i}.apple.com")


def clean_domain_string(raw: str) -> str:
    """Strip protocol, path, port, prefixes, and trailing dots."""
    line = raw.strip()
    if not line or line.startswith("#"):
        return ""
    for prefix in ("domain:", "full:", "keyword:"):
        if line.startswith(prefix):
            line = line.removeprefix(prefix)
            break

    if "://" in line:
        line = line.split("://", 1)[1]
    line = line.split("/", 1)[0]
    line = line.split(":", 1)[0]
    line = line.split("?", 1)[0]
    line = line.strip(".").lower()
    return line


def is_valid_domain(domain: str) -> bool:
    """Verify domain syntax and ensure it's not an IP address."""
    if not domain or len(domain) > 253:
        return False
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain):
        return False
    return bool(DOMAIN_REGEX.match(domain))


def load_protected_domains() -> set[str]:
    """Load domains from category-ru, whitelist, torrent, and direct gaming lists to ensure they are never proxied."""
    protected = set(BARE_PROTECTED_SUFFIXES)
    for file_path in (CATEGORY_RU_FILE, WHITELIST_FILE, TORRENT_FILE, *DIRECT_GAMING_FILES):
        if not file_path.exists():
            continue
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                d = clean_domain_string(line)
                if d and is_valid_domain(d):
                    protected.add(d)
    print(f"[Safety Gate] Loaded {len(protected)} protected domains from category-ru, whitelist, torrent, and gaming lists.")
    return protected


def load_baseline_geoblock(geoblock_file: Path = GEOBLOCK_FILE) -> set[str]:
    """Load existing manual baseline from category-geoblock-ru, data/ai, and Apple Wallet endpoints."""
    baseline = set(APPLE_WALLET_DOMAINS)
    for file_path in (geoblock_file, DATA_DIR / "ai"):
        if not file_path.exists():
            continue
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                s = line.strip()
                if s.startswith("regexp:"):
                    continue
                d = clean_domain_string(s)
                if d and is_valid_domain(d):
                    baseline.add(d)
    print(f"[Baseline] Loaded {len(baseline)} baseline domains.")
    return baseline


def load_baseline_regexps(geoblock_file: Path = GEOBLOCK_FILE) -> list[str]:
    """Load existing regexp: rules from category-geoblock-ru so they are preserved across updates."""
    regexps: list[str] = []
    seen: set[str] = set()
    if not geoblock_file.exists():
        return regexps
    with open(geoblock_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if " #" in s:
                s = s.split(" #", 1)[0].strip()
            if s.startswith("regexp:"):
                pattern = s.removeprefix("regexp:").strip()
                if pattern and pattern not in seen:
                    seen.add(pattern)
                    regexps.append(pattern)
    return regexps


def run_coro(coro: Coroutine[Any, Any, Any]) -> Any:
    """Drive a pure coroutine to completion without requiring a loopback socketpair event loop."""
    try:
        coro.send(None)
    except StopIteration as exc:
        return exc.value
    finally:
        coro.close()


# Max allowed payload size per remote fetch (10 MB) to prevent DoS / Memory Bombs
MAX_PAYLOAD_BYTES = 10 * 1024 * 1024


def _sync_fetch(url: str, timeout: int = 15) -> str:
    """Synchronous HTTP worker executed inside thread pool with size limit."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; KoridorRouting/1.0)"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise ValueError(f"HTTP status {resp.status}")
        data = resp.read(MAX_PAYLOAD_BYTES + 1)
        if len(data) > MAX_PAYLOAD_BYTES:
            raise ValueError(f"Payload from {url} exceeds maximum limit of {MAX_PAYLOAD_BYTES} bytes")
        return data.decode("utf-8", errors="ignore")


async def fetch_single_url(url: str, timeout: int = 15) -> set[str]:
    """Fetch and parse domains from a single remote URL with timeout and error handling."""
    print(f"[Fetch] Concurrently fetching: {url}...")
    try:
        raw_text = _sync_fetch(url, timeout)
    except TimeoutError:
        print(f"[Warning] Timeout fetching {url} after {timeout}s. Skipping.")
        return set()
    except urllib.error.HTTPError as e:
        print(f"[Warning] HTTP {e.code} ({e.reason}) fetching {url}. Skipping.")
        return set()
    except (urllib.error.URLError, OSError, ValueError) as e:
        print(f"[Warning] Network error fetching {url}: {e}. Skipping.")
        return set()

    domains = set()
    for raw_line in raw_text.splitlines():
        d = clean_domain_string(raw_line)
        if d and is_valid_domain(d):
            domains.add(d)
    print(f"[Fetch] Retrieved {len(domains)} valid domains from {url}.")
    return domains


async def fetch_all_community_domains(urls: list[str] | None = None) -> set[str]:
    """Execute concurrent non-blocking fetch across all community mirrors."""
    target_urls = urls if urls is not None else COMMUNITY_URLS
    if not target_urls:
        return set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(8, len(target_urls))) as executor:
        futures = [executor.submit(run_coro, fetch_single_url(url)) for url in target_urls]
        results = [fut.result() for fut in futures]
    combined = set().union(*results) if results else set()
    print(f"[Fetch] Total community domains retrieved: {len(combined)}.")
    return combined


def is_protected_domain(domain: str, protected: set[str]) -> bool:
    """Guard clause: returns True if domain belongs to protected TLD or protected RU lists."""
    if domain in EXPLICIT_PROXY_OVERRIDES or domain in APPLE_WALLET_DOMAINS:
        return False

    # Prevent root apple.com from entering geoblock (Apple Pay/Wallet subdomains are explicitly allowed)
    if domain == "apple.com":
        return True

    if domain.endswith(PROTECTED_TLDS):
        return True

    parts = domain.split(".")
    for i in range(len(parts) - 1):
        if ".".join(parts[i:]) in protected:
            return True
    return False


def prune_redundant_subdomains(domains: set[str]) -> set[str]:
    """
    If 'example.com' is present, eliminate 'sub.example.com', 'a.b.example.com'.
    In v2fly/geosite, a parent domain matches all subdomains automatically.
    """
    sorted_domains = sorted(domains, key=lambda x: (x.count("."), len(x)))
    pruned = set()

    for d in sorted_domains:
        parts = d.split(".")
        if not any(".".join(parts[i:]) in pruned for i in range(1, len(parts) - 1)):
            pruned.add(d)

    savings = len(domains) - len(pruned)
    print(f"[Prune] Domain collapsing removed {savings} redundant subdomains ({len(pruned)} remaining).")
    return pruned


async def async_main(
    geoblock_file: Path = GEOBLOCK_FILE,
    community_urls: list[str] | None = None,
) -> None:
    protected = load_protected_domains()
    baseline = load_baseline_geoblock()
    baseline_regexps = load_baseline_regexps(geoblock_file)
    community = await fetch_all_community_domains(
        COMMUNITY_URLS if community_urls is None else community_urls
    )

    combined = baseline | community
    print(f"[Process] Total raw domain pool: {len(combined)}")

    # Apply Safety Gate: reject RU domains and protected lists
    safe_pool = {d for d in combined if not is_protected_domain(d, protected)}
    blocked_by_safety = len(combined) - len(safe_pool)
    print(f"[Safety Gate] Filtered out {blocked_by_safety} protected/RU domains.")

    # Prune redundant subdomains
    final_domains = prune_redundant_subdomains(safe_pool)

    # Sanity check
    if len(final_domains) < len(baseline) * 0.8:
        print(f"[Error] Sanitized count ({len(final_domains)}) abnormally lower than baseline ({len(baseline)}). Aborting.")
        sys.exit(1)

    # Write atomically with rollback protection (preserving regexp: entries)
    output_lines = [f"domain:{d}\n" for d in sorted(final_domains)]
    for rx in baseline_regexps:
        output_lines.append(f"regexp:{rx}\n")
    temp_file = geoblock_file.with_suffix(".tmp")
    try:
        with open(temp_file, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(output_lines)
            f.flush()
            os.fsync(f.fileno())
        temp_file.replace(geoblock_file)
    except Exception as e:
        temp_file.unlink(missing_ok=True)
        print(f"[Error] Failed to write {geoblock_file.name}: {e}. Rolled back.")
        raise

    print(
        f"[Success] Updated {geoblock_file.name}: {len(final_domains)} domains "
        f"and {len(baseline_regexps)} regexps written atomically."
    )


def main() -> None:
    run_coro(async_main())


if __name__ == "__main__":
    main()
