import functools
import http.server
import tempfile
import threading
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from geo_skill.audit import audit_site, audit_url


class AuditTests(unittest.TestCase):
    def test_audit_site_reports_basics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
            (root / "sitemap.xml").write_text("<urlset></urlset>", encoding="utf-8")
            (root / "index.html").write_text(
                """
                <html>
                  <head>
                    <title>Example</title>
                    <meta name="description" content="example" />
                    <meta property="og:title" content="Example" />
                    <script type="application/ld+json">{}</script>
                  </head>
                  <body>
                    <h1>FAQ</h1>
                  </body>
                </html>
                """,
                encoding="utf-8",
            )
            result = audit_site(root)
            self.assertEqual(result.fail_count, 0)
            self.assertGreaterEqual(result.pass_count, 6)
            self.assertTrue(any(item.message == "llms.txt missing" for item in result.findings))

    def test_audit_site_reports_page_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
            (root / "sitemap.xml").write_text("<urlset></urlset>", encoding="utf-8")
            (root / "llms.txt").write_text("# Example\n", encoding="utf-8")
            (root / "index.html").write_text(
                "<html lang='en'><head><title>Example</title><meta name='description' content='example'><meta property='og:title' content='Example'><script type='application/ld+json'>{}</script></head><body><h1>FAQ</h1></body></html>",
                encoding="utf-8",
            )
            for relative in [
                "pricing/index.html",
                "docs/index.html",
                "features/live-audit/index.html",
                "about/index.html",
                "changelog/index.html",
            ]:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"<html><head><title>{relative}</title></head><body>{relative}</body></html>", encoding="utf-8")
            payload = audit_site(root).to_dict()
            self.assertTrue(payload["coverage"]["homepage"]["present"])
            self.assertTrue(payload["coverage"]["feature"]["present"])
            self.assertTrue(payload["coverage"]["pricing"]["present"])
            self.assertTrue(payload["coverage"]["docs"]["present"])
            self.assertTrue(payload["coverage"]["trust"]["present"])
            self.assertTrue(payload["coverage"]["changelog"]["present"])

    def test_audit_url_reports_live_basics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
            (root / "sitemap.xml").write_text("<urlset></urlset>", encoding="utf-8")
            (root / "llms.txt").write_text("# Example\n", encoding="utf-8")
            (root / "index.html").write_text(
                """
                <html lang="en">
                  <head>
                    <title>Live Example</title>
                    <link rel="canonical" href="http://localhost/example" />
                    <meta name="description" content="live example" />
                    <meta property="og:title" content="Live Example" />
                    <script type="application/ld+json">{"@context": "https://schema.org"}</script>
                  </head>
                  <body>
                    <h1>FAQ</h1>
                  </body>
                </html>
                """,
                encoding="utf-8",
            )
            handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                url = f"http://127.0.0.1:{server.server_port}/index.html"
                result = audit_url(url)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)
            self.assertEqual(result.fail_count, 0)
            self.assertGreaterEqual(result.pass_count, 8)
            payload = result.to_dict()
            self.assertTrue(payload["coverage"]["homepage"]["present"])
            self.assertTrue(payload["coverage"]["faq"]["present"])

    def test_audit_url_uses_sitemap_for_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sitemap = """<?xml version='1.0' encoding='UTF-8'?>
            <urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>
              <url><loc>http://127.0.0.1:9/</loc></url>
              <url><loc>http://127.0.0.1:9/pricing/</loc></url>
              <url><loc>http://127.0.0.1:9/docs/</loc></url>
              <url><loc>http://127.0.0.1:9/security/</loc></url>
              <url><loc>http://127.0.0.1:9/changelog/</loc></url>
            </urlset>
            """
            (root / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
            (root / "sitemap.xml").write_text(sitemap, encoding="utf-8")
            (root / "llms.txt").write_text("# Example\n", encoding="utf-8")
            (root / "index.html").write_text(
                "<html lang='en'><head><title>Live Example</title><meta name='description' content='live example'><meta property='og:title' content='Live Example'><link rel='canonical' href='https://example.com'><script type='application/ld+json'>{}</script></head><body><h1>FAQ</h1></body></html>",
                encoding="utf-8",
            )
            handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                port = server.server_port
                sitemap_text = sitemap.replace("127.0.0.1:9", f"127.0.0.1:{port}")
                (root / "sitemap.xml").write_text(sitemap_text, encoding="utf-8")
                url = f"http://127.0.0.1:{port}/index.html"
                payload = audit_url(url).to_dict()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)
            self.assertTrue(payload["coverage"]["pricing"]["present"])
            self.assertTrue(payload["coverage"]["docs"]["present"])
            self.assertTrue(payload["coverage"]["trust"]["present"])
            self.assertTrue(payload["coverage"]["changelog"]["present"])

    def test_audit_url_follows_final_origin_after_redirect(self):
        with tempfile.TemporaryDirectory() as tmp:
            content_root = Path(tmp) / "content"
            content_root.mkdir(parents=True, exist_ok=True)
            (content_root / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
            (content_root / "sitemap.xml").write_text("<urlset></urlset>", encoding="utf-8")
            (content_root / "llms.txt").write_text("# Example\n", encoding="utf-8")
            (content_root / "index.html").write_text(
                "<html lang='en'><head><title>Redirect Target</title><meta name='description' content='redirect target'><meta property='og:title' content='Redirect Target'><link rel='canonical' href='https://example.com'><script type='application/ld+json'>{}</script></head><body><h1>FAQ</h1></body></html>",
                encoding="utf-8",
            )

            content_handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(content_root))
            content_server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), content_handler)
            content_thread = threading.Thread(target=content_server.serve_forever, daemon=True)
            content_thread.start()

            redirect_target = f"http://127.0.0.1:{content_server.server_port}/index.html"

            class RedirectHandler(http.server.BaseHTTPRequestHandler):
                def do_GET(self):
                    if self.path == "/start":
                        self.send_response(302)
                        self.send_header("Location", redirect_target)
                        self.end_headers()
                        return
                    self.send_response(404)
                    self.end_headers()

                def log_message(self, format, *args):
                    return

            redirect_server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), RedirectHandler)
            redirect_thread = threading.Thread(target=redirect_server.serve_forever, daemon=True)
            redirect_thread.start()
            try:
                result = audit_url(f"http://127.0.0.1:{redirect_server.server_port}/start")
            finally:
                redirect_server.shutdown()
                redirect_server.server_close()
                redirect_thread.join(timeout=5)
                content_server.shutdown()
                content_server.server_close()
                content_thread.join(timeout=5)

            resource_messages = [item.message for item in result.findings if item.message.startswith(("robots.txt", "sitemap.xml", "llms.txt"))]
            self.assertTrue(all(f":{content_server.server_port}/" in message for message in resource_messages if "reachable at" in message))
            self.assertFalse(any("returned HTTP" in message for message in resource_messages))

    def test_audit_url_expands_sitemap_index_without_misclassifying_sitemap_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sitemap_index = """<?xml version='1.0' encoding='UTF-8'?>
            <sitemapindex xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>
              <sitemap><loc>http://127.0.0.1:9/docs-sitemap.xml</loc></sitemap>
              <sitemap><loc>http://127.0.0.1:9/pricing-sitemap.xml</loc></sitemap>
            </sitemapindex>
            """
            docs_sitemap = """<?xml version='1.0' encoding='UTF-8'?>
            <urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>
              <url><loc>http://127.0.0.1:9/docs/</loc></url>
            </urlset>
            """
            empty_sitemap = """<?xml version='1.0' encoding='UTF-8'?>
            <urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'></urlset>
            """
            (root / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
            (root / "sitemap.xml").write_text(sitemap_index, encoding="utf-8")
            (root / "docs-sitemap.xml").write_text(docs_sitemap, encoding="utf-8")
            (root / "pricing-sitemap.xml").write_text(empty_sitemap, encoding="utf-8")
            (root / "llms.txt").write_text("# Example\n", encoding="utf-8")
            (root / "index.html").write_text(
                "<html lang='en'><head><title>Live Example</title><meta name='description' content='live example'><meta property='og:title' content='Live Example'><link rel='canonical' href='https://example.com'><script type='application/ld+json'>{}</script></head><body><h1>FAQ</h1></body></html>",
                encoding="utf-8",
            )
            handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                port = server.server_port
                (root / "sitemap.xml").write_text(sitemap_index.replace("127.0.0.1:9", f"127.0.0.1:{port}"), encoding="utf-8")
                (root / "docs-sitemap.xml").write_text(docs_sitemap.replace("127.0.0.1:9", f"127.0.0.1:{port}"), encoding="utf-8")
                url = f"http://127.0.0.1:{port}/index.html"
                payload = audit_url(url).to_dict()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)
            self.assertTrue(payload["coverage"]["docs"]["present"])
            self.assertFalse(payload["coverage"]["pricing"]["present"])


if __name__ == "__main__":
    unittest.main()
