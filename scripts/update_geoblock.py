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

import sys
import re
import asyncio
import urllib.request
import urllib.error
from pathlib import Path

# Paths relative to repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
GEOBLOCK_FILE = DATA_DIR / "category-geoblock-ru"
CATEGORY_RU_FILE = DATA_DIR / "category-ru"
WHITELIST_FILE = DATA_DIR / "whitelist"

# Antifilter community curated blocked domains (supports multiple concurrent mirrors)
COMMUNITY_URLS = [
    "https://community.antifilter.download/list/domains.lst",
]

# Regex for valid domain name (RFC 1035 / RFC 1123)
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)

# Protected Top-Level Domains (Strict Safety Gate)
PROTECTED_TLDS = (".ru", ".рф", ".su", ".xn--p1ai")


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
    """Load domains from category-ru and whitelist to ensure they are never proxied."""
    protected = set()
    for file_path in (CATEGORY_RU_FILE, WHITELIST_FILE):
        if not file_path.exists():
            continue
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                d = clean_domain_string(line)
                if d and is_valid_domain(d):
                    protected.add(d)
    print(f"[Safety Gate] Loaded {len(protected)} protected domains from category-ru and whitelist.")
    return protected


def load_baseline_geoblock() -> set[str]:
    """Load existing manual baseline from category-geoblock-ru and data/ai."""
    baseline = set()
    for file_path in (GEOBLOCK_FILE, DATA_DIR / "ai"):
        if not file_path.exists():
            continue
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                d = clean_domain_string(line)
                if d and is_valid_domain(d):
                    baseline.add(d)
    print(f"[Baseline] Loaded {len(baseline)} baseline domains.")
    return baseline


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
        data = resp.read(MAX_PAYLOAD_BYTES)
        return data.decode("utf-8", errors="ignore")


async def fetch_single_url(url: str, timeout: int = 15) -> set[str]:
    """Asynchronously fetch and parse domains from a single remote URL with cancellation safety."""
    print(f"[Fetch] Concurrently fetching: {url}...")
    try:
        raw_text = await asyncio.wait_for(
            asyncio.to_thread(_sync_fetch, url, timeout),
            timeout=timeout + 2
        )
    except asyncio.TimeoutError:
        print(f"[Warning] Timeout fetching {url} after {timeout}s. Skipping.")
        return set()
    except urllib.error.HTTPError as e:
        print(f"[Warning] HTTP {e.code} ({e.reason}) fetching {url}. Skipping.")
        return set()
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"[Warning] Network error fetching {url}: {e}. Skipping.")
        return set()

    domains = set()
    for raw_line in raw_text.splitlines():
        d = clean_domain_string(raw_line)
        if d and is_valid_domain(d):
            domains.add(d)
    print(f"[Fetch] Retrieved {len(domains)} valid domains from {url}.")
    return domains


async def fetch_all_community_domains() -> set[str]:
    """Execute concurrent non-blocking fetch across all community mirrors."""
    tasks = [fetch_single_url(url) for url in COMMUNITY_URLS]
    results = await asyncio.gather(*tasks, return_exceptions=False)
    combined = set().union(*results) if results else set()
    print(f"[Fetch] Total community domains retrieved: {len(combined)}.")
    return combined


def is_protected_domain(domain: str, protected: set[str]) -> bool:
    """Guard clause: returns True if domain belongs to protected TLD or protected RU lists."""
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
    community_urls: list[str] = COMMUNITY_URLS,
) -> None:
    protected = load_protected_domains()
    baseline = load_baseline_geoblock()
    community = await fetch_all_community_domains()

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

    # Write atomically with rollback protection
    output_lines = [f"domain:{d}\n" for d in sorted(final_domains)]
    temp_file = geoblock_file.with_suffix(".tmp")
    try:
        with open(temp_file, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(output_lines)
        temp_file.replace(geoblock_file)
    except Exception as e:
        temp_file.unlink(missing_ok=True)
        print(f"[Error] Failed to write {geoblock_file.name}: {e}. Rolled back.")
        raise

    print(f"[Success] Updated {geoblock_file.name}: {len(final_domains)} domains written atomically.")


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
