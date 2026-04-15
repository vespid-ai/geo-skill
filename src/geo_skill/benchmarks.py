from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent.parent
PACKAGE_BENCHMARKS_ROOT = PACKAGE_ROOT / "data" / "benchmarks"


@dataclass(frozen=True)
class BenchmarkSpec:
    name: str
    description: str
    repo_relative_path: str
    package_relative_path: str

    @property
    def repo_path(self) -> Path:
        return REPO_ROOT / self.repo_relative_path

    @property
    def package_path(self) -> Path:
        return PACKAGE_ROOT / self.package_relative_path

    @property
    def path(self) -> Path:
        if self.repo_path.exists():
            return self.repo_path
        return self.package_path


BENCHMARK_SPECS: Dict[str, BenchmarkSpec] = {
    "weak-marketing-site": BenchmarkSpec(
        name="weak-marketing-site",
        description="Thin marketing surface with weak crawl/discovery signals and missing supporting pages.",
        repo_relative_path="benchmarks/weak-marketing-site",
        package_relative_path="data/benchmarks/weak-marketing-site",
    ),
    "docs-strong-site": BenchmarkSpec(
        name="docs-strong-site",
        description="Balanced product/docs/pricing/changelog surface with strong machine-readable GEO basics.",
        repo_relative_path="benchmarks/docs-strong-site",
        package_relative_path="data/benchmarks/docs-strong-site",
    ),
    "oss-release-site": BenchmarkSpec(
        name="oss-release-site",
        description="Open-source launch/release surface emphasizing changelog, releases, and docs linkage.",
        repo_relative_path="benchmarks/oss-release-site",
        package_relative_path="data/benchmarks/oss-release-site",
    ),
}


def list_benchmarks() -> List[BenchmarkSpec]:
    return [BENCHMARK_SPECS[name] for name in sorted(BENCHMARK_SPECS)]
