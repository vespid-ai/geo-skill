import contextlib
import io
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
                "Operational GEO skills and CLI",
            ])
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn("Hero", output)
        self.assertIn("Audience", output)
        self.assertIn("FAQ", output)

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
