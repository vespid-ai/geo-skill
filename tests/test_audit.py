import contextlib
import functools
import http.server
import io
import tempfile
import threading
import unittest
from pathlib import Path

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
            self.assertEqual(result.warn_count, 1)  # llms.txt missing

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
            self.assertEqual(result.warn_count, 0)


if __name__ == "__main__":
    unittest.main()
