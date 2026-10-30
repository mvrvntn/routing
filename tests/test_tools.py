import unittest
import os
import sys

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tools.streisand.generate_streisand_link import convert_to_v2, generate_link
from tools.v2rayNG.generate_v2rayng_routing_qr import convert_to_v2rayng_rules
from tools.v2rayNG.generate_geoasset_qr import get_urls
from tools.singbox.generate_singbox_rules import build_rules

mock_config = {
    "Name": "TestVPN",
    "BlockSites": ["geosite:win-spy", "domain:tracker.com"],
    "BlockIp": [],
    "ProxySites": ["geosite:youtube", "keyword:proxy", "geosite:discord"],
    "ProxyIp": ["geoip:telegram"],
    "DirectSites": ["geosite:category-ru"],
    "DirectIp": ["geoip:direct"],
    "Geoipurl": "https://custom.cdn/geoip.dat",
    "Geositeurl": "https://custom.cdn/geosite.dat"
}


class TestToolsSuite(unittest.TestCase):

    def test_streisand_conversion(self):
        v2 = convert_to_v2(mock_config)
        self.assertEqual(v2["name"], "TestVPN")
        self.assertEqual(v2["domainStrategy"], "IPIfNonMatch")
        self.assertEqual(v2["domainMatcher"], "hybrid")
        self.assertTrue("uuid" in v2)
        self.assertEqual(len(v2["rules"]), 3)

        block_rule = next(r for r in v2["rules"] if r["outboundTag"] == "block")
        self.assertIn("geosite:win-spy", block_rule["domain"])

        proxy_rule = next(r for r in v2["rules"] if r["outboundTag"] == "proxy")
        self.assertIn("geosite:youtube", proxy_rule["domain"])
        self.assertIn("geoip:telegram", proxy_rule["ip"])

        link = generate_link(v2)
        self.assertTrue(link.startswith("streisand://"))

    def test_v2rayng_conversion(self):
        rules = convert_to_v2rayng_rules(mock_config)
        self.assertEqual(len(rules), 3)

        block_rule = rules[0]
        self.assertEqual(block_rule["outboundTag"], "block")
        self.assertTrue(block_rule["enabled"])
        self.assertIn("geosite:win-spy", block_rule["domain"])

        proxy_rule = rules[1]
        self.assertEqual(proxy_rule["outboundTag"], "proxy")
        self.assertIn("geosite:discord", proxy_rule["domain"])
        self.assertIn("geoip:telegram", proxy_rule["ip"])

    def test_singbox_conversion(self):
        rules = build_rules(mock_config)
        self.assertEqual(len(rules), 4)

        self.assertEqual(rules[0]["action"], "hijack-dns")
        self.assertEqual(rules[0]["protocol"], "dns")

        block_rule = next(r for r in rules if r.get("action") == "reject")
        self.assertIn("domain_suffix", block_rule)
        self.assertIn("tracker.com", block_rule["domain_suffix"])

        proxy_rule = next(r for r in rules if r.get("outbound") == "proxy")
        self.assertEqual(proxy_rule["action"], "route")
        self.assertIn("domain_keyword", proxy_rule)
        self.assertIn("proxy", proxy_rule["domain_keyword"])

    def test_geoasset_urls(self):
        cdn_urls = get_urls("cdn")
        self.assertIn("mvrvntn/routing", cdn_urls["geosite.dat"])
        self.assertIn("mvrvntn/routing", cdn_urls["geoip.dat"])

        rel_urls = get_urls("releases")
        self.assertIn("github.com/mvrvntn/routing", rel_urls["geosite.dat"])
        self.assertIn("releases/latest/download", rel_urls["geoip.dat"])

    def test_singbox_ip_entries_use_ip_rule_sets(self):
        config = {
            "ProxySites": ["geosite:telegram"],
            "ProxyIp": ["geoip:telegram", "geoip:discord"],
        }
        rules = build_rules(config)
        proxy = next(r for r in rules if r.get("outbound") == "proxy")
        self.assertIn(
            "https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/sing-box/telegram-ip.srs",
            proxy["rule_set"],
        )
        self.assertIn(
            "https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/sing-box/discord-ip.srs",
            proxy["rule_set"],
        )
        self.assertEqual(len(proxy["rule_set"]), len(set(proxy["rule_set"])))

    def test_singbox_epicgames_srs(self):
        config = {
            "DirectSites": ["geosite:epicgames"],
        }
        rules = build_rules(config)
        direct = next(r for r in rules if r.get("outbound") == "direct")
        self.assertIn(
            "https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/sing-box/epicgames.srs",
            direct["rule_set"],
        )
        self.assertNotIn("epic-games.srs", direct["rule_set"][0])

    def test_configs_tag_integrity(self):
        import glob
        import json
        data_files = {os.path.basename(p) for p in glob.glob(os.path.join(BASE_DIR, "data", "*"))}
        with open(os.path.join(BASE_DIR, "geoip", "config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)
        geoip_tags = set()
        for item in cfg.get("input", []):
            args = item.get("args", {})
            if "name" in args:
                geoip_tags.add(args["name"].lower())
            if "wantedList" in args:
                for k in args["wantedList"]:
                    geoip_tags.add(k.lower())

        json_paths = glob.glob(os.path.join(BASE_DIR, "HAPP", "*.JSON")) + \
                     glob.glob(os.path.join(BASE_DIR, "INCY", "*.JSON")) + \
                     glob.glob(os.path.join(BASE_DIR, "RELOCANT", "*.JSON"))

        for jp in json_paths:
            with open(jp, "r", encoding="utf-8") as jf:
                data = json.load(jf)
            for k in ("DirectSites", "ProxySites", "BlockSites"):
                for entry in data.get(k, []):
                    if entry.startswith("geosite:"):
                        tag = entry.split(":", 1)[1]
                        self.assertIn(tag, data_files, f"Unknown geosite tag '{tag}' in {jp}")
            for k in ("DirectIp", "ProxyIp", "BlockIp"):
                for entry in data.get(k, []):
                    if entry.startswith("geoip:"):
                        tag = entry.split(":", 1)[1].lower()
                        self.assertIn(tag, geoip_tags, f"Unknown geoip tag '{tag}' in {jp}")

    def test_data_no_duplicates(self):
        import glob
        for p in glob.glob(os.path.join(BASE_DIR, "data", "*")):
            with open(p, "r", encoding="utf-8") as f:
                lines = [l.strip().lower() for l in f if l.strip() and not l.strip().startswith("#")]
            seen = set()
            for l in lines:
                self.assertNotIn(l, seen, f"Duplicate entry '{l}' found in {os.path.basename(p)}")
                seen.add(l)

    def test_deeplink_and_autorouting_integrity(self):
        import glob
        import base64
        import json
        deeplink_files = glob.glob(os.path.join(BASE_DIR, "*", "*.DEEPLINK"))
        for dlf in deeplink_files:
            with open(dlf, "r", encoding="utf-8") as f:
                content = f.read().strip()
            self.assertTrue(content.startswith("happ://") or content.startswith("incy://"))
            prefix = "routing/onadd/"
            idx = content.find(prefix)
            self.assertNotEqual(idx, -1, f"Missing {prefix} in {dlf}")
            b64 = content[idx + len(prefix):]
            pad = len(b64) % 4
            if pad:
                b64 += "=" * (4 - pad)
            decoded_obj = json.loads(base64.b64decode(b64).decode("utf-8"))
            
            # Find matching JSON file
            dirname, fname = os.path.split(dlf)
            base_name = os.path.splitext(fname)[0]
            json_path = os.path.join(dirname, f"{base_name}.JSON")
            self.assertTrue(os.path.exists(json_path), f"Missing JSON pair for {dlf}")
            with open(json_path, "r", encoding="utf-8") as jf:
                source_obj = json.load(jf)
            self.assertEqual(decoded_obj, source_obj, f"Mismatch between {dlf} and {json_path}")

        autorouting_files = glob.glob(os.path.join(BASE_DIR, "*", "*.AUTOROUTING"))
        for arf in autorouting_files:
            with open(arf, "r", encoding="utf-8") as f:
                content = f.read().strip()
            self.assertTrue(content.startswith("incy://autorouting/onadd/https://cdn.jsdelivr.net/"))

    def test_remnawave_templates_integrity(self):
        import json
        sb_path = os.path.join(BASE_DIR, "ADDON_AUTOROUTING", "Remnawave", "singbox_subscription_template.json")
        with open(sb_path, "r", encoding="utf-8") as f:
            sb = json.load(f)
        self.assertIn("route", sb)
        self.assertIn("rules", sb["route"])
        self.assertIn("rule_set", sb["route"])
        rule_set_tags = {r["tag"] for r in sb["route"]["rule_set"]}
        self.assertIn("discord", rule_set_tags)
        self.assertIn("discord-ip", rule_set_tags)
        self.assertIn("ai", rule_set_tags)

        xray_path = os.path.join(BASE_DIR, "ADDON_AUTOROUTING", "Remnawave", "xray_location_template.json")
        with open(xray_path, "r", encoding="utf-8") as f:
            xray = json.load(f)
        self.assertIn("routing", xray)
        self.assertIn("rules", xray["routing"])
        proxy_rules = [r for r in xray["routing"]["rules"] if r.get("outboundTag") == "proxy"]
        proxy_domains = set()
        proxy_ips = set()
        for r in proxy_rules:
            if "domain" in r:
                proxy_domains.update(r["domain"])
            if "ip" in r:
                proxy_ips.update(r["ip"])
        self.assertIn("geosite:discord", proxy_domains)
        self.assertIn("geosite:ai", proxy_domains)
        self.assertIn("geoip:discord", proxy_ips)
        self.assertIn("geoip:telegram", proxy_ips)

    def test_mihomo_yaml_syntax_and_providers(self):
        import glob
        try:
            import yaml
        except ImportError:
            return
        yaml_files = glob.glob(os.path.join(BASE_DIR, "MIHOMO", "*.yaml")) + \
                     glob.glob(os.path.join(BASE_DIR, "RELOCANT", "*.yaml"))
        for yf in yaml_files:
            with open(yf, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            self.assertIsInstance(data, dict, f"Root not dict in {yf}")
            if "rule-providers" in data:
                for name, provider in data["rule-providers"].items():
                    url = provider.get("url", "")
                    self.assertTrue(url.startswith("https://cdn.jsdelivr.net/"), f"Invalid provider URL in {yf}: {url}")

    def test_dns_configurations_and_eof_prevention(self):
        import glob
        import json
        for folder in ("HAPP", "INCY", "RELOCANT"):
            for p in glob.glob(os.path.join(BASE_DIR, folder, "*.JSON")):
                with open(p, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                self.assertNotIn("common.dot.dns.yandex.net", str(cfg), f"Dead DoT endpoint in {p}")
                if "77.88.8.8" in cfg.get("DomesticDns", ""):
                    self.assertEqual(
                        cfg.get("DomesticDNSType"),
                        "DoU",
                        f"{p} has 77.88.8.8 with DomesticDNSType='{cfg.get('DomesticDNSType')}' (must be 'DoU' to prevent iOS EOF)",
                    )
                    self.assertEqual(
                        cfg.get("DomesticDNSDomain", ""),
                        "",
                        f"{p} should have empty DomesticDNSDomain for DoU",
                    )
                if cfg.get("RemoteDns") == "8.8.8.8" and cfg.get("RemoteDNSType") == "DoH":
                    self.assertEqual(
                        cfg.get("RemoteDNSDomain"),
                        "https://8.8.8.8/dns-query",
                        f"{p} must use IP-based DoH URL to avoid bootstrap deadlock",
                    )

    def test_connectivity_check_domains_and_whitelist_route_order(self):
        import json
        expected_latency_domains = [
            "domain:cp.cloudflare.com",
            "domain:connectivitycheck.gstatic.com",
            "domain:connectivitycheck.android.com",
            "domain:clients3.google.com",
            "domain:msftconnecttest.com",
            "domain:detectportal.firefox.com",
        ]
        for folder in ("HAPP", "INCY"):
            def_path = os.path.join(BASE_DIR, folder, "DEFAULT.JSON")
            with open(def_path, "r", encoding="utf-8") as f:
                def_cfg = json.load(f)
            self.assertEqual(def_cfg.get("RouteOrder"), "block-proxy-direct")
            for dom in expected_latency_domains:
                self.assertIn(dom, def_cfg.get("ProxySites", []), f"Missing {dom} in {def_path} ProxySites")

            wl_path = os.path.join(BASE_DIR, folder, "WHITELIST.JSON")
            with open(wl_path, "r", encoding="utf-8") as f:
                wl_cfg = json.load(f)
            self.assertEqual(
                wl_cfg.get("RouteOrder"),
                "block-direct-proxy",
                f"{wl_path} must have RouteOrder block-direct-proxy so non-whitelist traffic proxies",
            )

        for client in ("HAPP", "INCY"):
            rel_path = os.path.join(BASE_DIR, "RELOCANT", f"{client}.JSON")
            with open(rel_path, "r", encoding="utf-8") as f:
                rel_cfg = json.load(f)
            self.assertEqual(rel_cfg.get("RouteOrder"), "block-proxy-direct")
            for dom in expected_latency_domains:
                self.assertIn(dom, rel_cfg.get("ProxySites", []), f"Missing {dom} in {rel_path} ProxySites")

    def test_data_includes_integrity(self):
        import glob
        data_files = {os.path.basename(p) for p in glob.glob(os.path.join(BASE_DIR, "data", "*"))}
        for p in glob.glob(os.path.join(BASE_DIR, "data", "*")):
            with open(p, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    line = line.strip()
                    if line.startswith("include:"):
                        target = line.split(":", 1)[1].strip()
                        self.assertIn(
                            target,
                            data_files,
                            f"Missing include target '{target}' at {p}:{line_no}",
                        )

    def test_geoip_cidrs_validity(self):
        import glob
        import ipaddress
        for p in glob.glob(os.path.join(BASE_DIR, "geoip", "*.txt")):
            with open(p, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    try:
                        ipaddress.ip_network(line, strict=False)
                    except ValueError as e:
                        self.fail(f"Invalid CIDR '{line}' at {p}:{line_no}: {e}")

    def test_remnawave_singbox_rulesets_coherence(self):
        import json
        sb_path = os.path.join(BASE_DIR, "ADDON_AUTOROUTING", "Remnawave", "singbox_subscription_template.json")
        with open(sb_path, "r", encoding="utf-8") as f:
            sb = json.load(f)
        declared_rule_sets = {rs["tag"] for rs in sb.get("route", {}).get("rule_set", [])}
        for idx, rule in enumerate(sb.get("route", {}).get("rules", [])):
            refs = rule.get("rule_set", [])
            if isinstance(refs, str):
                refs = [refs]
            for r in refs:
                self.assertIn(r, declared_rule_sets, f"Rule #{idx} references undeclared rule_set '{r}' in {sb_path}")
        declared_dns = {s["tag"] for s in sb.get("dns", {}).get("servers", [])}
        for idx, dr in enumerate(sb.get("dns", {}).get("rules", [])):
            srv = dr.get("server")
            if srv:
                self.assertIn(srv, declared_dns, f"DNS rule #{idx} references undeclared server '{srv}' in {sb_path}")

    def test_apple_wallet_routing_and_priority(self):
        import json
        import glob

        # 1. Verify category-geoblock-ru has critical Apple Pay / Wallet domains
        geoblock_path = os.path.join(BASE_DIR, "data", "category-geoblock-ru")
        with open(geoblock_path, "r", encoding="utf-8") as f:
            geoblock_entries = {line.strip() for line in f if line.strip() and not line.startswith("#")}

        critical_domains = [
            "domain:wallet.apple.com",
            "domain:smp-device.apple.com",
            "domain:smp-device-content.apple.com",
            "domain:apple-pay-gateway.apple.com",
            "domain:paymentpass.apple.com",
            "domain:pass-services.apple.com",
            "domain:applepaycash.net",
            "domain:applewallet.com",
            "domain:pos-device.apple.com",
            "domain:smp-paymentservices.apple.com",
            "domain:applepay.cdn-apple.com",
            "domain:token.americanexpress.com",
            "domain:smoothpebble.apple.com",
            "domain:pds.apple.com",
            "domain:vts.visa.com",
            "domain:mdes.mastercard.com",
        ]
        for d in critical_domains:
            self.assertIn(d, geoblock_entries, f"Missing {d} in data/category-geoblock-ru")

        # 2. Verify HAPP and INCY prioritize ProxySites over DirectSites
        for folder in ("HAPP", "INCY"):
            manifest_path = os.path.join(BASE_DIR, folder, "DEFAULT.JSON")
            with open(manifest_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            self.assertEqual(cfg.get("RouteOrder"), "block-proxy-direct")
            self.assertIn("geosite:category-geoblock-ru", cfg.get("ProxySites", []))
            self.assertIn("geosite:apple", cfg.get("DirectSites", []))

        # 3. Verify Mihomo configs have explicit Apple Wallet proxy rules before apple direct rule
        for yf in [
            os.path.join(BASE_DIR, "MIHOMO", "default.yaml"),
            os.path.join(BASE_DIR, "MIHOMO", "template_remnawave.yaml"),
            os.path.join(BASE_DIR, "MIHOMO", "template_3x-ui.yaml"),
        ]:
            with open(yf, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("DOMAIN-KEYWORD,smp-device,PROXY", content, f"Missing smp-device keyword rule in {yf}")
            self.assertIn("DOMAIN-KEYWORD,smp-,PROXY", content, f"Missing smp- keyword rule in {yf}")
            self.assertIn("DOMAIN-KEYWORD,applepay,PROXY", content, f"Missing applepay keyword rule in {yf}")
            self.assertIn("DOMAIN,wallet.apple.com,PROXY", content, f"Missing wallet.apple.com rule in {yf}")
            self.assertIn("DOMAIN,pos-device.apple.com,PROXY", content, f"Missing pos-device rule in {yf}")
            self.assertIn("DOMAIN,smoothpebble.apple.com,PROXY", content, f"Missing smoothpebble rule in {yf}")
            idx_smp = content.find("DOMAIN-KEYWORD,smp-device,PROXY")
            idx_apple = content.find("RULE-SET,apple,DIRECT")
            self.assertGreater(idx_apple, idx_smp, f"Apple Wallet rules must precede RULE-SET,apple,DIRECT in {yf}")

        # 4. Verify Xray template routes category-geoblock-ru DNS to DoH ahead of Yandex DNS
        xray_path = os.path.join(BASE_DIR, "ADDON_AUTOROUTING", "Remnawave", "xray_location_template.json")
        with open(xray_path, "r", encoding="utf-8") as f:
            xray = json.load(f)
        dns_servers = xray.get("dns", {}).get("servers", [])
        doh_server = next((s for s in dns_servers if isinstance(s, dict) and "geosite:category-geoblock-ru" in s.get("domains", [])), None)
        self.assertIsNotNone(doh_server, "Missing DoH DNS server for category-geoblock-ru in xray_location_template.json")
        self.assertTrue(doh_server.get("address", "").startswith("https://"), "category-geoblock-ru DNS must use secure DoH")

    def test_data_no_redundant_subdomains(self):
        import glob
        for fpath in glob.glob(os.path.join(BASE_DIR, "data", "*")):
            if os.path.isdir(fpath) or os.path.basename(fpath) == "private":
                continue
            fname = os.path.basename(fpath)
            with open(fpath, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            domains = set()
            for l in lines:
                if l.startswith("domain:"):
                    domains.add(l[7:])
                elif not l.startswith("full:") and not l.startswith("regexp:") and not l.startswith("include:"):
                    domains.add(l)
            for d in domains:
                parts = d.split(".")
                for i in range(1, len(parts)):
                    parent = ".".join(parts[i:])
                    self.assertNotIn(
                        parent,
                        domains,
                        f"Subdomain '{d}' in {fname} is shadowed by parent domain '{parent}'",
                    )

    def test_mihomo_sniffer_apple_protection(self):
        try:
            import yaml
        except ImportError:
            yaml = None

        configs = [
            os.path.join(BASE_DIR, "MIHOMO", "default.yaml"),
            os.path.join(BASE_DIR, "MIHOMO", "template_remnawave.yaml"),
            os.path.join(BASE_DIR, "RELOCANT", "mihomo.yaml"),
        ]
        for cfg_path in configs:
            with open(cfg_path, "r", encoding="utf-8") as f:
                content = f.read()
            if yaml is not None:
                doc = yaml.safe_load(content)
                sniffer = doc.get("sniffer", {})
                self.assertTrue(sniffer.get("enable"), f"Sniffer not enabled in {cfg_path}")
                skip_domain = sniffer.get("skip-domain", [])
                self.assertIn("+.apple.com", skip_domain, f"Missing '+.apple.com' in sniffer.skip-domain of {cfg_path}")
            else:
                self.assertIn("sniffer:", content)
                self.assertIn("enable: true", content)
                self.assertIn("+.apple.com", content)

    def test_mihomo_torrent_clients_no_duplicates(self):
        try:
            import yaml
        except ImportError:
            yaml = None

        tc_path = os.path.join(BASE_DIR, "MIHOMO", "torrent-clients.yaml")
        with open(tc_path, "r", encoding="utf-8") as f:
            content = f.read()
        if yaml is not None:
            data = yaml.safe_load(content)
            payload = data.get("payload", [])
            seen = set()
            for item in payload:
                self.assertNotIn(item, seen, f"Duplicate entry '{item}' in {tc_path}")
                seen.add(item)
        else:
            lines = [l.strip() for l in content.splitlines() if l.strip().startswith("- ")]
            items = [l[2:].strip().strip("'\"") for l in lines]
            self.assertEqual(len(items), len(set(items)), f"Duplicate entries in {tc_path}")

    def test_google_play_fcm_not_proxied(self):
        gp_path = os.path.join(BASE_DIR, "data", "google-play")
        with open(gp_path, "r", encoding="utf-8") as f:
            gp_lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        self.assertNotIn("domain:mtalk.google.com", gp_lines, "mtalk.google.com must not be in google-play to avoid proxying FCM")

        ru_path = os.path.join(BASE_DIR, "data", "category-ru")
        with open(ru_path, "r", encoding="utf-8") as f:
            ru_lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        self.assertIn("domain:mtalk.google.com", ru_lines, "mtalk.google.com must be in category-ru for direct FCM push")

    def test_category_geoblock_ru_no_torrent_trackers(self):
        def parse_file(fname):
            doms = set()
            with open(os.path.join(BASE_DIR, "data", fname), "r", encoding="utf-8") as f:
                for l in f:
                    l = l.strip()
                    if not l or l.startswith("#") or l.startswith("include:"):
                        continue
                    if l.startswith("domain:"):
                        doms.add(l[7:].strip().lower())
                    elif not l.startswith("full:") and not l.startswith("regexp:"):
                        doms.add(l.strip().lower())
            return doms

        geoblock = parse_file("category-geoblock-ru")
        torrent = parse_file("torrent")
        overlap = geoblock & torrent
        self.assertEqual(overlap, set(), f"Torrent trackers found in category-geoblock-ru: {overlap}")

    def test_mihomo_torrent_priority_and_no_resolve(self):
        configs = [
            os.path.join(BASE_DIR, "MIHOMO", "default.yaml"),
            os.path.join(BASE_DIR, "MIHOMO", "template_remnawave.yaml"),
            os.path.join(BASE_DIR, "MIHOMO", "template_3x-ui.yaml"),
        ]
        for cfg_path in configs:
            with open(cfg_path, "r", encoding="utf-8") as f:
                content = f.read()
            idx_torrent = content.find("RULE-SET,torrent-domains,DIRECT")
            idx_geoblock = content.find("RULE-SET,category-geoblock-ru,PROXY")
            self.assertNotEqual(idx_torrent, -1, f"Missing torrent-domains in {cfg_path}")
            self.assertNotEqual(idx_geoblock, -1, f"Missing category-geoblock-ru in {cfg_path}")
            self.assertLess(
                idx_torrent,
                idx_geoblock,
                f"torrent-domains must precede category-geoblock-ru in {cfg_path} to prevent torrent proxy leaks",
            )
            # Ensure direct-ips has no-resolve
            self.assertIn("RULE-SET,direct-ips,DIRECT,no-resolve", content, f"direct-ips must use no-resolve in {cfg_path}")

    def test_shadowrocket_generation_and_rules(self):
        from tools.shadowrocket.generate_shadowrocket import parse_geosite_rule, build_all_shadowrocket
        self.assertEqual(parse_geosite_rule("domain:example.com"), "DOMAIN-SUFFIX,example.com")
        self.assertEqual(parse_geosite_rule("full:example.com @attr"), "DOMAIN,example.com")
        self.assertEqual(parse_geosite_rule("keyword:test # note"), "DOMAIN-KEYWORD,test")
        self.assertIsNone(parse_geosite_rule("regexp:^pattern.*$"))
        self.assertIsNone(parse_geosite_rule("# only comment"))

        stats = build_all_shadowrocket(verbose=False)
        self.assertIn("domain:category-geoblock-ru", stats)
        self.assertIn("ip:discord-ips", stats)
        self.assertIn("ip:whitelist-ips", stats)

        sr_default = os.path.join(BASE_DIR, "SHADOWROCKET", "DEFAULT.CONF")
        self.assertTrue(os.path.exists(sr_default), "SHADOWROCKET/DEFAULT.CONF missing")
        with open(sr_default, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("dns.quad9.net", content)
        self.assertIn("dns.yandex.ru", content)
        self.assertNotIn("common.dot.dns.yandex.net", content)
        self.assertIn("lkfl2.nalog.ru = 213.24.64.175", content)
        self.assertIn("rules/category-ads.list,REJECT", content)
        self.assertIn("rules/discord.list,PROXY", content)
        self.assertIn("rules/discord-ips.list,PROXY", content)
        self.assertIn("GEOIP,RU,DIRECT", content)
        self.assertIn("FINAL,PROXY", content)

        # Verify include: directive expansion
        ads_all = os.path.join(BASE_DIR, "SHADOWROCKET", "rules", "category-ads-all.list")
        self.assertTrue(os.path.exists(ads_all))
        with open(ads_all, "r", encoding="utf-8") as f:
            ads_content = f.read()
        self.assertIn("DOMAIN-SUFFIX,adfox.yandex.ru", ads_content)
        self.assertGreater(stats.get("domain:category-ads-all", 0), 0)

        ai_list = os.path.join(BASE_DIR, "SHADOWROCKET", "rules", "ai.list")
        self.assertTrue(os.path.exists(ai_list))
        with open(ai_list, "r", encoding="utf-8") as f:
            ai_content = f.read()
        self.assertIn("DOMAIN-SUFFIX,deepmind.google", ai_content)
        self.assertIn("DOMAIN-SUFFIX,openai.com", ai_content)

    def test_marzban_and_marzneshin_subscription_helpers(self):
        """Test version parsing and KoridorResolver caching in ADDON_AUTOROUTING."""
        from unittest.mock import MagicMock, patch

        import sys
        for addon in ("Marzban", "Marzneshin"):
            sub_path = os.path.join(BASE_DIR, "ADDON_AUTOROUTING", addon, "subscription.py")
            self.assertTrue(os.path.exists(sub_path), f"{sub_path} missing")
            with open(sub_path, "r", encoding="utf-8") as f:
                lines = []
                for line in f:
                    if line.startswith("from fastapi") or line.startswith("from app."):
                        break
                    lines.append(line)
            ns = {}
            mock_requests = MagicMock()
            with patch.dict(sys.modules, {"requests": mock_requests}):
                exec("".join(lines), ns)

            # Test version functions if present
            if "_version_tuple" in ns and "_version_at_least" in ns:
                _version_tuple = ns["_version_tuple"]
                _version_at_least = ns["_version_at_least"]
                self.assertEqual(_version_tuple("1.8.29"), (1, 8, 29))
                self.assertEqual(_version_tuple("v2.0.1-beta"), (2, 0, 1, 0))
                self.assertTrue(_version_at_least("1.8.29", "1.8.0"))
                self.assertTrue(_version_at_least("2.0.0", "1.9.9"))
                self.assertFalse(_version_at_least("1.7.9", "1.8.0"))

            # Test _KoridorResolver
            _KoridorResolver = ns["_KoridorResolver"]
            # 1. Custom override via source
            with patch.dict(os.environ, {"KORIDOR_ROUTING_SOURCE": "custom", "KORIDOR_ROUTING_CUSTOM": "happ://custom-url"}):
                resolver = _KoridorResolver("default")
                self.assertEqual(resolver.get(), "happ://custom-url")

            # 2. HTTP fetch and caching
            mock_resp = MagicMock()
            mock_resp.text = "happ://routing/onadd/test-deeplink\n"
            mock_requests.get.reset_mock()
            mock_requests.get.return_value = mock_resp
            with patch.dict(os.environ, {"KORIDOR_ROUTING_SOURCE": "default", "KORIDOR_ROUTING_CUSTOM": ""}):
                resolver = _KoridorResolver("default")
                val1 = resolver.get()
                self.assertEqual(val1, "happ://routing/onadd/test-deeplink")
                # Second call should use cache without HTTP request
                val2 = resolver.get()
                self.assertEqual(val2, "happ://routing/onadd/test-deeplink")
                self.assertEqual(mock_requests.get.call_count, 1)

    def test_check_dead_domains_parser(self):
        from tools.check_dead_domains import clean_domain
        self.assertEqual(clean_domain("domain:example.com"), "example.com")
        self.assertEqual(clean_domain("full:Sub.EXAMPLE.COM @ads # comment"), "sub.example.com")
        self.assertIsNone(clean_domain("keyword:google"))
        self.assertIsNone(clean_domain("regexp:.*google.*"))
        self.assertIsNone(clean_domain("# just comment"))

    def test_discord_bulletproof_routing(self):
        """Verify Discord failsafe rules across Mihomo, Sing-box, Xray, and Shadowrocket."""
        # 1. Mihomo configs
        mihomo_files = [
            os.path.join(BASE_DIR, "MIHOMO", "default.yaml"),
            os.path.join(BASE_DIR, "MIHOMO", "template_remnawave.yaml"),
            os.path.join(BASE_DIR, "MIHOMO", "template_3x-ui.yaml"),
        ]
        for mf in mihomo_files:
            with open(mf, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("AND,((NETWORK,UDP),(DST-PORT,19294-19344)),💬 Discord", content, f"Missing UDP 19294-19344 in {mf}")
            self.assertIn("webcord", content, f"Missing webcord in {mf}")
            self.assertIn("vesktop", content, f"Missing vesktop in {mf}")

        # 2. Sing-box template
        sb_path = os.path.join(BASE_DIR, "ADDON_AUTOROUTING", "Remnawave", "singbox_subscription_template.json")
        with open(sb_path, "r", encoding="utf-8") as f:
            import json
            sb = json.load(f)
        rules = sb.get("route", {}).get("rules", [])
        has_discord_port = any(
            r.get("network") == "udp" and "19294:19344" in r.get("port_range", []) and r.get("outbound") == "→ Remnawave"
            for r in rules
        )
        self.assertTrue(has_discord_port, "Missing Discord UDP port_range 19294:19344 rule in Sing-box template")

        # 3. Xray template
        xray_path = os.path.join(BASE_DIR, "ADDON_AUTOROUTING", "Remnawave", "xray_location_template.json")
        with open(xray_path, "r", encoding="utf-8") as f:
            xray = json.load(f)
        xrules = xray.get("routing", {}).get("rules", [])
        has_xray_port = any(
            r.get("network") == "udp" and r.get("port") == "19294-19344" and r.get("outboundTag") == "proxy"
            for r in xrules
        )
        self.assertTrue(has_xray_port, "Missing Discord UDP port 19294-19344 in Xray template")

        # 4. Shadowrocket configs
        sr_files = [
            os.path.join(BASE_DIR, "SHADOWROCKET", "DEFAULT.CONF"),
            os.path.join(BASE_DIR, "SHADOWROCKET", "WHITELIST.CONF"),
        ]
        for srf in sr_files:
            with open(srf, "r", encoding="utf-8") as f:
                sr_content = f.read()
            self.assertIn("DEST-PORT,19294-19344,PROXY", sr_content, f"Missing DEST-PORT,19294-19344,PROXY in {srf}")

        # 5. GeoIP CIDR full Cloudflare Anycast edge
        with open(os.path.join(BASE_DIR, "geoip", "discord.txt"), "r", encoding="utf-8") as f:
            discord_cidrs = f.read()
        self.assertIn("162.159.128.0/19", discord_cidrs, "Missing 162.159.128.0/19 in geoip/discord.txt")

    def test_no_cross_action_domain_overlaps(self):
        """Ensure Direct categories do not share exact domains with Proxy or Block categories."""
        def parse_category(fname):
            doms = set()
            with open(os.path.join(BASE_DIR, "data", fname), "r", encoding="utf-8") as f:
                for line in f:
                    s = line.strip()
                    if not s or s.startswith("#") or s.startswith("include:") or s.startswith("regexp:"):
                        continue
                    for pfx in ("domain:", "full:", "keyword:"):
                        if s.startswith(pfx):
                            s = s[len(pfx):]
                            break
                    doms.add(s.strip(". ").lower())
            return doms

        direct_cats = ("category-ru", "whitelist", "epicgames", "steam", "riot", "escapefromtarkov", "origin", "faceit", "microsoft")
        proxy_cats = ("category-geoblock-ru", "google-play", "discord", "telegram", "youtube", "ai", "google-deepmind")
        block_cats = ("category-ads", "win-spy", "torrent")

        direct_union = set().union(*(parse_category(c) for c in direct_cats))
        proxy_union = set().union(*(parse_category(c) for c in proxy_cats))
        block_union = set().union(*(parse_category(c) for c in block_cats))

        self.assertEqual(
            direct_union & proxy_union,
            set(),
            f"Direct and Proxy categories have overlapping domains: {direct_union & proxy_union}",
        )
        self.assertEqual(
            direct_union & block_union,
            set(),
            f"Direct and Block categories have overlapping domains: {direct_union & block_union}",
        )

    def test_mihomo_payload_files_no_duplicates(self):
        """Ensure MIHOMO/games.yaml, ru-apps.yaml, and torrent-clients.yaml have no duplicate entries."""
        for fname in ("games.yaml", "ru-apps.yaml", "torrent-clients.yaml"):
            fpath = os.path.join(BASE_DIR, "MIHOMO", fname)
            items = []
            with open(fpath, "r", encoding="utf-8") as f:
                for line in f:
                    s = line.strip()
                    if s.startswith("- "):
                        items.append(s)
            self.assertEqual(len(items), len(set(items)), f"Duplicate entries found in MIHOMO/{fname}")


if __name__ == "__main__":
    unittest.main()


