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
        self.assertEqual(v2["domainStrategy"], "AsIs")
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


if __name__ == "__main__":
    unittest.main()
