import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from geo_skill.cli import main
from geo_skill.skills import list_skills


class CliTests(unittest.TestCase):
    def test_skills_list(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main(["skills", "list", "--agent", "hermes"])
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn("openai-chatgpt-search", output)
        self.assertIn("geo-faq-coverage", output)
        self.assertIn("[hermes]", output)
        first_line = output.splitlines()[0]
        self.assertIn("\t", first_line)
        self.assertNotIn("\\t", first_line)

    def test_generate_robots(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main(["generate", "robots", "--domain", "https://example.com"])
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn("OAI-SearchBot", output)
        self.assertIn("Bytespider", output)
        self.assertIn("Disallow: /", output)

    def test_generate_software_application_schema(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main([
                "generate",
                "schema",
                "software-application",
                "--name",
                "Geo Skill",
                "--url",
                "https://example.com",
                "--summary",
                "GEO automation toolkit",
                "--category",
                "BusinessApplication",
                "--operating-system",
                "Web",
            ])
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn('"@context": "https://schema.org"', output)
        self.assertIn('"@type": "SoftwareApplication"', output)
        self.assertIn('"name": "Geo Skill"', output)

    def test_generate_product_schema(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main([
                "generate",
                "schema",
                "product",
                "--name",
                "Geo Skill Cloud",
                "--url",
                "https://example.com/product",
                "--summary",
                "Managed GEO workflow platform",
                "--brand",
                "vespid-ai",
                "--price",
                "99",
            ])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["@type"], "Product")
        self.assertEqual(payload["brand"]["name"], "vespid-ai")
        self.assertEqual(payload["offers"]["price"], "99")

    def test_generate_organization_schema(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main([
                "generate",
                "schema",
                "organization",
                "--name",
                "vespid-ai",
                "--url",
                "https://vespid.ai",
                "--description",
                "Agent infrastructure and GEO tooling",
                "--same-as",
                "https://github.com/vespid-ai",
                "--same-as",
                "https://x.com/vespid_ai",
            ])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["@type"], "Organization")
        self.assertEqual(len(payload["sameAs"]), 2)
        self.assertEqual(payload["url"], "https://vespid.ai")

    def test_generate_website_schema(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main([
                "generate",
                "schema",
                "website",
                "--name",
                "Geo Skill",
                "--url",
                "https://example.com",
                "--description",
                "Operational GEO toolkit",
                "--search-url-template",
                "https://example.com/search?q={search_term_string}",
            ])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["@type"], "WebSite")
        self.assertEqual(payload["url"], "https://example.com")
        self.assertIn("potentialAction", payload)

    def test_generate_website_schema_skips_search_action_by_default(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main([
                "generate",
                "schema",
                "website",
                "--name",
                "Geo Skill",
                "--url",
                "https://example.com",
                "--description",
                "Operational GEO toolkit",
            ])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["@type"], "WebSite")
        self.assertNotIn("potentialAction", payload)

    def test_generate_breadcrumb_schema(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main([
                "generate",
                "schema",
                "breadcrumb",
                "--item",
                "Home::https://example.com",
                "--item",
                "Docs::https://example.com/docs",
                "--item",
                "API::https://example.com/docs/api",
            ])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["@type"], "BreadcrumbList")
        self.assertEqual(len(payload["itemListElement"]), 3)
        self.assertEqual(payload["itemListElement"][1]["name"], "Docs")

    def test_generate_homepage_outline(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main([
                "generate",
                "page-outline",
                "homepage",
                "--project",
                "Geo Skill",
                "--audience",
                "AI product teams",
                "--summary",
                "Operational GEO toolkit",
            ])
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn("Hero", output)
        self.assertIn("Audience", output)
        self.assertIn("FAQ", output)

    def test_generate_feature_page_template(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main([
                "generate",
                "page-template",
                "feature",
                "--project",
                "Geo Skill",
                "--feature",
                "Live URL Audit",
                "--audience",
                "AI product teams",
                "--summary",
                "Audit public pages for GEO readiness",
            ])
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn("# Live URL Audit", output)
        self.assertIn("Who it is for", output)
        self.assertIn("How it works", output)

    def test_audit_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
            (root / "sitemap.xml").write_text("<urlset></urlset>", encoding="utf-8")
            (root / "index.html").write_text(
                "<html lang='en'><head><title>Example</title><meta name='description' content='x'><meta property='og:title' content='x'><script type='application/ld+json'>{}</script></head><body><h1>FAQ</h1></body></html>",
                encoding="utf-8",
            )
            (root / "pricing").mkdir()
            (root / "pricing" / "index.html").write_text("<html><head><title>Pricing</title></head><body>Plans</body></html>", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "index.html").write_text("<html><head><title>Docs</title></head><body>Getting started</body></html>", encoding="utf-8")
            (root / "about").mkdir()
            (root / "about" / "index.html").write_text("<html><head><title>About</title></head><body>Team</body></html>", encoding="utf-8")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main(["audit", str(root), "--format", "json"])
            self.assertEqual(code, 0)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["summary"]["fail"], 0)
            self.assertGreaterEqual(payload["score"], 70)
            self.assertTrue(any(item["message"].startswith("robots.txt") for item in payload["findings"]))
            self.assertTrue(payload["coverage"]["pricing"]["present"])
            self.assertTrue(payload["coverage"]["docs"]["present"])
            self.assertTrue(payload["coverage"]["trust"]["present"])
            self.assertFalse(payload["coverage"]["changelog"]["present"])

    def test_audit_text_output_includes_coverage_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
            (root / "sitemap.xml").write_text("<urlset></urlset>", encoding="utf-8")
            (root / "index.html").write_text("<html><head><title>Example</title><meta name='description' content='x'></head><body></body></html>", encoding="utf-8")
            (root / "pricing").mkdir()
            (root / "pricing" / "index.html").write_text("<html><head><title>Pricing</title></head><body>Plans</body></html>", encoding="utf-8")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main(["audit", str(root)])
            self.assertEqual(code, 0)
            output = stdout.getvalue()
            self.assertIn("Coverage:", output)
            self.assertIn("pricing: yes", output)
            self.assertIn("faq: no", output)

    def test_install_codex_skill_to_tempdir(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main([
                    "install",
                    "--agent",
                    "codex",
                    "--skill",
                    "geo-oss-repo-geo",
                    "--destination",
                    tmp,
                ])
            self.assertEqual(code, 0)
            target = Path(tmp) / "geo-oss-repo-geo" / "SKILL.md"
            self.assertTrue(target.exists())
            self.assertIn(str(target), stdout.getvalue())

    def test_skill_catalog_size(self):
        self.assertGreaterEqual(len(list_skills()), 20)


if __name__ == "__main__":
    unittest.main()
