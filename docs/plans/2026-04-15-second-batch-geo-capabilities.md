# Second Batch GEO Capabilities Plan

> For Hermes: implement directly in-repo and keep Hermes / Codex / Claude variants aligned.

Goal: ship the second batch in one pass by adding live URL audit, schema/page generators, multilingual/API-docs/case-studies/migration skills, and README updates that make these capabilities discoverable.

Architecture: keep one canonical skill catalog in `src/geo_skill/skills.py`, extend `src/geo_skill/audit.py` with reusable HTML/url auditing primitives, and extend `src/geo_skill/cli.py` with new `audit --url` and `generate schema/page-outline` workflows. Maintain zero runtime dependencies.

Tech stack: Python stdlib only, unittest, urllib/http.server for tests.

---

## Task 1: Add failing tests for second-batch capabilities
Files:
- Modify: `tests/test_audit.py`
- Modify: `tests/test_cli.py`

Coverage to add:
- live URL audit using a local HTTP server
- schema generation for `software-application`
- page-outline generation for homepage or faq
- larger skill catalog threshold to reflect new skills

## Task 2: Implement live URL audit
Files:
- Modify: `src/geo_skill/audit.py`
- Modify: `src/geo_skill/cli.py`

Behavior:
- support `geo-skill audit --url https://example.com`
- fetch page HTML and related discovery files like `/robots.txt`, `/sitemap.xml`, `/llms.txt`
- report metadata / canonical / JSON-LD / FAQ-like signals for live pages

## Task 3: Implement schema and page-outline generators
Files:
- Modify: `src/geo_skill/cli.py`

Behavior:
- `geo-skill generate schema software-application ...`
- `geo-skill generate schema faq ...`
- `geo-skill generate page-outline homepage|faq|pricing|docs|case-study ...`

## Task 4: Expand second-batch skills
Files:
- Modify: `src/geo_skill/skills.py`
- Regenerate: `skills/hermes/*`, `.agents/skills/*`, `.claude/skills/*`

New skills:
- `geo-multilingual-localization`
- `geo-api-docs-geo`
- `geo-case-studies-social-proof`
- `geo-site-migration-url-stability`

## Task 5: Update README and verify
Files:
- Modify: `README.md`

Verification:
- `python -m unittest discover -s tests -v`
- CLI spot checks for audit, schema, page-outline, and skills
- git commit + push
