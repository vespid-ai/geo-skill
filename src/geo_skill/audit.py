from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Finding:
    level: str
    message: str


@dataclass(frozen=True)
class AuditResult:
    root: str
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

    @property
    def total_count(self) -> int:
        return len(self.findings)

    @property
    def score(self) -> int:
        if not self.findings:
            return 0
        raw = (self.pass_count + 0.5 * self.warn_count) / self.total_count
        return round(raw * 100)

    def to_dict(self) -> dict:
        return {
            "root": self.root,
            "score": self.score,
            "summary": {
                "pass": self.pass_count,
                "warn": self.warn_count,
                "fail": self.fail_count,
                "total": self.total_count,
            },
            "findings": [
                {"level": item.level, "message": item.message}
                for item in self.findings
            ],
        }


@dataclass(frozen=True)
class FetchResult:
    url: str
    status: int
    content_type: str
    text: str


def _sample_html_files(root: Path, limit: int = 10) -> Iterable[Path]:
    return sorted(root.rglob("*.html"))[:limit]


def _check_file(findings: List[Finding], path: Path, label: str) -> None:
    if path.exists():
        findings.append(Finding("PASS", f"{label} exists"))
    else:
        findings.append(Finding("WARN", f"{label} missing"))


def _fetch_text(url: str, timeout: int = 10) -> FetchResult:
    request = Request(url, headers={"User-Agent": "geo-skill/0.1"})
    with urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        payload = response.read().decode("utf-8", errors="ignore")
        return FetchResult(url=response.geturl(), status=getattr(response, "status", 200), content_type=content_type, text=payload)


def _check_remote_file(findings: List[Finding], base_url: str, relative_path: str, label: str, timeout: int) -> None:
    target = urljoin(base_url, relative_path)
    try:
        result = _fetch_text(target, timeout=timeout)
    except HTTPError as exc:
        findings.append(Finding("WARN", f"{label} returned HTTP {exc.code}"))
        return
    except URLError as exc:
        findings.append(Finding("WARN", f"{label} fetch failed: {exc.reason}"))
        return
    findings.append(Finding("PASS", f"{label} reachable at {result.url}"))


def _audit_html(findings: List[Finding], html: str, label: str) -> None:
    lower = html.lower()
    if "<title" in lower:
        findings.append(Finding("PASS", f"{label} has title tag"))
    else:
        findings.append(Finding("WARN", f"{label} missing title tag"))

    if 'name="description"' in lower or "name='description'" in lower:
        findings.append(Finding("PASS", f"{label} has meta description"))
    else:
        findings.append(Finding("WARN", f"{label} missing meta description"))

    if 'property="og:title"' in lower or "property='og:title'" in lower:
        findings.append(Finding("PASS", f"{label} has Open Graph title"))
    else:
        findings.append(Finding("WARN", f"{label} missing Open Graph title"))

    if 'rel="canonical"' in lower or "rel='canonical'" in lower:
        findings.append(Finding("PASS", f"{label} has canonical link"))
    else:
        findings.append(Finding("WARN", f"{label} missing canonical link"))

    if "<html lang=" in lower or "<html xml:lang=" in lower:
        findings.append(Finding("PASS", f"{label} has html language attribute"))
    else:
        findings.append(Finding("WARN", f"{label} missing html language attribute"))

    if 'application/ld+json' in lower:
        findings.append(Finding("PASS", f"{label} has JSON-LD structured data"))
    else:
        findings.append(Finding("WARN", f"{label} missing JSON-LD structured data"))

    if "faq" in lower or "frequently asked" in lower:
        findings.append(Finding("PASS", f"{label} includes FAQ-like content"))
    else:
        findings.append(Finding("WARN", f"{label} missing FAQ-like content"))


def audit_site(root: str | Path) -> AuditResult:
    site_root = Path(root).expanduser().resolve()
    findings: List[Finding] = []

    if not site_root.exists() or not site_root.is_dir():
        return AuditResult(str(site_root), [Finding("FAIL", "site root does not exist or is not a directory")])

    _check_file(findings, site_root / "robots.txt", "robots.txt")
    _check_file(findings, site_root / "sitemap.xml", "sitemap.xml")
    _check_file(findings, site_root / "llms.txt", "llms.txt")

    index_html = site_root / "index.html"
    if not index_html.exists():
        findings.append(Finding("FAIL", "index.html missing"))
        return AuditResult(str(site_root), findings)

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

    return AuditResult(str(site_root), findings)


def audit_url(url: str, timeout: int = 10) -> AuditResult:
    findings: List[Finding] = []
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return AuditResult(url, [Finding("FAIL", "url must include http(s) scheme and hostname")])

    try:
        result = _fetch_text(url, timeout=timeout)
    except HTTPError as exc:
        return AuditResult(url, [Finding("FAIL", f"page returned HTTP {exc.code}")])
    except URLError as exc:
        return AuditResult(url, [Finding("FAIL", f"page fetch failed: {exc.reason}")])

    findings.append(Finding("PASS", f"page reachable at {result.url}"))
    if result.content_type.lower().startswith("text/html"):
        findings.append(Finding("PASS", f"page content-type is HTML ({result.content_type})"))
    else:
        findings.append(Finding("WARN", f"page content-type is {result.content_type or 'unknown'}"))

    origin = f"{parsed.scheme}://{parsed.netloc}/"
    _check_remote_file(findings, origin, "robots.txt", "robots.txt", timeout)
    _check_remote_file(findings, origin, "sitemap.xml", "sitemap.xml", timeout)
    _check_remote_file(findings, origin, "llms.txt", "llms.txt", timeout)
    _audit_html(findings, result.text, "page")
    return AuditResult(result.url, findings)
