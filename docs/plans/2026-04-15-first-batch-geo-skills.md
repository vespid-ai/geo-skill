# First Batch GEO Skills Expansion Plan

> For Hermes: implement directly in-repo and keep Hermes / Codex / Claude skill variants aligned.

Goal: turn geo-skill from a 4-skill proof-of-concept into a genuinely useful first batch of operational GEO skills for OpenAI, 豆包, docs-first sites, SaaS product sites, and OSS repos.

Architecture: keep one canonical Python skill catalog in `src/geo_skill/skills.py`, then generate repo-local Hermes / Codex / Claude skill files from that source of truth. Update README to expose the broader skill coverage and search-friendly terminology. Keep the CLI surface stable.

Tech stack: Python stdlib only, setuptools packaging, GitHub Actions unittest workflow.

---

## Task 1: Expand canonical skill catalog
- Modify: `src/geo_skill/skills.py`
- Goal: add the first high-value operational GEO skills as new `SkillSpec` entries
- Planned additions:
  - `geo-bing-webmaster-foundation`
  - `geo-homepage-positioning`
  - `geo-feature-pages`
  - `geo-pricing-pages`
  - `geo-faq-coverage`
  - `geo-docs-help-center`
  - `geo-changelog-freshness`
  - `geo-comparison-pages`
  - `geo-trust-and-entity-pages`
  - `geo-structured-data-software-sites`
  - `geo-oss-repo-geo`
  - `geo-launch-distribution`

## Task 2: Regenerate multi-agent skill files
- Modify/generated:
  - `skills/hermes/*`
  - `.agents/skills/*`
  - `.claude/skills/*`
- Goal: ensure all new skills are generated in Hermes / Codex / Claude-compatible formats from the canonical source.

## Task 3: Update README for broader GEO coverage
- Modify: `README.md`
- Goal: explain that the repo now covers product pages, docs, FAQ, pricing, trust, changelog, structured data, distribution, and OSS repo GEO.

## Task 4: Strengthen tests and verification
- Modify: `tests/test_cli.py`
- Run:
  - `python -m unittest discover -s tests -v`
  - `geo-skill skills list --agent codex`
  - `geo-skill skills show geo-faq-coverage --agent hermes`
  - `geo-skill install --agent codex --skill geo-oss-repo-geo --destination /tmp/...`
- Goal: confirm CLI still works after catalog expansion.

## Task 5: Commit and push
- Run git status, commit, push
- Goal: publish the first real skill batch to `vespid-ai/geo-skill`
