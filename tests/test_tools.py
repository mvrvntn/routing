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


if __name__ == "__main__":
    unittest.main()
