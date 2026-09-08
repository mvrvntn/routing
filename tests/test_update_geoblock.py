#!/usr/bin/env python3
"""
Unit and regression test suite for scripts/update_geoblock.py
Covers:
1. clean_domain_string (normalization, prefixes, URLs, ports)
2. is_valid_domain (RFC 1035, rejection of IPs and malformed strings)
3. is_protected_domain (Safety Gate: .ru, .рф, .su, whitelist hierarchy)
4. prune_redundant_subdomains (domain collapsing without losing root targets)
5. fetch_single_url with mocked async network responses (timeouts, HTTP errors)
6. Atomic file writing and rollback protection
"""

import sys
import unittest
import asyncio
from pathlib import Path
from unittest.mock import patch

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.update_geoblock import (
    clean_domain_string,
    is_valid_domain,
    is_protected_domain,
    prune_redundant_subdomains,
    fetch_single_url,
    async_main,
)


class TestDomainSanitization(unittest.TestCase):
    """Test cleaning and normalization of raw input strings."""

    def test_strip_prefixes(self):
        self.assertEqual(clean_domain_string("domain:example.com"), "example.com")
        self.assertEqual(clean_domain_string("full:sub.example.com"), "sub.example.com")
        self.assertEqual(clean_domain_string("keyword:badword"), "badword")

    def test_strip_urls_ports_and_paths(self):
        self.assertEqual(clean_domain_string("https://example.com/api/v1?token=123"), "example.com")
        self.assertEqual(clean_domain_string("http://tracker.torrent.org:8080/announce"), "tracker.torrent.org")
        self.assertEqual(clean_domain_string("  EXAMPLE.COM.  "), "example.com")

    def test_ignore_comments_and_empty(self):
        self.assertEqual(clean_domain_string(""), "")
        self.assertEqual(clean_domain_string("   "), "")
        self.assertEqual(clean_domain_string("# This is a comment"), "")
        self.assertEqual(clean_domain_string("#domain:test.com"), "")


class TestDomainValidation(unittest.TestCase):
    """Test RFC 1035 domain syntax validation."""

    def test_valid_domains(self):
        self.assertTrue(is_valid_domain("discord.com"))
        self.assertTrue(is_valid_domain("api.openai.com"))
        self.assertTrue(is_valid_domain("sub-domain.co.uk"))
        self.assertTrue(is_valid_domain("x.ai"))

    def test_reject_ip_addresses(self):
        self.assertFalse(is_valid_domain("1.1.1.1"))
        self.assertFalse(is_valid_domain("192.168.1.1"))
        self.assertFalse(is_valid_domain("10.0.0.1/32"))

    def test_reject_malformed(self):
        self.assertFalse(is_valid_domain("invalid_char$.com"))
        self.assertFalse(is_valid_domain("nodots"))
        self.assertFalse(is_valid_domain(".startswithdot.com"))
        self.assertFalse(is_valid_domain("a" * 255 + ".com"))


class TestSafetyGate(unittest.TestCase):
    """Test strict protection of Russian services, banks, and whitelisted domains."""

    def setUp(self):
        self.protected = {
            "gosuslugi.ru",
            "sberbank.ru",
            "tbank.ru",
            "custom-white.com",
        }

    def test_blocks_national_tlds(self):
        self.assertTrue(is_protected_domain("mail.ru", self.protected))
        self.assertTrue(is_protected_domain("сайт.рф", self.protected))
        self.assertTrue(is_protected_domain("old.su", self.protected))
        self.assertTrue(is_protected_domain("gov.xn--p1ai", self.protected))

    def test_blocks_protected_subdomains(self):
        self.assertTrue(is_protected_domain("online.sberbank.ru", self.protected))
        self.assertTrue(is_protected_domain("api.sub.custom-white.com", self.protected))

    def test_allows_foreign_unprotected_services(self):
        self.assertFalse(is_protected_domain("discord.com", self.protected))
        self.assertFalse(is_protected_domain("openai.com", self.protected))
        self.assertFalse(is_protected_domain("notion.so", self.protected))
        self.assertFalse(is_protected_domain("spotify.com", self.protected))


class TestSubdomainPruning(unittest.TestCase):
    """Test memory-optimizing domain collapsing without losing coverage."""

    def test_collapsing_redundant_children(self):
        domains = {
            "discord.com",
            "gateway.discord.com",
            "cdn.discord.com",
            "api.discord.com",
            "other.org",
        }
        pruned = prune_redundant_subdomains(domains)
        self.assertEqual(pruned, {"discord.com", "other.org"})

    def test_deep_hierarchy_collapsing(self):
        domains = {
            "root.io",
            "a.root.io",
            "b.a.root.io",
            "c.b.a.root.io",
        }
        pruned = prune_redundant_subdomains(domains)
        self.assertEqual(pruned, {"root.io"})

    def test_preserves_independent_domains(self):
        domains = {"example.com", "notexample.com", "sub.different.com"}
        pruned = prune_redundant_subdomains(domains)
        self.assertEqual(pruned, domains)


class TestNetworkIsolationAndMocks(unittest.IsolatedAsyncioTestCase):
    """Test async network fetching with zero live network calls."""

    @patch("scripts.update_geoblock._sync_fetch")
    async def test_successful_fetch(self, mock_fetch):
        mock_fetch.return_value = "chatgpt.com\ninstagram.com\n1.2.3.4\n# comment\n"
        result = await fetch_single_url("https://mock.url/domains.lst", timeout=5)
        self.assertEqual(result, {"chatgpt.com", "instagram.com"})

    @patch("scripts.update_geoblock._sync_fetch")
    async def test_timeout_fallback(self, mock_fetch):
        mock_fetch.side_effect = TimeoutError("Socket timed out")
        result = await fetch_single_url("https://mock.url/timeout.lst", timeout=1)
        self.assertEqual(result, set())


class TestAtomicWriteAndRollback(unittest.TestCase):
    """Test transactional atomic file writing and rollback on error."""

    def test_rollback_on_failure(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "test_geoblock"
            target.write_text("domain:initial.com\n", encoding="utf-8")

            # Patch load functions to provide minimal data
            with patch("scripts.update_geoblock.load_protected_domains", return_value=set()), \
                 patch("scripts.update_geoblock.load_baseline_geoblock", return_value={"initial.com"}), \
                 patch("scripts.update_geoblock.fetch_all_community_domains", return_value=set()):

                # Simulate disk write failure
                with patch("builtins.open", side_effect=OSError("Disk write error")):
                    with self.assertRaises(OSError):
                        asyncio.run(async_main(geoblock_file=target, community_urls=[]))

            # Ensure .tmp is cleaned up and original file intact
            tmp_file = target.with_suffix(".tmp")
            self.assertFalse(tmp_file.exists())
            self.assertEqual(target.read_text(encoding="utf-8"), "domain:initial.com\n")


if __name__ == "__main__":
    unittest.main()
