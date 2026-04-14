from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .audit import audit_site
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

    audit_parser = subparsers.add_parser("audit", help="audit a static site directory")
    audit_parser.add_argument("path", help="path to site root")

    generate_parser = subparsers.add_parser("generate", help="generate GEO starter assets")
    generate_sub = generate_parser.add_subparsers(dest="generate_command", required=True)

    robots_parser = generate_sub.add_parser("robots", help="generate robots.txt")
    robots_parser.add_argument("--domain", required=True, help="site domain, like https://example.com")
    robots_parser.add_argument("--allow-gptbot", action="store_true", help="allow GPTBot for training access")

    llms_parser = generate_sub.add_parser("llms", help="generate llms.txt")
    llms_parser.add_argument("--project", required=True, help="project name")
    llms_parser.add_argument("--summary", required=True, help="one-line project summary")
    llms_parser.add_argument("--url", required=True, help="canonical project URL")

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

    if args.command == "audit":
        result = audit_site(Path(args.path))
        print(f"GEO audit for {result.root}")
        print()
        for finding in result.findings:
            print(f"{finding.level:<5} {finding.message}")
        print()
        print(f"Summary: {result.pass_count} pass, {result.warn_count} warn, {result.fail_count} fail")
        return 1 if result.fail_count else 0

    if args.command == "generate":
        if args.generate_command == "robots":
            print(_render_robots(args.domain, args.allow_gptbot))
            return 0
        if args.generate_command == "llms":
            print(_render_llms(args.project, args.summary, args.url))
            return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
