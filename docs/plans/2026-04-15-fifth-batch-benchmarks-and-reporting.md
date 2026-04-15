# Fifth Batch Benchmarks and Reporting Implementation Plan

> For Hermes: use subagent-driven-development or strict local TDD to implement this plan task-by-task.

Goal: ship the fifth batch in one pass by adding bundled benchmark fixtures, richer audit export formats, and a before/after compare workflow for GEO audits.

Architecture: keep runtime zero-dependency and agent-friendly. Reuse `AuditResult.to_dict()` as the canonical machine-readable shape, then layer markdown/SARIF/report rendering in the CLI. Add benchmark metadata in a small dedicated Python module and point it at repo-local fixture directories under `benchmarks/`.

Tech Stack: stdlib Python only, existing `argparse` CLI, unittest, static HTML fixtures.

---

### Task 1: Add failing tests for benchmark listing and compare/report outputs

Objective: define the fifth-batch surface before touching implementation.

Files:
- Modify: `tests/test_cli.py`
- Modify: `tests/test_audit.py`

Steps:
1. Add a failing CLI test for `geo-skill benchmarks list`.
2. Add a failing CLI test for `geo-skill audit <site> --format markdown`.
3. Add a failing CLI test for `geo-skill audit <site> --format sarif`.
4. Add a failing CLI test for `geo-skill compare before.json after.json --format json`.
5. Run targeted unittest commands and confirm the new tests fail for the expected missing-feature reason.

### Task 2: Add bundled benchmark fixtures and metadata

Objective: ship inspectable benchmark fixtures that users and tests can audit directly.

Files:
- Create: `src/geo_skill/benchmarks.py`
- Create: `benchmarks/weak-marketing-site/index.html`
- Create: `benchmarks/weak-marketing-site/robots.txt`
- Create: `benchmarks/docs-strong-site/index.html`
- Create: `benchmarks/docs-strong-site/robots.txt`
- Create: `benchmarks/docs-strong-site/sitemap.xml`
- Create: `benchmarks/docs-strong-site/llms.txt`
- Create: `benchmarks/docs-strong-site/docs/index.html`
- Create: `benchmarks/docs-strong-site/pricing/index.html`
- Create: `benchmarks/docs-strong-site/changelog/index.html`
- Create: `benchmarks/oss-release-site/index.html`
- Create: `benchmarks/oss-release-site/robots.txt`
- Create: `benchmarks/oss-release-site/sitemap.xml`
- Create: `benchmarks/oss-release-site/releases/index.html`

Steps:
1. Define benchmark names, one-line descriptions, and filesystem paths in `benchmarks.py`.
2. Add small, readable fixture sites that represent weak, medium, and strong GEO surfaces.
3. Keep the fixtures human-readable in GitHub.

### Task 3: Implement markdown and SARIF audit exports

Objective: let agents and CI consume richer report formats without external tools.

Files:
- Modify: `src/geo_skill/cli.py`
- Modify: `src/geo_skill/audit.py` only if shared helpers are needed

Steps:
1. Extend `audit --format` choices from `text|json` to `text|json|markdown|sarif`.
2. Add a markdown renderer that includes score, summary, findings, and coverage.
3. Add a SARIF renderer that maps FAIL/WARN/PASS findings into SARIF results.
4. Keep stdout behavior consistent: render to stdout, exit code still depends on fail_count.

### Task 4: Implement compare workflow for before/after audit JSON reports

Objective: make GEO progress reviewable after migrations or content changes.

Files:
- Modify: `src/geo_skill/cli.py`
- Optionally create: `src/geo_skill/reporting.py` if helper density gets high
- Modify: `tests/test_cli.py`

Steps:
1. Add a new top-level CLI command: `geo-skill compare before.json after.json`.
2. Support `--format text|json|markdown`.
3. Compare score delta, summary delta, and coverage changes by page type.
4. Flag newly fixed findings and newly introduced regressions separately.

### Task 5: Update docs and versions

Objective: make the fifth batch discoverable and consistent.

Files:
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `pyproject.toml`
- Modify: `src/geo_skill/__init__.py`

Steps:
1. Bump version to `0.5.0`.
2. Document new benchmark/report/compare commands in README examples.
3. Add a new changelog section for `v0.5.0`.
4. Update roadmap wording so completed items move out of P0/P1.

### Task 6: Verify, review, and ship

Objective: release the fifth batch safely.

Files:
- No code target; verification only.

Steps:
1. Run `python -m unittest discover -s tests -v`.
2. Run smoke commands for `benchmarks list`, `audit --format markdown`, `audit --format sarif`, and `compare`.
3. Run an independent review pass.
4. Commit, push, create release `v0.5.0`, and verify CI is green.
