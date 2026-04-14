import tempfile
import unittest
from pathlib import Path

from geo_skill.audit import audit_site


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


if __name__ == "__main__":
    unittest.main()
