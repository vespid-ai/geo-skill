# geo-skill

[![Status](https://img.shields.io/badge/status-released%20CLI-16a34a)](https://github.com/vespid-ai/geo-skill)
[![Docs](https://img.shields.io/badge/docs-vespid.ai-111827)](https://vespid.ai/projects/geo-skill/)
[![Website](https://img.shields.io/badge/website-vespid.ai-0f766e)](https://vespid.ai)
[![Release](https://img.shields.io/badge/release-v0.4.0-16a34a)](https://github.com/vespid-ai/geo-skill/releases/tag/v0.4.0)
[![License](https://img.shields.io/badge/license-MIT-16a34a)](./LICENSE)

Generative Engine Optimization (GEO) skill pack and Python CLI for AI search, ChatGPT Search, Bing, llms.txt, structured data, and machine-readable content discovery.

`geo-skill` is an open-source repository for teams that want reusable GEO skills plus a practical CLI for auditing and generating the pages, files, and metadata that improve discovery across OpenAI / ChatGPT Search, Bing, 豆包 / Bytespider, docs sites, multilingual sites, and OSS repos.

[Built-in GEO skills](#built-in-geo-skills) · [CLI commands](#cli-commands) · [Quick start](#quick-start)

## Multilingual snapshot

### 简体中文
`geo-skill` 提供面向 AI Search / ChatGPT Search / 豆包 / Bytespider 的 GEO 技能包与 Python CLI，用于审计站点可发现性、生成 llms.txt / schema / 页面骨架，并提升机器可读内容质量。

### 日本語
`geo-skill` は AI Search / ChatGPT Search / 豆包 / Bytespider 向けの GEO skill pack と Python CLI を提供し、llms.txt、schema、ページ構造、ドキュメント導線を実務レベルで改善できるようにします。

### Español
`geo-skill` ofrece un skill pack GEO y un CLI en Python para AI search, ChatGPT Search y otros motores de descubrimiento, con auditoría de sitios, generación de llms.txt, schema y mejoras de contenido legible por máquinas.

## Search surface

- Generative Engine Optimization
- GEO
- AI search optimization
- ChatGPT Search
- llms.txt
- structured data
- machine-readable content
- agent skill pack

## What this repo provides

1. agent-loadable skills for Hermes Agent, Claude Code, and Codex
2. a zero-dependency Python CLI for auditing and generating core GEO assets
3. a searchable README and repository structure that describe GEO, skill, CLI, and agent workflows clearly
4. a first real batch of operational GEO skills for product sites, docs, pricing, trust, changelog, comparisons, and OSS repos
5. a second batch of live-audit and generator capabilities for multilingual sites, API docs, case studies, and migration-safe GEO work
6. a third batch with score-based audit output, JSON reporting, richer live checks, starter page templates, and the first tagged release workflow
7. a fourth batch with sitemap-aware page archetype coverage, trust/discovery surface detection, and broader schema generation for Product, Organization, WebSite, and BreadcrumbList

## Agent compatibility

### Hermes Agent

Hermes skills are stored in `skills/hermes/<skill-name>/SKILL.md` and can be installed into `~/.hermes/skills/geo/`.

### Claude Code

Claude-ready skills are stored in `.claude/skills/*.md` and can be installed into `~/.claude/skills/`.

### Codex

Codex-ready skills are stored in `.agents/skills/<skill-name>/SKILL.md` and follow OpenAI Codex skill conventions.

## Built-in GEO skills

### Search-surface skills

- `openai-chatgpt-search`
- `doubao-bytespider`
- `geo-bing-webmaster-foundation`
- `geo-site-readiness`
- `geo-structured-data-software-sites`

### Content and page-modeling skills

- `geo-content-modeling`
- `geo-homepage-positioning`
- `geo-feature-pages`
- `geo-pricing-pages`
- `geo-faq-coverage`
- `geo-docs-help-center`
- `geo-changelog-freshness`
- `geo-comparison-pages`
- `geo-trust-and-entity-pages`

### Distribution and repo skills

- `geo-oss-repo-geo`
- `geo-launch-distribution`

### Second-batch expansion skills

- `geo-multilingual-localization`
- `geo-api-docs-geo`
- `geo-case-studies-social-proof`
- `geo-site-migration-url-stability`

## CLI commands

```bash
geo-skill skills list
geo-skill skills show openai-chatgpt-search --agent hermes
geo-skill install --agent codex --all
geo-skill install --agent claude --skill geo-site-readiness
geo-skill audit ./site
geo-skill audit --url https://example.com
geo-skill audit ./site --format json
geo-skill generate robots --domain https://example.com
geo-skill generate llms --project GeoSkill --summary "Open-source GEO skill pack" --url https://example.com
geo-skill generate schema software-application --name "Geo Skill" --url https://example.com --summary "Operational GEO toolkit"
geo-skill generate schema product --name "Geo Skill Cloud" --url https://example.com/product --summary "Managed GEO workflow platform" --brand "vespid-ai" --price 99
geo-skill generate schema organization --name "vespid-ai" --url https://vespid.ai --description "Agent infrastructure and GEO tooling" --same-as https://github.com/vespid-ai
geo-skill generate schema website --name "Geo Skill" --url https://example.com --description "Operational GEO toolkit" --search-url-template "https://example.com/search?q={search_term_string}"
geo-skill generate schema breadcrumb --item "Home::https://example.com" --item "Docs::https://example.com/docs"
geo-skill generate page-outline homepage --project "Geo Skill" --audience "AI product teams" --summary "Operational GEO toolkit"
geo-skill generate page-template feature --project "Geo Skill" --feature "Live URL Audit" --audience "AI product teams" --summary "Audit public pages for GEO readiness"
```

## Why this exists

Most GEO advice is still too fuzzy to operationalize. Teams hear that they should “write for AI search” but end up missing the concrete layers that matter:

- crawler allow / deny rules
- sitemap and indexing hygiene
- product fact modeling
- FAQ and docs coverage
- pricing and packaging clarity
- trust and entity signals
- changelog freshness
- comparison pages
- structured data
- machine-readable page design
- OSS repo discoverability
- distribution signals outside the main site
- agent-operable skills that can repeat the work

`geo-skill` focuses on operational GEO instead of folklore.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
geo-skill skills list
```

## Install skills into local agents

Install every Codex skill into your user skill directory:

```bash
geo-skill install --agent codex --all
```

Install one Hermes skill:

```bash
geo-skill install --agent hermes --skill openai-chatgpt-search
```

Install one Claude skill into a custom directory:

```bash
geo-skill install --agent claude --skill geo-content-modeling --destination ./tmp-claude-skills
```

## What the first useful batch covers

This first real batch is designed to cover the actual GEO work most teams need first:

- making OpenAI / ChatGPT Search and 豆包 / Bytespider discovery easier
- improving Bing-facing indexing and submission hygiene
- fixing homepage positioning and feature-page structure
- making pricing, FAQ, docs, changelog, and trust pages easier to cite
- creating grounded comparison pages
- improving OSS repo discoverability on GitHub and the open web
- improving launch and distribution signals outside the official website
- generating starter structured data and page outlines
- auditing live URLs before and after publication or migration
- covering multilingual, API-doc, case-study, and migration GEO workflows

## Third-batch audit and generator upgrades

The third batch adds operational output modes and starter generation, not just advice:

- score-based audit output in text mode
- `--format json` for CI or scripted consumption
- richer live checks for canonical, `html lang`, and discovery files
- starter markdown page templates for feature, pricing, FAQ, comparison, and changelog pages
- first public release preparation

## Fourth-batch coverage and schema upgrades

The fourth batch moves from isolated page checks toward site-shape validation and broader machine-readable entities:

- sitemap-aware detection for homepage, feature, pricing, docs, FAQ, changelog, and trust surfaces
- coverage summaries in both text and JSON audit output
- trust/discovery checks backed by page archetype matching instead of only single-page metadata
- new schema generators for `Product`, `Organization`, `WebSite`, and `BreadcrumbList`

## Technical audit example

```text
$ geo-skill audit ./public
GEO audit for ./public

PASS  robots.txt exists
PASS  sitemap.xml exists
WARN  llms.txt missing
PASS  index.html has title tag
PASS  index.html has meta description
WARN  no JSON-LD structured data found in sampled HTML files

Summary: 4 pass, 2 warn, 0 fail
Coverage:
- homepage: yes (/)
- feature: no
- pricing: no
- docs: no
- faq: yes (/)
- changelog: no
- trust: no
```

## Repository layout

```text
.agents/skills/          Codex-ready skills
.claude/skills/          Claude-ready skills
skills/hermes/           Hermes-ready skills
src/geo_skill/           CLI implementation
tests/                   unit tests
docs/plans/              implementation plans
```

## Design principles

- no external runtime dependencies
- skills stay readable in GitHub
- CLI stays easy to call from agents
- OpenAI GEO and ByteDance GEO are modeled as distinct surfaces
- README uses industry-standard terms so humans and search systems can find it with combinations like GEO + skill + CLI + agent
- useful page archetypes are treated as first-class GEO work, not as generic SEO leftovers

## Roadmap

### P0

- benchmark fixtures from real product sites
- richer page-type heuristics for multilingual and multi-product sites
- optional markdown / SARIF export for CI comments and issue filing

### P1

- repo-scoped installer helpers for Codex and Claude skill locations
- benchmark diff mode for before/after GEO audits
- optional plugin packaging for Codex distribution

### P2

- more agent-specific skill variants and packaging helpers
- sitemap index crawling for very large sites
- opt-in remote concurrency for large live audits

## License

MIT
