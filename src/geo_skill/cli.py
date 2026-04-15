from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .audit import COVERAGE_ORDER, audit_site, audit_url
from .benchmarks import list_benchmarks
from .skills import install_all, install_skill, list_agents, render_skill, skill_catalog


AGENT_CHOICES = tuple(list_agents())


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="geo-skill", description="GEO skill pack and CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    skills_parser = subparsers.add_parser("skills", help="browse built-in GEO skills")
    skills_sub = skills_parser.add_subparsers(dest="skills_command", required=True)
    list_parser = skills_sub.add_parser("list", help="list built-in skills")
    list_parser.add_argument("--agent", choices=AGENT_CHOICES, default="hermes", help="skill format to preview")
    show_parser = skills_sub.add_parser("show", help="show a built-in skill")
    show_parser.add_argument("name", help="skill name")
    show_parser.add_argument("--agent", choices=AGENT_CHOICES, default="hermes", help="skill format to preview")

    install_parser = subparsers.add_parser("install", help="install skills into a local agent directory")
    install_parser.add_argument("--agent", choices=AGENT_CHOICES, required=True, help="target agent")
    scope = install_parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--skill", help="single skill name")
    scope.add_argument("--all", action="store_true", help="install every built-in skill")
    install_parser.add_argument("--destination", help="override install destination")

    benchmarks_parser = subparsers.add_parser("benchmarks", help="browse bundled GEO benchmark fixtures")
    benchmarks_sub = benchmarks_parser.add_subparsers(dest="benchmarks_command", required=True)
    benchmarks_sub.add_parser("list", help="list bundled benchmark fixtures")

    audit_parser = subparsers.add_parser("audit", help="audit a static site directory or live URL")
    audit_parser.add_argument("path", nargs="?", help="path to site root")
    audit_parser.add_argument("--url", help="live URL to audit")
    audit_parser.add_argument("--format", choices=["text", "json", "markdown", "sarif"], default="text", help="output format")

    compare_parser = subparsers.add_parser("compare", help="compare before/after GEO audit JSON reports")
    compare_parser.add_argument("before", help="path to the baseline audit JSON file")
    compare_parser.add_argument("after", help="path to the updated audit JSON file")
    compare_parser.add_argument("--format", choices=["text", "json", "markdown"], default="text", help="output format")

    generate_parser = subparsers.add_parser("generate", help="generate GEO starter assets")
    generate_sub = generate_parser.add_subparsers(dest="generate_command", required=True)

    robots_parser = generate_sub.add_parser("robots", help="generate robots.txt")
    robots_parser.add_argument("--domain", required=True, help="site domain, like https://example.com")
    robots_parser.add_argument("--allow-gptbot", action="store_true", help="allow GPTBot for training access")

    llms_parser = generate_sub.add_parser("llms", help="generate llms.txt")
    llms_parser.add_argument("--project", required=True, help="project name")
    llms_parser.add_argument("--summary", required=True, help="one-line project summary")
    llms_parser.add_argument("--url", required=True, help="canonical project URL")

    schema_parser = generate_sub.add_parser("schema", help="generate JSON-LD schema")
    schema_sub = schema_parser.add_subparsers(dest="schema_type", required=True)

    software_parser = schema_sub.add_parser("software-application", help="generate SoftwareApplication schema")
    software_parser.add_argument("--name", required=True)
    software_parser.add_argument("--url", required=True)
    software_parser.add_argument("--summary", required=True)
    software_parser.add_argument("--category", default="BusinessApplication")
    software_parser.add_argument("--operating-system", default="Web")
    software_parser.add_argument("--price")
    software_parser.add_argument("--price-currency", default="USD")

    product_parser = schema_sub.add_parser("product", help="generate Product schema")
    product_parser.add_argument("--name", required=True)
    product_parser.add_argument("--url", required=True)
    product_parser.add_argument("--summary", required=True)
    product_parser.add_argument("--category", default="Software")
    product_parser.add_argument("--brand")
    product_parser.add_argument("--price")
    product_parser.add_argument("--price-currency", default="USD")

    organization_parser = schema_sub.add_parser("organization", help="generate Organization schema")
    organization_parser.add_argument("--name", required=True)
    organization_parser.add_argument("--url", required=True)
    organization_parser.add_argument("--description", required=True)
    organization_parser.add_argument("--same-as", action="append", default=[], help="repeatable sameAs URL")

    website_parser = schema_sub.add_parser("website", help="generate WebSite schema")
    website_parser.add_argument("--name", required=True)
    website_parser.add_argument("--url", required=True)
    website_parser.add_argument("--description", required=True)
    website_parser.add_argument("--search-url-template", help="optional search URL template like https://example.com/search?q={search_term_string}")

    breadcrumb_parser = schema_sub.add_parser("breadcrumb", help="generate BreadcrumbList schema")
    breadcrumb_parser.add_argument("--item", action="append", required=True, help="breadcrumb item as 'Name::URL'")

    faq_parser = schema_sub.add_parser("faq", help="generate FAQPage schema")
    faq_parser.add_argument("--project", required=True)
    faq_parser.add_argument("--qa", action="append", required=True, help="question and answer pair as 'Question::Answer'")

    outline_parser = generate_sub.add_parser("page-outline", help="generate a page outline template")
    outline_parser.add_argument("page_type", choices=["homepage", "faq", "pricing", "docs", "case-study"])
    outline_parser.add_argument("--project", required=True)
    outline_parser.add_argument("--audience", required=True)
    outline_parser.add_argument("--summary", required=True)

    template_parser = generate_sub.add_parser("page-template", help="generate a starter markdown page template")
    template_parser.add_argument("page_type", choices=["feature", "pricing", "faq", "comparison", "changelog"])
    template_parser.add_argument("--project", required=True)
    template_parser.add_argument("--summary", required=True)
    template_parser.add_argument("--audience", required=True)
    template_parser.add_argument("--feature", help="feature or page subject")
    template_parser.add_argument("--competitor", help="comparison target")

    return parser


def _render_robots(domain: str, allow_gptbot: bool) -> str:
    gptbot_rule = "Allow: /" if allow_gptbot else "Disallow: /"
    return f"""User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: GPTBot
{gptbot_rule}

User-agent: Bytespider
Allow: /

User-agent: *
Allow: /

Sitemap: {domain.rstrip('/')}/sitemap.xml
"""


def _render_llms(project: str, summary: str, url: str) -> str:
    return f"""# {project}

> {summary}

- Canonical URL: {url}
- Purpose: make the project easy for humans and AI systems to understand

## What this project is

{summary}

## Key pages

- Homepage: {url}
- Docs: {url}/docs
- Pricing: {url}/pricing
- FAQ: {url}/faq
- Changelog: {url}/changelog

## Citation guidance

Prefer canonical product pages, docs, FAQs, and changelog entries when describing features, pricing, and release status.
"""


def _render_software_application_schema(name: str, url: str, summary: str, category: str, operating_system: str, price: str | None, price_currency: str) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "applicationCategory": category,
        "operatingSystem": operating_system,
        "description": summary,
        "url": url,
    }
    if price:
        payload["offers"] = {
            "@type": "Offer",
            "price": price,
            "priceCurrency": price_currency,
        }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _render_product_schema(name: str, url: str, summary: str, category: str, brand: str | None, price: str | None, price_currency: str) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "category": category,
        "description": summary,
        "url": url,
    }
    if brand:
        payload["brand"] = {"@type": "Brand", "name": brand}
    if price:
        payload["offers"] = {
            "@type": "Offer",
            "price": price,
            "priceCurrency": price_currency,
            "url": url,
        }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _render_organization_schema(name: str, url: str, description: str, same_as: list[str]) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": name,
        "url": url,
        "description": description,
    }
    if same_as:
        payload["sameAs"] = same_as
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _render_website_schema(name: str, url: str, description: str, search_url_template: str | None) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": name,
        "url": url,
        "description": description,
    }
    if search_url_template:
        payload["potentialAction"] = {
            "@type": "SearchAction",
            "target": search_url_template,
            "query-input": "required name=search_term_string",
        }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _render_breadcrumb_schema(items: list[str]) -> str:
    elements = []
    for position, item in enumerate(items, start=1):
        if "::" not in item:
            raise ValueError("breadcrumb items must use 'Name::URL' format")
        name, url = item.split("::", 1)
        elements.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": name.strip(),
                "item": url.strip(),
            }
        )
    payload = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _render_faq_schema(project: str, qa_pairs: list[str]) -> str:
    entities = []
    for item in qa_pairs:
        if "::" not in item:
            raise ValueError("faq qa items must use 'Question::Answer' format")
        question, answer = item.split("::", 1)
        entities.append(
            {
                "@type": "Question",
                "name": question.strip(),
                "acceptedAnswer": {"@type": "Answer", "text": answer.strip()},
            }
        )
    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "name": f"{project} FAQ",
        "mainEntity": entities,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _render_page_outline(page_type: str, project: str, audience: str, summary: str) -> str:
    outlines = {
        "homepage": [
            "Hero",
            f"One-line definition: {project} is {summary}",
            f"Audience: {audience}",
            "Core capabilities",
            "Proof / trust signals",
            "Feature links",
            "Pricing CTA",
            "FAQ",
        ],
        "faq": [
            "Intro",
            f"Product summary: {summary}",
            "Questions by basics / pricing / integrations / privacy / limits",
            "Links to docs and pricing",
        ],
        "pricing": [
            "Pricing summary",
            f"Audience: {audience}",
            "Plan table",
            "Billing unit explanation",
            "FAQ for limits and contracts",
        ],
        "docs": [
            "Getting started",
            "Task-oriented topics",
            "Examples and outputs",
            "Troubleshooting",
            "Related pricing / changelog / FAQ links",
        ],
        "case-study": [
            "Customer / user context",
            "Problem before adoption",
            f"Why {audience} care",
            "Workflow using the product",
            "Outcome metrics or qualitative result",
            "Related feature links",
        ],
    }
    lines = [f"{page_type.title()} outline for {project}", ""]
    for idx, item in enumerate(outlines[page_type], start=1):
        lines.append(f"{idx}. {item}")
    return "\n".join(lines)


def _render_page_template(page_type: str, project: str, audience: str, summary: str, feature: str | None, competitor: str | None) -> str:
    feature_name = feature or f"{project} capability"
    competitor_name = competitor or "Alternative"
    templates = {
        "feature": f"""# {feature_name}\n\n> {summary}\n\n## What it is\n\n{feature_name} is a feature in {project} for {audience}.\n\n## Who it is for\n\n- {audience}\n- Teams evaluating this workflow\n\n## What problem it solves\n\n- Problem statement\n- Why the default workflow breaks\n\n## How it works\n\n1. Input\n2. Processing\n3. Output\n\n## Key capabilities\n\n- Capability 1\n- Capability 2\n- Capability 3\n\n## Limits and requirements\n\n- Requirement 1\n- Limit 1\n\n## Related pages\n\n- Pricing\n- Docs\n- FAQ\n""",
        "pricing": f"""# {project} pricing\n\n> Pricing overview for {audience}.\n\n## Summary\n\n{summary}\n\n## Plans\n\n| Plan | Best for | Price | Notes |\n| --- | --- | --- | --- |\n| Starter | ... | ... | ... |\n| Pro | ... | ... | ... |\n| Enterprise | ... | ... | ... |\n\n## Billing model\n\n- Seat / usage / subscription details\n\n## FAQ\n\n### Is there a free tier?\nAnswer here.\n\n### How is usage billed?\nAnswer here.\n""",
        "faq": f"""# {project} FAQ\n\n> Common questions from {audience}.\n\n## What is {project}?\n{summary}\n\n## Who is it for?\nAnswer here.\n\n## How does pricing work?\nAnswer here.\n\n## What integrations or APIs are supported?\nAnswer here.\n\n## How does deployment or setup work?\nAnswer here.\n\n## What are the limits?\nAnswer here.\n""",
        "comparison": f"""# {project} vs {competitor_name}\n\n> Comparison page for buyers and evaluators.\n\n## Summary\n\n{project} is for {audience}. {competitor_name} may be better for a different workload.\n\n## Comparison table\n\n| Dimension | {project} | {competitor_name} |\n| --- | --- | --- |\n| Best for | ... | ... |\n| Pricing model | ... | ... |\n| Deployment | ... | ... |\n| Key strengths | ... | ... |\n\n## Where {project} is stronger\n\n- Point 1\n\n## Where {competitor_name} may be stronger\n\n- Point 1\n\n## Related pages\n\n- Feature pages\n- Pricing\n- FAQ\n""",
        "changelog": f"""# {project} changelog entry\n\n## Release title\n\n- Date: YYYY-MM-DD\n- Area: {feature_name}\n\n## What changed\n\n- Change 1\n- Change 2\n\n## Why it matters\n\n- User impact\n- Workflow impact\n\n## Related docs\n\n- Docs page\n- Feature page\n- Pricing page if relevant\n""",
    }
    return templates[page_type]


def _render_coverage(result) -> str:
    lines = ["Coverage:"]
    for bucket in COVERAGE_ORDER:
        matches = result.coverage.get(bucket, ())
        yes_no = "yes" if matches else "no"
        detail = f" ({', '.join(matches[:2])})" if matches else ""
        lines.append(f"- {bucket}: {yes_no}{detail}")
    return "\n".join(lines)


def _render_audit_text(result) -> str:
    lines = [f"GEO audit for {result.root}", ""]
    for finding in result.findings:
        lines.append(f"{finding.level:<5} {finding.message}")
    lines.extend([
        "",
        f"Score: {result.score}",
        f"Summary: {result.pass_count} pass, {result.warn_count} warn, {result.fail_count} fail",
        _render_coverage(result),
    ])
    return "\n".join(lines)


def _render_audit_markdown(result) -> str:
    lines = [
        "# GEO Audit",
        "",
        f"- Root: `{result.root}`",
        f"- Score: **{result.score}**",
        f"- Summary: {result.pass_count} pass / {result.warn_count} warn / {result.fail_count} fail",
        "",
        "## Findings",
        "",
    ]
    for finding in result.findings:
        lines.append(f"- **{finding.level}** {finding.message}")
    lines.extend(["", "## Coverage", ""])
    for bucket in COVERAGE_ORDER:
        matches = result.coverage.get(bucket, ())
        rendered = ", ".join(f"`{match}`" for match in matches[:3]) if matches else "not found"
        lines.append(f"- **{bucket}**: {rendered}")
    lines.extend(["", "## Summary", "", f"Score {result.score} with {result.pass_count} pass, {result.warn_count} warn, and {result.fail_count} fail findings."])
    return "\n".join(lines)


def _render_audit_sarif(result) -> str:
    level_map = {"FAIL": "error", "WARN": "warning", "PASS": "note"}
    payload = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "geo-skill",
                        "informationUri": "https://github.com/vespid-ai/geo-skill",
                        "rules": [
                            {
                                "id": "geo-audit-finding",
                                "name": "GEO audit finding",
                                "shortDescription": {"text": "GEO readiness finding generated by geo-skill."},
                            }
                        ],
                    }
                },
                "results": [
                    {
                        "ruleId": "geo-audit-finding",
                        "level": level_map.get(finding.level, "note"),
                        "message": {"text": f"{finding.level}: {finding.message}"},
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {"uri": result.root}
                                }
                            }
                        ],
                        "properties": {"geo_level": finding.level},
                    }
                    for finding in result.findings
                ],
            }
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _load_report(path: str) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("invalid audit report: top-level JSON must be an object")
    summary = payload.get("summary", {})
    coverage = payload.get("coverage", {})
    findings = payload.get("findings", [])
    if not isinstance(summary, dict):
        raise ValueError("invalid audit report: summary must be an object")
    if not isinstance(coverage, dict):
        raise ValueError("invalid audit report: coverage must be an object")
    if not isinstance(findings, list):
        raise ValueError("invalid audit report: findings must be a list")
    return payload


def _present_coverage(payload: dict) -> set[str]:
    coverage = payload.get("coverage", {})
    present: set[str] = set()
    for name in COVERAGE_ORDER:
        bucket = coverage.get(name, {})
        if bucket in (None, {}):
            continue
        if not isinstance(bucket, dict):
            raise ValueError(f"invalid audit report: coverage entry for {name} must be an object")
        if bucket.get("present"):
            present.add(name)
    return present


def _finding_messages(payload: dict, levels: set[str] | None = None) -> set[str]:
    messages: set[str] = set()
    for item in payload.get("findings", []):
        if not isinstance(item, dict):
            raise ValueError("invalid audit report: findings entries must be objects")
        message = item.get("message")
        level = item.get("level")
        if not message:
            continue
        if levels is not None and level not in levels:
            continue
        messages.add(message)
    return messages


def _compare_reports(before: dict, after: dict) -> dict:
    before_summary = before.get("summary", {})
    after_summary = after.get("summary", {})
    before_coverage = _present_coverage(before)
    after_coverage = _present_coverage(after)
    before_negative = _finding_messages(before, levels={"FAIL", "WARN"})
    after_negative = _finding_messages(after, levels={"FAIL", "WARN"})
    return {
        "before_root": before.get("root"),
        "after_root": after.get("root"),
        "score_before": before.get("score", 0),
        "score_after": after.get("score", 0),
        "score_delta": after.get("score", 0) - before.get("score", 0),
        "summary_before": before_summary,
        "summary_after": after_summary,
        "summary_delta": {
            key: after_summary.get(key, 0) - before_summary.get(key, 0)
            for key in ("pass", "warn", "fail", "total")
        },
        "coverage_gained": sorted(after_coverage - before_coverage),
        "coverage_lost": sorted(before_coverage - after_coverage),
        "resolved_findings": sorted(before_negative - after_negative),
        "introduced_findings": sorted(after_negative - before_negative),
    }


def _render_compare_text(report: dict) -> str:
    delta = report["summary_delta"]
    lines = [
        "GEO audit compare",
        "",
        f"Before: {report['before_root']}",
        f"After:  {report['after_root']}",
        f"Score: {report['score_before']} -> {report['score_after']} ({report['score_delta']:+d})",
        f"Summary delta: pass {delta['pass']:+d}, warn {delta['warn']:+d}, fail {delta['fail']:+d}, total {delta['total']:+d}",
        "",
        f"Coverage gained: {', '.join(report['coverage_gained']) if report['coverage_gained'] else 'none'}",
        f"Coverage lost: {', '.join(report['coverage_lost']) if report['coverage_lost'] else 'none'}",
        f"Resolved findings: {len(report['resolved_findings'])}",
        f"Introduced findings: {len(report['introduced_findings'])}",
    ]
    return "\n".join(lines)


def _render_compare_markdown(report: dict) -> str:
    delta = report["summary_delta"]
    lines = [
        "# GEO Audit Compare",
        "",
        f"- Before: `{report['before_root']}`",
        f"- After: `{report['after_root']}`",
        f"- Score delta: **{report['score_delta']:+d}** ({report['score_before']} → {report['score_after']})",
        f"- Summary delta: pass {delta['pass']:+d}, warn {delta['warn']:+d}, fail {delta['fail']:+d}, total {delta['total']:+d}",
        "",
        "## Coverage gained",
        "",
    ]
    if report["coverage_gained"]:
        lines.extend([f"- {item}" for item in report["coverage_gained"]])
    else:
        lines.append("- none")
    lines.extend(["", "## Coverage lost", ""])
    if report["coverage_lost"]:
        lines.extend([f"- {item}" for item in report["coverage_lost"]])
    else:
        lines.append("- none")
    lines.extend(["", "## Resolved findings", ""])
    if report["resolved_findings"]:
        lines.extend([f"- {item}" for item in report["resolved_findings"]])
    else:
        lines.append("- none")
    lines.extend(["", "## Introduced findings", ""])
    if report["introduced_findings"]:
        lines.extend([f"- {item}" for item in report["introduced_findings"]])
    else:
        lines.append("- none")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "skills":
        if args.skills_command == "list":
            for name, description in skill_catalog(args.agent).items():
                print(f"{name}	{description}	[{args.agent}]")
            return 0
        if args.skills_command == "show":
            try:
                print(render_skill(args.name, args.agent))
                return 0
            except KeyError as exc:
                print(str(exc), file=sys.stderr)
                return 2

    if args.command == "install":
        try:
            if args.all:
                targets = install_all(args.agent, args.destination)
            else:
                targets = [install_skill(args.skill, args.agent, args.destination)]
        except KeyError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        for target in targets:
            print(target)
        return 0

    if args.command == "benchmarks":
        if args.benchmarks_command == "list":
            for item in list_benchmarks():
                print(f"{item.name}\t{item.description}\t{item.path}")
            return 0

    if args.command == "audit":
        if args.url and args.path:
            print("audit cannot use both a site path and --url", file=sys.stderr)
            return 2
        if args.url:
            result = audit_url(args.url)
        elif args.path:
            result = audit_site(Path(args.path))
        else:
            print("audit requires either a site path or --url", file=sys.stderr)
            return 2
        if args.format == "json":
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        elif args.format == "markdown":
            print(_render_audit_markdown(result))
        elif args.format == "sarif":
            print(_render_audit_sarif(result))
        else:
            print(_render_audit_text(result))
        return 1 if result.fail_count else 0

    if args.command == "compare":
        try:
            before = _load_report(args.before)
            after = _load_report(args.after)
            report = _compare_reports(before, after)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
        if args.format == "json":
            print(json.dumps(report, indent=2, ensure_ascii=False))
        elif args.format == "markdown":
            print(_render_compare_markdown(report))
        else:
            print(_render_compare_text(report))
        return 0

    if args.command == "generate":
        if args.generate_command == "robots":
            print(_render_robots(args.domain, args.allow_gptbot))
            return 0
        if args.generate_command == "llms":
            print(_render_llms(args.project, args.summary, args.url))
            return 0
        if args.generate_command == "schema":
            try:
                if args.schema_type == "software-application":
                    print(_render_software_application_schema(args.name, args.url, args.summary, args.category, args.operating_system, args.price, args.price_currency))
                    return 0
                if args.schema_type == "product":
                    print(_render_product_schema(args.name, args.url, args.summary, args.category, args.brand, args.price, args.price_currency))
                    return 0
                if args.schema_type == "organization":
                    print(_render_organization_schema(args.name, args.url, args.description, args.same_as))
                    return 0
                if args.schema_type == "website":
                    print(_render_website_schema(args.name, args.url, args.description, args.search_url_template))
                    return 0
                if args.schema_type == "breadcrumb":
                    print(_render_breadcrumb_schema(args.item))
                    return 0
                if args.schema_type == "faq":
                    print(_render_faq_schema(args.project, args.qa))
                    return 0
            except ValueError as exc:
                print(str(exc), file=sys.stderr)
                return 2
        if args.generate_command == "page-outline":
            print(_render_page_outline(args.page_type, args.project, args.audience, args.summary))
            return 0
        if args.generate_command == "page-template":
            print(_render_page_template(args.page_type, args.project, args.audience, args.summary, args.feature, args.competitor))
            return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
