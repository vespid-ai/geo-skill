# geo-skill contributor guide

## Purpose

This repository publishes Generative Engine Optimization (GEO) skills and a CLI that other agents can call.

## Scope

- keep terminology aligned with industry-standard GEO / AI-search language
- prioritize OpenAI / ChatGPT Search, Bing-facing search hygiene, and 豆包 / Bytespider workflows
- prefer zero-dependency Python for CLI changes unless a dependency is clearly justified

## Repository conventions

- Hermes skills live in `skills/hermes/<skill-name>/SKILL.md`
- Codex skills live in `.agents/skills/<skill-name>/SKILL.md`
- Claude skills live in `.claude/skills/<skill-name>.md`
- if you change skill content, keep equivalent guidance aligned across supported agents
- if you change CLI behavior, update README examples and tests in the same change

## Verification

Run:

```bash
python -m unittest discover -s tests -v
```
