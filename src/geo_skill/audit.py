from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


COVERAGE_ORDER = ("homepage", "feature", "pricing", "docs", "faq", "changelog", "trust")
COVERAGE_KEYWORDS = {
    "feature": ("/feature", "/features", "/capability", "/capabilities", "/product/", "/solutions/"),
    "pricing": ("/pricing", "/plans", "/plan", "/billing", "/cost"),
    "docs": ("/docs", "/doc", "/documentation", "/guide", "/help", "/api", "/reference"),
    "faq": ("/faq", "/faqs", "frequently-asked"),
    "changelog": ("/changelog", "/release", "/releases", "/updates", "/release-notes"),
    "trust": ("/about", "/contact", "/privacy", "/terms", "/security", "/legal", "/trust"),
}


@dataclass(frozen=True)
class Finding:
    level: str
    message: str


@dataclass(frozen=True)
class AuditResult:
    root: str
    findings: List[Finding]
    coverage: Dict[str, tuple[str, ...]]

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
            "coverage": {
                name: {
                    "present": bool(self.coverage.get(name, ())),
                    "matches": list(self.coverage.get(name, ())),
                }
                for name in COVERAGE_ORDER
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


def _sample_html_files(root: Path, limit: int = 25) -> Iterable[Path]:
    return sorted(root.rglob("*.html"))[:limit]


def _empty_coverage() -> Dict[str, list[str]]:
    return {name: [] for name in COVERAGE_ORDER}


def _freeze_coverage(coverage: Dict[str, list[str]]) -> Dict[str, tuple[str, ...]]:
    return {name: tuple(coverage.get(name, ())) for name in COVERAGE_ORDER}


def _add_coverage_match(coverage: Dict[str, list[str]], bucket: str, match: str) -> None:
    if match not in coverage[bucket]:
        coverage[bucket].append(match)


def _normalize_local_candidate(path: Path, root: Path) -> str:
    relative = path.relative_to(root).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return f"/{relative[:-10].strip('/')}/"
    return f"/{relative.lstrip('/')}"


def _normalize_remote_candidate(candidate: str) -> str:
    parsed = urlparse(candidate)
    path = parsed.path or "/"
    return path if path.startswith("/") else f"/{path}"


def _classify_path(candidate: str, html: str | None = None) -> set[str]:
    normalized = candidate.lower()
    buckets: set[str] = set()

    if normalized in {"/", "/index.html"}:
        buckets.add("homepage")

    for bucket, keywords in COVERAGE_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            buckets.add(bucket)

    if html:
        lower = html.lower()
        if any(token in lower for token in (">faq<", "frequently asked questions", "frequently asked", 'id="faq"', "id='faq'", 'class="faq"', "class='faq'")):
            buckets.add("faq")

    return buckets


def _coverage_findings(findings: List[Finding], coverage: Dict[str, tuple[str, ...]]) -> None:
    for bucket in COVERAGE_ORDER:
        matches = coverage.get(bucket, ())
        label = bucket.replace("_", " ")
        if matches:
            findings.append(Finding("PASS", f"coverage: {label} pages found ({', '.join(matches[:3])})"))
        else:
            findings.append(Finding("WARN", f"coverage: {label} pages not found"))


def _check_file(findings: List[Finding], path: Path, label: str) -> None:
    if path.exists():
        findings.append(Finding("PASS", f"{label} exists"))
    else:
        findings.append(Finding("WARN", f"{label} missing"))


def _fetch_text(url: str, timeout: int = 10) -> FetchResult:
    request = Request(url, headers={"User-Agent": "geo-skill/0.4"})
    with urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        payload = response.read().decode("utf-8", errors="ignore")
        return FetchResult(url=response.geturl(), status=getattr(response, "status", 200), content_type=content_type, text=payload)


def _fetch_optional(findings: List[Finding], base_url: str, relative_path: str, label: str, timeout: int) -> FetchResult | None:
    target = urljoin(base_url, relative_path)
    try:
        result = _fetch_text(target, timeout=timeout)
    except HTTPError as exc:
        findings.append(Finding("WARN", f"{label} returned HTTP {exc.code}"))
        return None
    except URLError as exc:
        findings.append(Finding("WARN", f"{label} fetch failed: {exc.reason}"))
        return None
    findings.append(Finding("PASS", f"{label} reachable at {result.url}"))
    return result


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

    if "application/ld+json" in lower:
        findings.append(Finding("PASS", f"{label} has JSON-LD structured data"))
    else:
        findings.append(Finding("WARN", f"{label} missing JSON-LD structured data"))

    if "faq" in lower or "frequently asked" in lower:
        findings.append(Finding("PASS", f"{label} includes FAQ-like content"))
    else:
        findings.append(Finding("WARN", f"{label} missing FAQ-like content"))


def _extract_sitemap_payload(xml_text: str) -> tuple[str, list[str]]:
    if not xml_text.strip():
        return "unknown", []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return "unknown", []

    root_tag = root.tag.lower()
    kind = "sitemapindex" if root_tag.endswith("sitemapindex") else "urlset"
    urls: list[str] = []
    for element in root.iter():
        if element.tag.endswith("loc") and element.text:
            urls.append(element.text.strip())
    return kind, urls


def _expand_sitemap_urls(sitemap_text: str, timeout: int, depth: int = 0, visited: set[str] | None = None) -> list[str]:
    kind, urls = _extract_sitemap_payload(sitemap_text)
    if kind != "sitemapindex":
        return urls

    if visited is None:
        visited = set()

    expanded: list[str] = []
    if depth >= 2:
        return expanded

    for child_url in urls[:10]:
        if child_url in visited:
            continue
        visited.add(child_url)
        try:
            child_result = _fetch_text(child_url, timeout=timeout)
        except (HTTPError, URLError):
            continue
        expanded.extend(_expand_sitemap_urls(child_result.text, timeout=timeout, depth=depth + 1, visited=visited))
    return expanded


def _collect_local_coverage(site_root: Path) -> Dict[str, tuple[str, ...]]:
    coverage = _empty_coverage()
    for path in sorted(site_root.rglob("*.html")):
        relative = _normalize_local_candidate(path, site_root)
        html = path.read_text(encoding="utf-8", errors="ignore")
        for bucket in _classify_path(relative, html):
            _add_coverage_match(coverage, bucket, relative)
    return _freeze_coverage(coverage)


def _collect_remote_coverage(url: str, html: str, sitemap_text: str | None, timeout: int) -> Dict[str, tuple[str, ...]]:
    coverage = _empty_coverage()
    normalized = _normalize_remote_candidate(url)
    for bucket in _classify_path(normalized, html):
        _add_coverage_match(coverage, bucket, normalized)

    for candidate in _expand_sitemap_urls(sitemap_text or "", timeout=timeout):
        normalized_candidate = _normalize_remote_candidate(candidate)
        for bucket in _classify_path(normalized_candidate):
            _add_coverage_match(coverage, bucket, normalized_candidate)

    return _freeze_coverage(coverage)


def audit_site(root: str | Path) -> AuditResult:
    site_root = Path(root).expanduser().resolve()
    findings: List[Finding] = []

    if not site_root.exists() or not site_root.is_dir():
        return AuditResult(str(site_root), [Finding("FAIL", "site root does not exist or is not a directory")], _freeze_coverage(_empty_coverage()))

    _check_file(findings, site_root / "robots.txt", "robots.txt")
    _check_file(findings, site_root / "sitemap.xml", "sitemap.xml")
    _check_file(findings, site_root / "llms.txt", "llms.txt")

    index_html = site_root / "index.html"
    if not index_html.exists():
        return AuditResult(str(site_root), findings + [Finding("FAIL", "index.html missing")], _freeze_coverage(_empty_coverage()))

    html = index_html.read_text(encoding="utf-8", errors="ignore")
    _audit_html(findings, html, "index.html")

    html_files = list(_sample_html_files(site_root))
    if not html_files:
        findings.append(Finding("WARN", "no HTML files found for structured-data sampling"))
    else:
        found_json_ld = False
        faq_like_pages = 0
        for path in html_files:
            content = path.read_text(encoding="utf-8", errors="ignore").lower()
            if "application/ld+json" in content:
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

    coverage = _collect_local_coverage(site_root)
    _coverage_findings(findings, coverage)
    return AuditResult(str(site_root), findings, coverage)


def audit_url(url: str, timeout: int = 10) -> AuditResult:
    findings: List[Finding] = []
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return AuditResult(url, [Finding("FAIL", "url must include http(s) scheme and hostname")], _freeze_coverage(_empty_coverage()))

    try:
        result = _fetch_text(url, timeout=timeout)
    except HTTPError as exc:
        return AuditResult(url, [Finding("FAIL", f"page returned HTTP {exc.code}")], _freeze_coverage(_empty_coverage()))
    except URLError as exc:
        return AuditResult(url, [Finding("FAIL", f"page fetch failed: {exc.reason}")], _freeze_coverage(_empty_coverage()))

    findings.append(Finding("PASS", f"page reachable at {result.url}"))
    if result.content_type.lower().startswith("text/html"):
        findings.append(Finding("PASS", f"page content-type is HTML ({result.content_type})"))
    else:
        findings.append(Finding("WARN", f"page content-type is {result.content_type or 'unknown'}"))

    final = urlparse(result.url)
    origin = f"{final.scheme}://{final.netloc}/"
    _fetch_optional(findings, origin, "robots.txt", "robots.txt", timeout)
    sitemap_result = _fetch_optional(findings, origin, "sitemap.xml", "sitemap.xml", timeout)
    _fetch_optional(findings, origin, "llms.txt", "llms.txt", timeout)
    _audit_html(findings, result.text, "page")

    coverage = _collect_remote_coverage(result.url, result.text, sitemap_result.text if sitemap_result else None, timeout=timeout)
    _coverage_findings(findings, coverage)
    return AuditResult(result.url, findings, coverage)
