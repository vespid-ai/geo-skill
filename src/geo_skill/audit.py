from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class Finding:
    level: str
    message: str


@dataclass(frozen=True)
class AuditResult:
    root: Path
    findings: List[Finding]

    @property
    def pass_count(self) -> int:
        return sum(1 for item in self.findings if item.level == "PASS")

    @property
    def warn_count(self) -> int:
        return sum(1 for item in self.findings if item.level == "WARN")

    @property
    def fail_count(self) -> int:
        return sum(1 for item in self.findings if item.level == "FAIL")


def _sample_html_files(root: Path, limit: int = 10) -> Iterable[Path]:
    html_files = sorted(root.rglob("*.html"))
    return html_files[:limit]


def _check_file(findings: List[Finding], path: Path, label: str) -> None:
    if path.exists():
        findings.append(Finding("PASS", f"{label} exists"))
    else:
        findings.append(Finding("WARN", f"{label} missing"))


def audit_site(root: str | Path) -> AuditResult:
    site_root = Path(root).expanduser().resolve()
    findings: List[Finding] = []

    if not site_root.exists() or not site_root.is_dir():
        return AuditResult(site_root, [Finding("FAIL", "site root does not exist or is not a directory")])

    _check_file(findings, site_root / "robots.txt", "robots.txt")
    _check_file(findings, site_root / "sitemap.xml", "sitemap.xml")
    _check_file(findings, site_root / "llms.txt", "llms.txt")

    index_html = site_root / "index.html"
    if not index_html.exists():
        findings.append(Finding("FAIL", "index.html missing"))
        return AuditResult(site_root, findings)

    html = index_html.read_text(encoding="utf-8", errors="ignore")
    if "<title" in html.lower():
        findings.append(Finding("PASS", "index.html has title tag"))
    else:
        findings.append(Finding("WARN", "index.html missing title tag"))

    if 'name="description"' in html.lower() or "name='description'" in html.lower():
        findings.append(Finding("PASS", "index.html has meta description"))
    else:
        findings.append(Finding("WARN", "index.html missing meta description"))

    if 'property="og:title"' in html.lower() or "property='og:title'" in html.lower():
        findings.append(Finding("PASS", "index.html has Open Graph title"))
    else:
        findings.append(Finding("WARN", "index.html missing Open Graph title"))

    html_files = list(_sample_html_files(site_root))
    if not html_files:
        findings.append(Finding("WARN", "no HTML files found for structured-data sampling"))
    else:
        found_json_ld = False
        faq_like_pages = 0
        for path in html_files:
            content = path.read_text(encoding="utf-8", errors="ignore").lower()
            if 'application/ld+json' in content:
                found_json_ld = True
            if "faq" in content or "frequently asked" in content:
                faq_like_pages += 1
        if found_json_ld:
            findings.append(Finding("PASS", "JSON-LD structured data found in sampled HTML files"))
        else:
            findings.append(Finding("WARN", "no JSON-LD structured data found in sampled HTML files"))
        if faq_like_pages:
            findings.append(Finding("PASS", f"FAQ-like content found in {faq_like_pages} sampled HTML file(s)"))
        else:
            findings.append(Finding("WARN", "no FAQ-like content found in sampled HTML files"))

    return AuditResult(site_root, findings)
