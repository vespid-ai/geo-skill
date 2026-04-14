# geo-skill

Generative Engine Optimization (GEO) skill pack, CLI, and agent-ready repository for OpenAI / ChatGPT Search, 豆包 / Bytespider, and machine-readable product discovery.

`geo-skill` is an open-source GitHub project for teams that want reusable GEO skills and a practical CLI that can be used by agents such as Hermes Agent, Claude Code, and Codex.

Search keywords this repository is deliberately optimized around:

- Generative Engine Optimization
- GEO
- GEO skill
- GEO CLI
- GEO agent
- ChatGPT Search GEO
- OpenAI GEO
- 豆包 GEO
- Bytespider GEO
- agent skill pack

## What this repo provides

1. agent-loadable skills for Hermes Agent, Claude Code, and Codex
2. a zero-dependency Python CLI for auditing and generating core GEO assets
3. a searchable README and repository structure that describe GEO, skill, CLI, and agent workflows clearly

## Agent compatibility

### Hermes Agent

Hermes skills are stored in `skills/hermes/<skill-name>/SKILL.md` and can be installed into `~/.hermes/skills/geo/`.

### Claude Code

Claude-ready skills are stored in `.claude/skills/*.md` and can be installed into `~/.claude/skills/`.

### Codex

Codex-ready skills are stored in `.agents/skills/<skill-name>/SKILL.md` and follow OpenAI Codex skill conventions.

## Built-in GEO skills

- `openai-chatgpt-search`
- `doubao-bytespider`
- `geo-site-readiness`
- `geo-content-modeling`

## CLI commands

```bash
geo-skill skills list
geo-skill skills show openai-chatgpt-search --agent hermes
geo-skill install --agent codex --all
geo-skill install --agent claude --skill geo-site-readiness
geo-skill audit ./site
geo-skill generate robots --domain https://example.com
geo-skill generate llms --project GeoSkill --summary "Open-source GEO skill pack" --url https://example.com
```

## Why this exists

Most GEO advice is still too fuzzy to operationalize. Teams hear that they should “write for AI search” but end up missing the concrete layers that matter:

- crawler allow / deny rules
- sitemap and indexing hygiene
- product fact modeling
- FAQ and docs coverage
- structured data
- machine-readable page design
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
```

## Repository layout

```text
.agents/skills/          Codex-ready skills
.claude/skills/          Claude-ready skills
skills/hermes/           Hermes-ready skills
src/geo_skill/           CLI implementation
tests/                   unit tests
```

## Design principles

- no external runtime dependencies
- skills stay readable in GitHub
- CLI stays easy to call from agents
- OpenAI GEO and ByteDance GEO are modeled as distinct surfaces
- README uses industry-standard terms so humans and search systems can find it with combinations like GEO + skill + CLI + agent

## Roadmap

### P0

- richer audit checks for canonical, OG/Twitter, schema quality, and page coverage
- more skills for pricing pages, changelog strategy, and docs IA
- JSON output mode for CI gates

### P1

- live URL audit mode
- installer helpers for repo-scoped Codex and Claude skill locations
- schema generators for `SoftwareApplication`, `Product`, and FAQ pages

### P2

- benchmark fixtures from real product sites
- more agent-specific skill variants and packaging helpers
- optional plugin packaging for Codex distribution

## License

MIT
