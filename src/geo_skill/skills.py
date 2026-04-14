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
    'doubao-bytespider': SkillSpec(
        name='doubao-bytespider',
        title='豆包 / Bytespider GEO',
        one_line='Use when the task is about helping a site be easier to discover through ByteDance search surfaces, Bytespider crawling, or practical 豆包 GEO work.',
        summary='Improve ByteDance-side GEO with Bytespider access, sitemap submission, rendered HTML, and Chinese-language product fact pages.',
        body=(
            'Treat 豆包 GEO as a real search/crawl problem, not as a mysterious hidden bot interface.',
            'Default operating checklist:',
            '1. Ensure robots.txt allows Bytespider.',
            '2. Ensure WAF/CDN/bot protection does not block Bytespider by UA or IP policy.',
            '3. Publish sitemap.xml with reachable canonical URLs only.',
            '4. Prefer rendered HTML instead of empty client-side shells.',
            '5. Build Chinese-language FAQ and scenario pages that match natural product discovery queries.',
            '6. Include official identity pages: company/about/contact/privacy/terms.',
            '7. When available, use 头条搜索站长平台 to verify the site and submit sitemap.',
            'Use the CLI where possible:',
            '- `geo-skill audit <site-root>` for local readiness checks.',
            '- `geo-skill generate robots --domain https://example.com` for a starter policy that includes Bytespider.',
            'Do not invent a fake DoubaoBot dependency when public crawler guidance points to Bytespider / 头条搜索 surfaces.',
        ),
    ),
    'geo-api-docs-geo': SkillSpec(
        name='geo-api-docs-geo',
        title='GEO for API Docs',
        one_line='Use when the product exposes APIs or SDKs and the API documentation needs to become a first-class discovery and citation surface.',
        summary='Improve API-doc GEO with endpoint-focused pages, authentication/setup clarity, examples, limits, and troubleshooting sections that match developer search intent.',
        body=(
            'Developer-facing products are often discovered through API and integration questions rather than marketing pages.',
            'Default operating checklist:',
            '1. Give important endpoints, SDK workflows, and auth setup topics stable URLs.',
            '2. Show request, response, authentication, and error examples explicitly.',
            '3. Publish rate limits, pricing model, environments, and prerequisites in text.',
            '4. Add troubleshooting pages for common integration failures.',
            '5. Link API docs back to pricing, changelog, and product overview pages.',
            '6. Prefer task-oriented headings such as authenticate, stream, upload, webhook, or paginate over vague titles.',
            'Do not force developers to reverse-engineer basic usage from a single giant reference page.',
        ),
    ),
    'geo-bing-webmaster-foundation': SkillSpec(
        name='geo-bing-webmaster-foundation',
        title='Bing Webmaster GEO Foundation',
        one_line='Use when the task is to improve Bing-facing discovery, sitemap submission, or the search-engine foundation that supports OpenAI search visibility.',
        summary='Strengthen Bing-side discovery with site verification, sitemap submission, URL submission, crawl diagnostics, and IndexNow-aware operational GEO.',
        body=(
            'Treat Bing as a practical submission and diagnostics layer for OpenAI-adjacent GEO work, not as the entire ranking story.',
            'Default operating checklist:',
            '1. Verify the site in Bing Webmaster Tools.',
            '2. Submit sitemap.xml and keep it current.',
            '3. Use URL submission or IndexNow for key new pages when appropriate.',
            '4. Review crawl, indexing, and site-scan diagnostics for blocked or low-quality pages.',
            '5. Make sure canonical URLs, titles, descriptions, and structured data are consistent before submitting.',
            '6. Focus submission effort on product, feature, pricing, docs, FAQ, and changelog pages first.',
            'Use the CLI where possible:',
            '- `geo-skill audit <site-root>` before manual search-engine submission work.',
            'Do not treat Bing submission as a substitute for fixing weak page quality or crawlability.',
        ),
    ),
    'geo-case-studies-social-proof': SkillSpec(
        name='geo-case-studies-social-proof',
        title='GEO Case Studies and Social Proof',
        one_line='Use when the product needs stronger proof, outcomes, and adoption signals so AI systems can cite real usage instead of only self-description.',
        summary='Use case studies, customer stories, benchmarks, and outcome pages to give GEO stronger proof signals around who uses the product and what results it creates.',
        body=(
            'Case studies make products easier to trust because they connect capabilities to real outcomes and user types.',
            'Default operating checklist:',
            '1. Create dedicated pages for customer stories, internal benchmarks, or reference workflows.',
            '2. State who the user was, what problem they had, and what changed after adoption.',
            '3. Use numbers, timelines, or operational deltas only when they are real and attributable.',
            '4. Link case studies to the relevant feature, pricing, or docs pages.',
            '5. Group case studies by vertical, persona, or workflow if that maps to search demand.',
            '6. Keep proof pages factual enough that a search agent can quote them cleanly.',
            'Do not rely on empty testimonial carousels if you want strong evidence surfaces.',
        ),
    ),
    'geo-changelog-freshness': SkillSpec(
        name='geo-changelog-freshness',
        title='GEO Changelog and Freshness',
        one_line='Use when search systems need better freshness signals or when the product changes quickly and the site does not expose updates clearly.',
        summary='Use changelog, release notes, and dated updates to provide freshness signals that help AI systems answer with current product status.',
        body=(
            'Freshness matters most when product capability, pricing, models, or integrations change often.',
            'Default operating checklist:',
            '1. Publish a dedicated changelog or release notes section.',
            '2. Put dates on updates and keep entries specific.',
            '3. Link release notes back to the affected feature, pricing, or docs pages.',
            '4. Archive deprecated statements instead of leaving stale claims on top pages.',
            '5. Use update summaries that can be quoted cleanly by search agents.',
            'Do not rely on silent homepage edits alone when users or AI systems need to know what changed and when.',
        ),
    ),
    'geo-comparison-pages': SkillSpec(
        name='geo-comparison-pages',
        title='GEO Comparison Pages',
        one_line='Use when users compare your product to alternatives and you want AI systems to retrieve a grounded, balanced comparison page rather than random third-party summaries.',
        summary='Publish structured comparison pages that define differences, tradeoffs, target users, and capability boundaries without fake objectivity or keyword spam.',
        body=(
            'Comparison pages are answer magnets for bottom-of-funnel and evaluation queries.',
            'Default operating checklist:',
            '1. Create one comparison page per major alternative or category comparison.',
            '2. Use tables for capabilities, pricing model, deployment model, and best-fit user segments.',
            '3. Be explicit about tradeoffs and where the competitor is better.',
            '4. Link to your own feature, pricing, FAQ, and docs pages for evidence.',
            '5. Keep the tone factual enough that an AI system can quote it without sounding like ad copy.',
            'Do not publish empty versus pages that only repeat your own slogan and the competitor name.',
        ),
    ),
    'geo-content-modeling': SkillSpec(
        name='geo-content-modeling',
        title='GEO Content Modeling',
        one_line='Use when the task is to rewrite or structure pages so AI systems can understand, quote, and compare the product correctly.',
        summary='Model product facts for GEO so AI systems can quote what the product is, who it is for, what it does, and how it is priced or deployed.',
        body=(
            'Optimize for quotable product facts, not vague slogans.',
            'Default operating checklist:',
            '1. Put a one-sentence product definition near the top of each important page.',
            '2. Answer who the product is for and what problem it solves.',
            '3. Make capabilities, pricing, deployment, and availability explicit.',
            '4. Use natural-language FAQ sections aligned with likely search prompts.',
            '5. Publish changelog or dated updates for freshness signals.',
            '6. Avoid hiding critical facts inside images, videos, or interactive widgets only.',
            'Use the CLI where possible:',
            '- `geo-skill generate llms --project NAME --summary "..." --url https://example.com` for a starting llms.txt-style summary.',
            'Aim for pages that can be cited cleanly by search agents and coding agents alike.',
        ),
    ),
    'geo-docs-help-center': SkillSpec(
        name='geo-docs-help-center',
        title='GEO Docs and Help Center',
        one_line='Use when the product is docs-first or technical and you need the documentation set to become a primary GEO surface.',
        summary='Turn docs and help-center content into a strong GEO surface with stable URLs, topic-focused pages, explicit examples, and internal linking.',
        body=(
            'For technical products, docs often outperform the homepage as the page type most likely to be cited.',
            'Default operating checklist:',
            '1. Give each concept, workflow, and API topic its own stable page.',
            '2. Use titles and headings that mirror user tasks and troubleshooting questions.',
            '3. Add examples, limits, prerequisites, and expected outputs.',
            '4. Link docs pages back to product, pricing, and FAQ pages when relevant.',
            '5. Avoid hiding core instructions behind tabs or interactive widgets only.',
            '6. Publish last-updated dates when documentation freshness matters.',
            'Do not force the entire docs set into one scrolling page if you want strong answer retrieval.',
        ),
    ),
    'geo-faq-coverage': SkillSpec(
        name='geo-faq-coverage',
        title='GEO FAQ Coverage',
        one_line='Use when you need to turn real user questions into machine-readable FAQ coverage that maps directly to AI search prompts.',
        summary='Build FAQ pages around real user-language questions so AI systems can answer comparisons, setup, pricing, deployment, privacy, and capability queries.',
        body=(
            'FAQ content is one of the cleanest ways to match natural-language prompts.',
            'Default operating checklist:',
            '1. Collect the top repeated sales, support, and onboarding questions.',
            '2. Write each question the way a user would ask it, not in internal taxonomy language.',
            '3. Answer directly in the first sentence, then add detail.',
            '4. Group by product basics, setup, pricing, integrations, privacy, security, and limits.',
            '5. Link each answer to deeper docs or product pages.',
            '6. Consider FAQPage structured data when the content is real and stable.',
            'Use the CLI where possible:',
            '- `geo-skill generate llms --project NAME --summary "FAQ coverage for key user questions" --url https://example.com/faq` for a starting summary block.',
            'Do not stuff dozens of barely useful keyword variants into one FAQ; prioritize genuine answer quality.',
        ),
    ),
    'geo-feature-pages': SkillSpec(
        name='geo-feature-pages',
        title='GEO Feature Pages',
        one_line='Use when a product has multiple capabilities but they are collapsed into one page, making it hard for search systems to quote and compare specific features.',
        summary='Create dedicated feature pages that isolate capabilities, use cases, and evidence so AI systems can cite the right page for the right question.',
        body=(
            'Feature pages improve precision: one capability, one page, one clear answer surface.',
            'Default operating checklist:',
            '1. Split major capabilities into distinct URLs.',
            '2. Give each page a clear title, summary, inputs, outputs, and user value.',
            '3. Add links to pricing, docs, API references, and related feature pages.',
            '4. Include constraints, deployment notes, or supported integrations when relevant.',
            '5. Use screenshots as support, not as the only carrier of product facts.',
            'Use the CLI where possible:',
            '- `geo-skill generate llms --project NAME --summary "Feature page summary" --url https://example.com/feature` as a drafting aid.',
            'Avoid giant all-in-one pages where every feature competes for the same keywords and answer intents.',
        ),
    ),
    'geo-homepage-positioning': SkillSpec(
        name='geo-homepage-positioning',
        title='GEO Homepage Positioning',
        one_line='Use when the homepage is vague, slogan-heavy, or failing to define what the product is for AI search systems and first-time human visitors.',
        summary='Make the homepage define the product clearly with category, audience, problem, capabilities, and proof instead of vague brand copy.',
        body=(
            'The homepage must answer what the product is in the first screenful of text.',
            'Default operating checklist:',
            '1. Add a one-sentence category definition near the hero.',
            '2. State who the product is for and what problem it solves.',
            '3. List 3 to 6 core capabilities in plain language.',
            '4. Link to deeper product, feature, docs, pricing, and FAQ pages.',
            '5. Avoid jargon that only the internal team understands.',
            '6. Add proof signals such as OSS repo, customers, integrations, benchmarks, or launch status where real.',
            'Use the CLI where possible:',
            '- `geo-skill audit <site-root>` to confirm the homepage also meets technical readiness basics.',
            'Do not let the homepage be only a mood board; it must expose quotable product facts.',
        ),
    ),
    'geo-launch-distribution': SkillSpec(
        name='geo-launch-distribution',
        title='GEO Launch and Distribution',
        one_line='Use when the site already has core pages but still needs external signals, distribution, and launch artifacts so AI systems can see more than the official site alone.',
        summary='Create external proof and distribution surfaces so GEO is supported by repo pages, social posts, directories, docs links, and third-party references.',
        body=(
            'AI systems trust a product more when official claims are reinforced by external surfaces.',
            'Default operating checklist:',
            '1. Publish launch posts, docs links, and repository updates around the same positioning language.',
            '2. Submit or publish to relevant directories, communities, or product lists where appropriate.',
            '3. Make sure social, repo, docs, and homepage all point back to canonical URLs.',
            '4. Use consistent short descriptions across profiles and launch surfaces.',
            '5. Encourage third-party tutorials, examples, and reviews when they are real and attributable.',
            'Do not rely on the website alone if you want strong entity recognition and citation breadth.',
        ),
    ),
    'geo-multilingual-localization': SkillSpec(
        name='geo-multilingual-localization',
        title='GEO Multilingual and Localization Strategy',
        one_line='Use when a product targets more than one language or region and needs GEO-safe localized pages instead of shallow machine-translated duplicates.',
        summary='Build multilingual GEO with stable localized URLs, explicit language targeting, consistent product facts, and region-aware FAQ or pricing surfaces.',
        body=(
            'Multilingual GEO is about preserving meaning and retrieval quality across languages, not just translating strings.',
            'Default operating checklist:',
            '1. Give each language or region a stable URL structure.',
            '2. Keep product naming and category definitions consistent across languages.',
            '3. Localize FAQ, pricing, and docs with market-appropriate wording instead of literal translation only.',
            '4. Use hreflang when the site architecture supports it cleanly.',
            '5. Avoid publishing thin duplicate pages where the only change is a language switcher with no adapted content.',
            '6. Make sure critical trust, privacy, and contact pages are understandable in the main target languages.',
            'Do not let localized pages drift so far that AI systems see them as different products or conflicting facts.',
        ),
    ),
    'geo-oss-repo-geo': SkillSpec(
        name='geo-oss-repo-geo',
        title='GEO for Open-Source Repositories',
        one_line='Use when the product is open source and GitHub, docs, releases, examples, and README quality are core discovery surfaces.',
        summary='Optimize OSS repositories for GEO with a strong README, clear examples, releases, docs links, and public product facts that search systems can cite.',
        body=(
            'For OSS projects, the repository itself is often the homepage, docs hub, and proof surface at once.',
            'Default operating checklist:',
            '1. Make README define what the project is, who it is for, and why it matters.',
            '2. Add installation, quickstart, examples, and architecture or capability summaries.',
            '3. Link to docs, issues, releases, changelog, and license clearly.',
            '4. Use tags, topics, and release notes to improve retrieval across GitHub and search systems.',
            '5. Keep project naming, package naming, and repo naming consistent.',
            '6. Include trust signals such as maintainer identity, contribution model, and roadmap where real.',
            'Do not assume code alone is enough; GEO for OSS requires strong explanatory text and structure.',
        ),
    ),
    'geo-pricing-pages': SkillSpec(
        name='geo-pricing-pages',
        title='GEO Pricing Pages',
        one_line='Use when pricing, free tier, or packaging questions are common and the site does not expose them cleanly enough for AI systems to answer.',
        summary='Make pricing pages machine-readable and direct so search agents can answer what it costs, what plans exist, and how usage is packaged.',
        body=(
            'Pricing is one of the highest-value answer surfaces because users ask about cost before purchase.',
            'Default operating checklist:',
            '1. Publish a dedicated pricing page on a stable canonical URL.',
            '2. State whether there is a free tier, trial, self-hosted option, or enterprise plan.',
            '3. Make plan differences explicit in text, not just in visual cards.',
            '4. Clarify pricing units: seat, request, token, API call, project, or monthly subscription.',
            '5. Link to FAQ entries for edge cases such as limits, refunds, and contract terms.',
            '6. Keep old pricing statements updated or archived to avoid conflicting citations.',
            'Do not hide pricing behind forms if you want strong answerability for pricing-related queries.',
        ),
    ),
    'geo-site-migration-url-stability': SkillSpec(
        name='geo-site-migration-url-stability',
        title='GEO Site Migration and URL Stability',
        one_line='Use when moving domains, restructuring docs, redesigning the site, or changing URL patterns without losing accumulated GEO signals.',
        summary='Protect GEO during site migrations with URL inventories, redirects, canonical continuity, sitemap updates, and post-migration validation.',
        body=(
            'A migration can erase accumulated discovery signals if redirects and canonical mappings are sloppy.',
            'Default operating checklist:',
            '1. Inventory the current high-value URLs before changing structure.',
            '2. Map old URLs to the most relevant new URLs with permanent redirects.',
            '3. Keep titles, product facts, and canonical intent stable during the transition.',
            '4. Regenerate sitemap.xml and update any submission workflows after the cutover.',
            '5. Recheck robots.txt, structured data, and trust pages on the new paths.',
            '6. Watch for broken docs, pricing, FAQ, and changelog links after launch.',
            'Use the CLI where possible:',
            '- `geo-skill audit <site-root>` before and after migration to catch missing technical basics.',
            'Do not launch a new IA or domain without a redirect map for the old answer surfaces.',
        ),
    ),
    'geo-site-readiness': SkillSpec(
        name='geo-site-readiness',
        title='GEO Site Readiness',
        one_line='Use when the task is to assess whether a website is technically ready for GEO before content rewrites or distribution work.',
        summary='Audit the technical baseline for GEO: robots, sitemap, llms.txt, metadata, HTML access, FAQ coverage, and structured data.',
        body=(
            'Run the technical baseline before spending time on content strategy.',
            'Default operating checklist:',
            '1. Check robots.txt, sitemap.xml, and llms.txt presence.',
            '2. Confirm indexable entry pages contain title and meta description.',
            '3. Confirm Open Graph basics exist for important pages.',
            '4. Sample HTML pages and look for JSON-LD structured data.',
            '5. Check whether FAQ-like content exists in page copy.',
            '6. Review whether there are distinct URLs for product, feature, docs, pricing, FAQ, changelog, and trust pages.',
            'Use the CLI first:',
            '- `geo-skill audit <site-root>`.',
            'Treat a missing technical baseline as a blocker for GEO claims.',
        ),
    ),
    'geo-structured-data-software-sites': SkillSpec(
        name='geo-structured-data-software-sites',
        title='GEO Structured Data for Software Sites',
        one_line='Use when the site needs stronger machine-readable semantics for software, product, organization, FAQ, breadcrumb, and article pages.',
        summary='Use structured data deliberately on software and product sites so search systems can parse entities, offers, FAQs, and content relationships more reliably.',
        body=(
            'Structured data helps with machine readability, but only when it reflects real page content.',
            'Default operating checklist:',
            '1. Start with Organization and WebSite on top-level identity pages.',
            '2. Use Product or SoftwareApplication on core product pages when the content supports it.',
            '3. Use FAQPage only for actual question-and-answer sections.',
            '4. Add BreadcrumbList where site hierarchy matters.',
            '5. Keep schema fields aligned with visible page content and canonical URLs.',
            '6. Avoid fake review or rating data.',
            'Use the CLI where possible:',
            '- `geo-skill audit <site-root>` to catch whether any JSON-LD is present before improving quality.',
            'Do not treat schema markup as a substitute for weak content or absent pages.',
        ),
    ),
    'geo-trust-and-entity-pages': SkillSpec(
        name='geo-trust-and-entity-pages',
        title='GEO Trust and Entity Pages',
        one_line='Use when the site needs stronger legitimacy, company identity, trust, and entity resolution signals for both AI systems and human evaluators.',
        summary='Expose trust pages and entity facts so AI systems can connect the product to a real team, company, policy surface, and contact identity.',
        body=(
            'Strong trust and entity pages make the product easier to verify and safer to cite.',
            'Default operating checklist:',
            '1. Publish About, Contact, Privacy, and Terms pages.',
            '2. Include legal or company identity details where appropriate.',
            '3. Link official socials, GitHub org, and docs consistently.',
            '4. Keep brand naming consistent across pages and metadata.',
            '5. Add team or maintainer context if the project is OSS-first.',
            '6. Make support or contact channels explicit.',
            'Do not expect AI systems to trust a product with no visible operator, policy, or contact surface.',
        ),
    ),
    'openai-chatgpt-search': SkillSpec(
        name='openai-chatgpt-search',
        title='OpenAI / ChatGPT Search GEO',
        one_line='Use when the task is about improving discoverability in ChatGPT Search, separating search visibility from training permission, or fixing OAI-SearchBot / GPTBot / Bing-facing GEO issues.',
        summary='Improve ChatGPT Search visibility with OAI-SearchBot, Bing-facing indexing, sitemap hygiene, and machine-readable product pages.',
        body=(
            'Keep search and training separate: OAI-SearchBot is the search surface, GPTBot is the training surface, and ChatGPT-User is user-triggered access rather than automatic discovery.',
            'Default operating checklist:',
            '1. Confirm robots.txt explicitly allows OAI-SearchBot.',
            '2. Decide whether GPTBot should be allowed or blocked for training.',
            '3. Ensure sitemap.xml exists, is reachable, and contains canonical URLs only.',
            '4. Make sure key product/docs/faq/pricing pages return 200 without login walls or bot challenges.',
            '5. Improve Bing-side discoverability because ChatGPT Search uses third-party search providers and Bing is explicitly referenced in OpenAI help documentation.',
            '6. Add structured data where useful and make product facts explicit in HTML.',
            '7. Verify changelog / freshness pages exist for frequently changing products.',
            'Use the CLI where possible:',
            '- `geo-skill audit <site-root>` to check technical readiness.',
            '- `geo-skill generate robots --domain https://example.com` for a starter robots.txt policy.',
            'Do not claim that allowing GPTBot is sufficient for ChatGPT Search visibility.',
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
        raise KeyError(f"unknown agent {agent!r}. available: {', ' .join(AGENTS)}")
    if name not in SKILL_SPECS:
        raise KeyError(f"unknown skill {name!r}. available: {', ' .join(list_skills())}")

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
    raise KeyError(f"unknown agent {agent!r}")


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
