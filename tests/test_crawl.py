import unittest
from pathlib import Path
from unittest import mock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import geolib as G
import crawl


class FakeResp:
    """模拟 requests.get 的流式响应，够 fetch 用即可。"""

    def __init__(self, status, body=b"<html>ok</html>", ctype="text/html"):
        self.status_code = status
        self.headers = {"Content-Type": ctype}
        self.url = "http://x.test/"
        self._body = body
        self.encoding = "utf-8"

    def iter_content(self, n):
        yield self._body

    def close(self):
        pass


class TestFetchRetry(unittest.TestCase):
    def _run(self, responses, retries=1):
        with mock.patch.object(G.requests, "get", side_effect=responses) as get, \
             mock.patch.object(G.time, "sleep"):
            res = G.fetch("http://x.test/", retries=retries)
        return res, get.call_count

    def test_retry_500_then_200(self):
        res, calls = self._run([FakeResp(500), FakeResp(200)])
        self.assertEqual(res["status"], 200)
        self.assertEqual(calls, 2)

    def test_retry_429(self):
        res, calls = self._run([FakeResp(429), FakeResp(200)])
        self.assertEqual(res["status"], 200)
        self.assertEqual(calls, 2)

    def test_no_retry_404(self):
        res, calls = self._run([FakeResp(404)])
        self.assertEqual(res["status"], 404)
        self.assertEqual(calls, 1)

    def test_retry_exhausted_returns_last(self):
        res, calls = self._run([FakeResp(500), FakeResp(500)])
        self.assertEqual(res["status"], 500)
        self.assertEqual(calls, 2)

    def test_403_falls_back_to_browser_ua(self):
        with mock.patch.object(G.requests, "get",
                               side_effect=[FakeResp(403), FakeResp(200)]) as get, \
             mock.patch.object(G.time, "sleep"):
            res = G.fetch("http://x.test/", retries=0)
        self.assertEqual(res["status"], 200)
        self.assertTrue(res["ua_fallback"])
        uas = [c.kwargs["headers"]["User-Agent"] for c in get.call_args_list]
        self.assertIn("geo-skill", uas[0])
        self.assertNotIn("geo-skill", uas[1])

    def test_403_on_both_uas_returns_403(self):
        with mock.patch.object(G.requests, "get",
                               side_effect=[FakeResp(403), FakeResp(403)]) as get, \
             mock.patch.object(G.time, "sleep"):
            res = G.fetch("http://x.test/", retries=0)
        self.assertEqual(res["status"], 403)
        self.assertEqual(get.call_count, 2)

    def test_explicit_ua_never_falls_back(self):
        with mock.patch.object(G.requests, "get", side_effect=[FakeResp(403)]) as get, \
             mock.patch.object(G.time, "sleep"):
            res = G.fetch("http://x.test/", retries=0, ua="AI-Bot/1.0")
        self.assertEqual(res["status"], 403)
        self.assertEqual(get.call_count, 1)


class TestCrawlHealth(unittest.TestCase):
    def _pages(self, statuses):
        return [{"status": s} for s in statuses]

    def test_all_dead_dies(self):
        with self.assertRaises(SystemExit):
            crawl.check_crawl_health(self._pages([0, 0, 0]))

    def test_low_ok_ratio_dies(self):
        with self.assertRaises(SystemExit):
            crawl.check_crawl_health(self._pages([200] + [0] * 9))

    def test_healthy_passes(self):
        crawl.check_crawl_health(self._pages([200] * 5))

    def test_failure_hint_names_waf_on_403(self):
        hint = crawl._crawl_failure_hint([{"status": 403}] * 5)
        self.assertIn("HTTP 403×5", hint)
        self.assertIn("WAF", hint)

    def test_failure_hint_names_tls_on_sslerror(self):
        hint = crawl._crawl_failure_hint(
            [{"status": 0, "error": "SSLError: certificate verify failed"}] * 3)
        self.assertIn("证书", hint)
        self.assertIn("SSLError", hint)
        crawl.check_crawl_health(self._pages([200] + [0] * 4))  # 20% 刚好达标


class TestWordCountKana(unittest.TestCase):
    def test_pure_kana_counts(self):
        self.assertGreater(G.word_count("これはテストです"), 0)

    def test_cjk_unchanged(self):
        self.assertGreater(G.word_count("这是一个测试"), 0)


if __name__ == "__main__":
    unittest.main()
