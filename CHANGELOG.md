# Changelog

## v0.3.0 - 2026-04-15

First public tagged release of `geo-skill`.

### Added
- first full batch of operational GEO skills for homepage, feature, pricing, FAQ, docs, changelog, trust, comparison, OSS repo, and distribution workflows
- second batch of multilingual, API-doc, case-study, and migration GEO skills
- live URL audit via `geo-skill audit --url ...`
- JSON-LD schema generation for `SoftwareApplication` and `FAQPage`
- page-outline generation for homepage, FAQ, pricing, docs, and case-study workflows
- page-template generation for feature, pricing, FAQ, comparison, and changelog content
- JSON audit output via `geo-skill audit --format json`
- score-based audit summaries for terminal output

### Improved
- richer live checks for `robots.txt`, `sitemap.xml`, `llms.txt`, canonical tags, language tags, Open Graph, JSON-LD, and FAQ-like content
- multi-agent skill coverage for Hermes Agent, Codex, and Claude Code
- repository README for GEO / skill / CLI / agent discoverability

### Validation
- unittest suite passes locally
- GitHub Actions CI passes on the release commit
