"""Shadowrocket Configuration and Ruleset Generator.

Generates standard Shadowrocket .CONF profiles and modular .list rulesets
based on the repository's geosite domain lists (`data/*`) and geoip IP subnets (`geoip/*`).

Supports:
- SHADOWROCKET/DEFAULT.CONF (Smart split-tunnel routing)
- SHADOWROCKET/WHITELIST.CONF (Strict Russian whitelist)
- SHADOWROCKET/rules/*.list (Pre-compiled modular rulesets for remote loading)
"""

from __future__ import annotations

import argparse
import ipaddress
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = REPO_ROOT / "data"
GEOIP_DIR = REPO_ROOT / "geoip"
OUTPUT_DIR = REPO_ROOT / "SHADOWROCKET"
RULES_DIR = OUTPUT_DIR / "rules"

REPO_URL = "https://cdn.jsdelivr.net/gh/mvrvntn/routing@main"
GITHUB_REPO_URL = "https://github.com/mvrvntn/routing"


def parse_geosite_rule(line: str) -> str | None:
    """Convert v2fly geosite syntax to Shadowrocket rule format."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    # Strip inline comments
    if " #" in line:
        line = line.split(" #", 1)[0].strip()

    # Strip attributes (@attr)
    parts = line.split()
    rule_def = parts[0]

    if ":" in rule_def:
        prefix, val = rule_def.split(":", 1)
        prefix = prefix.lower()
        val = val.lower().strip(".")
        if prefix == "domain":
            return f"DOMAIN-SUFFIX,{val}"
        elif prefix == "full":
            return f"DOMAIN,{val}"
        elif prefix == "keyword":
            return f"DOMAIN-KEYWORD,{val}"
        elif prefix == "regexp":
            # Shadowrocket does not support PCRE regex on hostnames
            return None
    else:
        # Default implicit domain suffix
        return f"DOMAIN-SUFFIX,{rule_def.lower().strip('.')}"

    return None


def resolve_data_file_rules(src_path: Path, visited: set[Path] | None = None) -> list[str]:
    """Read a data category file and recursively resolve rules and include: directives."""
    if visited is None:
        visited = set()
    src_path = src_path.resolve()
    if not src_path.exists() or src_path in visited:
        return []

    visited.add(src_path)
    rules: list[str] = []

    with open(src_path, "r", encoding="utf-8") as f:
        for line in f:
            raw_line = line.strip()
            if not raw_line or raw_line.startswith("#"):
                continue
            if " #" in raw_line:
                raw_line = raw_line.split(" #", 1)[0].strip()
            parts = raw_line.split()
            rule_def = parts[0]
            if rule_def.startswith("include:"):
                inc_name = rule_def.split(":", 1)[1].strip()
                inc_path = src_path.parent / inc_name
                rules.extend(resolve_data_file_rules(inc_path, visited))
            else:
                converted = parse_geosite_rule(line)
                if converted:
                    rules.append(converted)

    return rules


def convert_data_file_to_list(src_path: Path, dst_path: Path, name: str) -> int:
    """Read a data category file and write a Shadowrocket .list file."""
    if not src_path.exists():
        return 0

    out_rules = resolve_data_file_rules(src_path)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for r in out_rules:
        if r not in seen:
            seen.add(r)
            deduped.append(r)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(f"# NAME: {name}.list\n")
        f.write(f"# TOTAL RULES: {len(deduped)}\n")
        f.write(f"# REPO: {GITHUB_REPO_URL}\n\n")
        for r in deduped:
            f.write(f"{r}\n")

    return len(deduped)


def convert_ip_file_to_list(src_path: Path, dst_path: Path, name: str) -> int:
    """Read an IP CIDR list, collapse overlapping CIDRs, and write Shadowrocket .list."""
    if not src_path.exists():
        return 0

    v4_nets: list[ipaddress.IPv4Network] = []
    v6_nets: list[ipaddress.IPv6Network] = []
    with open(src_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cidr = line.split()[0].strip()
            try:
                net = ipaddress.ip_network(cidr, strict=False)
                if net.version == 4:
                    v4_nets.append(net)
                else:
                    v6_nets.append(net)
            except ValueError:
                continue

    collapsed_v4 = sorted(ipaddress.collapse_addresses(v4_nets), key=lambda n: (int(n.network_address), n.prefixlen))
    collapsed_v6 = sorted(ipaddress.collapse_addresses(v6_nets), key=lambda n: (int(n.network_address), n.prefixlen))
    deduped = [f"IP-CIDR,{net},no-resolve" for net in collapsed_v4] + [
        f"IP-CIDR6,{net},no-resolve" for net in collapsed_v6
    ]

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(f"# NAME: {name}.list\n")
        f.write(f"# TOTAL IP RULES: {len(deduped)}\n")
        f.write(f"# REPO: {GITHUB_REPO_URL}\n\n")
        for r in deduped:
            f.write(f"{r}\n")

    return len(deduped)


def generate_default_conf() -> str:
    """Generate the full content for SHADOWROCKET/DEFAULT.CONF."""
    return f"""# @mvrvntn Routing for Shadowrocket
# Profile: DEFAULT (Умный раздельный роутинг)
# Repository: {GITHUB_REPO_URL}

[General]
# Отключение IPv6 для предотвращения утечек и обхода антифрода
ipv6 = false
prefer-ipv6 = false

# Разрешение приватных IP адресов локальной сети
private-ip-answer = true

# Управление DNS: локальный DNS для DIRECT-сайтов РФ, защищенный DoH для остальных
dns-direct-system = true
dns-fallback-system = false
dns-direct-fallback-proxy = true

# Удаленный DoH (Google) и отечественный DoH (Yandex)
dns-server = https://dns.google/dns-query, 8.8.8.8
fallback-dns-server = https://dns.yandex.ru/dns-query, 77.88.8.8, system

# Перехват стандартных DNS запросов
hijack-dns = :53

# Всегда возвращать реальный IP адрес
always-real-ip = *

# Служебные адреса и локальные сети в обход туннеля
skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, 127.0.0.1, localhost, *.local, captive.apple.com

# Исключения из виртуального TUN-интерфейса
tun-excluded-routes = 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.88.99.0/24, 192.168.0.0/16, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 255.255.255.255/32, 239.255.255.250/32

icmp-auto-reply = false
always-reject-url-rewrite = false
udp-policy-not-supported-behaviour = REJECT

# URL автоматического обновления конфигурации
update-url = {REPO_URL}/SHADOWROCKET/DEFAULT.CONF

[Host]
# Статические DNS-записи для государственных налоговых сервисов
lkfl2.nalog.ru = 213.24.64.175
lknpd.nalog.ru = 213.24.64.181
dns.google = 8.8.8.8

[Rule]
# --- Блокировка рекламы и трекеров (Block) ---
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/category-ads.list,REJECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/torrent.list,REJECT

# --- Apple Pay / Wallet / Apple Intelligence (PROXY для обхода гео-блокировок) ---
DOMAIN-KEYWORD,smp-,PROXY
DOMAIN-KEYWORD,applepay,PROXY
DOMAIN-SUFFIX,apple-pay.com,PROXY

# --- Discord (Полная маршрутизация: Домены + Голосовые RTC IP + Медиа-порты) ---
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/discord.list,PROXY
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/discord-ips.list,PROXY
DEST-PORT,19294-19344,PROXY

# --- Push-уведомления (Apple APNs & Google FCM) — напрямую до geoblock-ru ---
DEST-PORT,5223,DIRECT
DOMAIN-SUFFIX,push.apple.com,DIRECT
DEST-PORT,5228-5230,DIRECT
DOMAIN-KEYWORD,mtalk,DIRECT
DOMAIN-SUFFIX,fcm.googleapis.com,DIRECT

# --- Прямой доступ: Игровые платформы и стриминг (до geoblock-ru) ---
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/steam.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/epicgames.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/riot.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/origin.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/escapefromtarkov.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/faceit.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/twitch-ads.list,PROXY
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/twitch.list,DIRECT

# --- Проксируемые зарубежные ресурсы (Proxy) ---
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/category-geoblock-ru.list,PROXY
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/ai.list,PROXY
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/google-deepmind.list,PROXY
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/google-play.list,PROXY
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/youtube.list,PROXY
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/telegram.list,PROXY
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/github.list,PROXY

# --- Прямой доступ: Локальные сети и Системные сервисы (Direct) ---
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/private.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/apple.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/microsoft.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/pinterest.list,DIRECT

# --- Прямой доступ: Российские сервисы и Белый список (Direct) ---
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/category-ru.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/whitelist.list,DIRECT

# Прямое подключение ко всем IP-адресам Российской Федерации и Республики Беларусь
GEOIP,RU,DIRECT
GEOIP,BY,DIRECT

# --- Финальное правило (Все незаблокированные зарубежные ресурсы — в Proxy) ---
FINAL,PROXY
"""


def generate_whitelist_conf() -> str:
    """Generate the full content for SHADOWROCKET/WHITELIST.CONF."""
    return f"""# @mvrvntn Routing for Shadowrocket
# Profile: WHITELIST (Строгий белый список: только доверенные RU-сервисы напрямую)
# Repository: {GITHUB_REPO_URL}

[General]
ipv6 = false
prefer-ipv6 = false
private-ip-answer = true
dns-direct-system = true
dns-fallback-system = false
dns-direct-fallback-proxy = true

dns-server = https://dns.google/dns-query, 8.8.8.8
fallback-dns-server = https://dns.yandex.ru/dns-query, 77.88.8.8, system
hijack-dns = :53
always-real-ip = *

skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, 127.0.0.1, localhost, *.local, captive.apple.com
tun-excluded-routes = 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.88.99.0/24, 192.168.0.0/16, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 255.255.255.255/32, 239.255.255.250/32

icmp-auto-reply = false
always-reject-url-rewrite = false
udp-policy-not-supported-behaviour = REJECT
update-url = {REPO_URL}/SHADOWROCKET/WHITELIST.CONF

[Host]
lkfl2.nalog.ru = 213.24.64.175
lknpd.nalog.ru = 213.24.64.181
dns.google = 8.8.8.8

[Rule]
# Блокировка рекламы и торрентов
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/category-ads.list,REJECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/torrent.list,REJECT

# Прямой доступ строго для локальной сети и мобильного белого списка
# (apple.list намеренно не добавлен — при БПЛА Apple работает только через VPN)
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/private.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/whitelist.list,DIRECT
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/whitelist-ips.list,DIRECT

# Всё остальное (включая Apple/YouTube/Discord/AI) проксируется через обход БС
FINAL,PROXY
"""


def generate_relocant_conf() -> str:
    """Generate the full content for RELOCANT/SHADOWROCKET.CONF."""
    return f"""# @mvrvntn Routing for Shadowrocket
# Profile: RELOCANT (Обратный роутинг для релокантов и путешественников: РФ через прокси, мир напрямую)
# Repository: {GITHUB_REPO_URL}

[General]
ipv6 = false
prefer-ipv6 = false
private-ip-answer = true
dns-direct-system = true
dns-fallback-system = false
dns-direct-fallback-proxy = true

dns-server = https://cloudflare-dns.com/dns-query, https://dns.google/dns-query, 1.1.1.1, 8.8.8.8
fallback-dns-server = https://dns.yandex.ru/dns-query, 77.88.8.8, system
hijack-dns = :53
always-real-ip = *

skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, 127.0.0.1, localhost, *.local, captive.apple.com
tun-excluded-routes = 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.88.99.0/24, 192.168.0.0/16, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 255.255.255.255/32, 239.255.255.250/32

icmp-auto-reply = false
always-reject-url-rewrite = false
udp-policy-not-supported-behaviour = REJECT
update-url = {REPO_URL}/RELOCANT/SHADOWROCKET.CONF

[Host]
lkfl2.nalog.ru = 213.24.64.175
lknpd.nalog.ru = 213.24.64.181

[Rule]
# --- Локальные сети и системные ресурсы (Direct) ---
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/private.list,DIRECT

# --- Блокировка рекламы и трекеров (Block) ---
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/category-ads.list,REJECT

# --- Игровые серверы РФ и СНГ (Proxy) ---
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/faceit.list,PROXY

# --- Государственные порталы, банки, СБП и домены РФ (Proxy) ---
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/whitelist.list,PROXY
RULE-SET,{REPO_URL}/SHADOWROCKET/rules/category-ru.list,PROXY

# --- Подсети Российской Федерации и Республики Беларусь (Proxy) ---
GEOIP,RU,PROXY
GEOIP,BY,PROXY

# --- Весь остальной мировой интернет — напрямую (Direct) ---
FINAL,DIRECT
"""


def build_all_shadowrocket(verbose: bool = True) -> dict[str, int]:
    """Compile all rulesets and emit .CONF files."""
    RULES_DIR.mkdir(parents=True, exist_ok=True)
    stats: dict[str, int] = {}

    # 1. Compile all domain categories from data/
    for data_file in DATA_DIR.iterdir():
        if data_file.is_file() and not data_file.name.startswith("."):
            dst = RULES_DIR / f"{data_file.name}.list"
            cnt = convert_data_file_to_list(data_file, dst, data_file.name)
            stats[f"domain:{data_file.name}"] = cnt
            if verbose:
                print(f"  [+] rules/{data_file.name}.list: {cnt} rules")

    # 2. Compile IP CIDR rulesets
    discord_ip = GEOIP_DIR / "discord.txt"
    if discord_ip.is_file():
        cnt = convert_ip_file_to_list(discord_ip, RULES_DIR / "discord-ips.list", "discord-ips")
        stats["ip:discord-ips"] = cnt
        if verbose:
            print(f"  [+] rules/discord-ips.list: {cnt} IP rules")

    whitelist_ip = GEOIP_DIR / "CUSTOM-WHITELIST.txt"
    if whitelist_ip.is_file():
        cnt = convert_ip_file_to_list(whitelist_ip, RULES_DIR / "whitelist-ips.list", "whitelist-ips")
        stats["ip:whitelist-ips"] = cnt
        if verbose:
            print(f"  [+] rules/whitelist-ips.list: {cnt} IP rules")

    # 3. Write .CONF profiles
    with open(OUTPUT_DIR / "DEFAULT.CONF", "w", encoding="utf-8") as f:
        f.write(generate_default_conf())
    if verbose:
        print(f"  [OK] Written {OUTPUT_DIR / 'DEFAULT.CONF'}")

    with open(OUTPUT_DIR / "WHITELIST.CONF", "w", encoding="utf-8") as f:
        f.write(generate_whitelist_conf())
    if verbose:
        print(f"  [OK] Written {OUTPUT_DIR / 'WHITELIST.CONF'}")

    relocant_dir = REPO_ROOT / "RELOCANT"
    relocant_dir.mkdir(parents=True, exist_ok=True)
    with open(relocant_dir / "SHADOWROCKET.CONF", "w", encoding="utf-8") as f:
        f.write(generate_relocant_conf())
    if verbose:
        print(f"  [OK] Written {relocant_dir / 'SHADOWROCKET.CONF'}")

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Shadowrocket configurations and rulesets.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
    args = parser.parse_args()

    print("Building Shadowrocket rules and configurations...")
    stats = build_all_shadowrocket(verbose=not args.quiet)
    print(f"Successfully generated Shadowrocket profiles and {len(stats)} rulesets.")


if __name__ == "__main__":
    main()
