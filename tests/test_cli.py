import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

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
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main(["audit", str(root), "--format", "json"])
            self.assertEqual(code, 0)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["summary"]["fail"], 0)
            self.assertGreaterEqual(payload["score"], 70)
            self.assertTrue(any(item["message"].startswith("robots.txt") for item in payload["findings"]))

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
