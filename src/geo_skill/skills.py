from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class SkillSpec:
    name: str
    title: str
    one_line: str
    summary: str
    body: tuple[str, ...]


SKILL_SPECS: Dict[str, SkillSpec] = {
    "openai-chatgpt-search": SkillSpec(
        name="openai-chatgpt-search",
        title="OpenAI / ChatGPT Search GEO",
        one_line="Use when the task is about improving discoverability in ChatGPT Search, separating search visibility from training permission, or fixing OAI-SearchBot / GPTBot / Bing-facing GEO issues.",
        summary="Improve ChatGPT Search visibility with OAI-SearchBot, Bing-facing indexing, sitemap hygiene, and machine-readable product pages.",
        body=(
            "Keep search and training separate: OAI-SearchBot is the search surface, GPTBot is the training surface, and ChatGPT-User is user-triggered access rather than automatic discovery.",
            "Default operating checklist:",
            "1. Confirm robots.txt explicitly allows OAI-SearchBot.",
            "2. Decide whether GPTBot should be allowed or blocked for training.",
            "3. Ensure sitemap.xml exists, is reachable, and contains canonical URLs only.",
            "4. Make sure key product/docs/faq/pricing pages return 200 without login walls or bot challenges.",
            "5. Improve Bing-side discoverability because ChatGPT Search uses third-party search providers and Bing is explicitly referenced in OpenAI help documentation.",
            "6. Add structured data where useful and make product facts explicit in HTML.",
            "7. Verify changelog / freshness pages exist for frequently changing products.",
            "Use the CLI where possible:",
            "- `geo-skill audit <site-root>` to check technical readiness.",
            "- `geo-skill generate robots --domain https://example.com` for a starter robots.txt policy.",
            "Do not claim that allowing GPTBot is sufficient for ChatGPT Search visibility.",
        ),
    ),
    "doubao-bytespider": SkillSpec(
        name="doubao-bytespider",
        title="豆包 / Bytespider GEO",
        one_line="Use when the task is about helping a site be easier to discover through ByteDance search surfaces, Bytespider crawling, or practical 豆包 GEO work.",
        summary="Improve ByteDance-side GEO with Bytespider access, sitemap submission, rendered HTML, and Chinese-language product fact pages.",
        body=(
            "Treat 豆包 GEO as a real search/crawl problem, not as a mysterious hidden bot interface.",
            "Default operating checklist:",
            "1. Ensure robots.txt allows Bytespider.",
            "2. Ensure WAF/CDN/bot protection does not block Bytespider by UA or IP policy.",
            "3. Publish sitemap.xml with reachable canonical URLs only.",
            "4. Prefer rendered HTML instead of empty client-side shells.",
            "5. Build Chinese-language FAQ and scenario pages that match natural product discovery queries.",
            "6. Include official identity pages: company/about/contact/privacy/terms.",
            "7. When available, use 头条搜索站长平台 to verify the site and submit sitemap.",
            "Use the CLI where possible:",
            "- `geo-skill audit <site-root>` for local readiness checks.",
            "- `geo-skill generate robots --domain https://example.com` for a starter policy that includes Bytespider.",
            "Do not invent a fake 'DoubaoBot' dependency when public crawler guidance points to Bytespider / 头条搜索 surfaces.",
        ),
    ),
    "geo-site-readiness": SkillSpec(
        name="geo-site-readiness",
        title="GEO Site Readiness",
        one_line="Use when the task is to assess whether a website is technically ready for GEO before content rewrites or distribution work.",
        summary="Audit the technical baseline for GEO: robots, sitemap, llms.txt, metadata, HTML access, FAQ coverage, and structured data.",
        body=(
            "Run the technical baseline before spending time on content strategy.",
            "Default operating checklist:",
            "1. Check robots.txt, sitemap.xml, and llms.txt presence.",
            "2. Confirm index.html or equivalent entry pages contain title and meta description.",
            "3. Confirm Open Graph basics exist for key pages.",
            "4. Sample HTML pages and look for JSON-LD structured data.",
            "5. Check whether FAQ-like content exists in page copy.",
            "6. Review whether there are distinct URLs for product, feature, docs, pricing, FAQ, changelog, and trust pages.",
            "Use the CLI first:",
            "- `geo-skill audit <site-root>`",
            "Treat a missing technical baseline as a blocker for GEO claims.",
        ),
    ),
    "geo-content-modeling": SkillSpec(
        name="geo-content-modeling",
        title="GEO Content Modeling",
        one_line="Use when the task is to rewrite or structure pages so AI systems can understand, quote, and compare the product correctly.",
        summary="Model product facts for GEO so AI systems can quote what the product is, who it is for, what it does, and how it is priced or deployed.",
        body=(
            "Optimize for quotable product facts, not vague slogans.",
            "Default operating checklist:",
            "1. Put a one-sentence product definition near the top of each important page.",
            "2. Answer who the product is for and what problem it solves.",
            "3. Make capabilities, pricing, deployment, and availability explicit.",
            "4. Use natural-language FAQ sections aligned with likely search prompts.",
            "5. Publish changelog or dated updates for freshness signals.",
            "6. Avoid hiding critical facts inside images, videos, or interactive widgets only.",
            "Use the CLI where possible:",
            "- `geo-skill generate llms --project NAME --summary \"...\" --url https://example.com` for a starting llms.txt-style summary.",
            "Aim for pages that can be cited cleanly by search agents and coding agents alike.",
        ),
    ),
}

AGENTS = ("hermes", "codex", "claude")


def list_skills() -> List[str]:
    return sorted(SKILL_SPECS)


def list_agents() -> List[str]:
    return list(AGENTS)


def _render_body(items: Iterable[str], checklist_heading: str = "## Procedure", cli_heading: str = "## CLI hooks") -> str:
    rendered: List[str] = []
    for item in items:
        if item == "Default operating checklist:":
            rendered.append(checklist_heading)
        elif item in {"Use the CLI where possible:", "Use the CLI first:"}:
            rendered.append(cli_heading)
        elif item[:1].isdigit() or item.startswith("- "):
            rendered.append(item)
        else:
            rendered.append(f"- {item}")
    return "\n".join(rendered)


def render_skill(name: str, agent: str) -> str:
    if agent not in AGENTS:
        raise KeyError(f"unknown agent '{agent}'. available: {', '.join(AGENTS)}")
    if name not in SKILL_SPECS:
        raise KeyError(f"unknown skill '{name}'. available: {', '.join(list_skills())}")

    spec = SKILL_SPECS[name]
    body = _render_body(spec.body)

    if agent == "hermes":
        return f"""---
name: {name}
description: {spec.one_line}
version: 0.1.0
author: vespid-ai
license: MIT
metadata:
  hermes:
    tags: [geo, generative-engine-optimization, search, cli, agent]
---

# {spec.title}

{spec.summary}

## Trigger

{spec.one_line}

{body}
"""
    if agent == "codex":
        return f"""---
name: {name}
description: {spec.one_line}
---

# {spec.title}

{spec.summary}

## When to use

{spec.one_line}

{body}
"""
    return f"""# {name}

{spec.one_line}

## Goal

{spec.summary}

{body}
"""


def skill_catalog(agent: str | None = None) -> Dict[str, str]:
    _ = agent
    return {name: SKILL_SPECS[name].summary for name in list_skills()}


def default_install_dir(agent: str) -> Path:
    home = Path.home()
    if agent == "hermes":
        return home / ".hermes" / "skills" / "geo"
    if agent == "codex":
        return home / ".agents" / "skills"
    if agent == "claude":
        return home / ".claude" / "skills"
    raise KeyError(f"unknown agent '{agent}'")


def install_skill(name: str, agent: str, destination: str | Path | None = None) -> Path:
    content = render_skill(name, agent)
    base = Path(destination).expanduser() if destination else default_install_dir(agent)
    if agent in {"hermes", "codex"}:
        target_dir = base / name
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / "SKILL.md"
    else:
        base.mkdir(parents=True, exist_ok=True)
        target = base / f"{name}.md"
    target.write_text(content, encoding="utf-8")
    return target


def install_all(agent: str, destination: str | Path | None = None) -> List[Path]:
    return [install_skill(name, agent, destination) for name in list_skills()]


def export_repo_skill_files(repo_root: str | Path) -> List[Path]:
    root = Path(repo_root)
    created: List[Path] = []
    for name in list_skills():
        hermes_target = root / "skills" / "hermes" / name / "SKILL.md"
        hermes_target.parent.mkdir(parents=True, exist_ok=True)
        hermes_target.write_text(render_skill(name, "hermes"), encoding="utf-8")
        created.append(hermes_target)

        codex_target = root / ".agents" / "skills" / name / "SKILL.md"
        codex_target.parent.mkdir(parents=True, exist_ok=True)
        codex_target.write_text(render_skill(name, "codex"), encoding="utf-8")
        created.append(codex_target)

        claude_target = root / ".claude" / "skills" / f"{name}.md"
        claude_target.parent.mkdir(parents=True, exist_ok=True)
        claude_target.write_text(render_skill(name, "claude"), encoding="utf-8")
        created.append(claude_target)
    return created


def clean_generated_skill_dirs(repo_root: str | Path) -> None:
    root = Path(repo_root)
    for rel in ["skills/hermes", ".agents/skills", ".claude/skills"]:
        target = root / rel
        if target.exists():
            shutil.rmtree(target)
