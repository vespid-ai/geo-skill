# geo-skill

[English](./README.md) | 简体中文 | [日本語](./README.ja.md)

`geo-skill` 是一个开源 GEO 工具包，面向希望提升产品、文档、定价页、FAQ、更新日志在 AI 搜索与答案引擎中可发现性和可引用性的团队。

它提供两部分能力：

1. 一个实用的 Python CLI，用于审计 GEO readiness、生成核心机器可读资产
2. 一组可复用的 agent skills，可被 Hermes Agent、Claude Code、Codex 加载使用

这个仓库的 README 现在是给外部用户看的，不是给内部维护者看的“批次记录”。

## 适合谁

- 做 AI 产品、Agent 产品、SaaS 产品的网站团队
- docs-first / API-first，希望文档更容易被 AI 搜索引用的团队
- 想让 GitHub README、文档、release 更容易被引用的开源项目
- 想把 GEO 工作流塞进 agent 的开发者

## 你可以用 geo-skill 做什么

- 审计本地静态站点或线上 URL 的 GEO 基础能力
- 生成 `robots.txt`、`llms.txt`、JSON-LD schema 等 starter assets
- 对比改版前后、迁移前后的 GEO 报告差异
- 导出 markdown 或 SARIF 报告给人看、给 CI 用
- 把 GEO skills 安装到 Hermes / Claude / Codex
- 用内置 benchmark fixtures 对照弱 / 强 GEO 站点模式

## 为什么有人会用它

很多 GEO 建议都太空。真正有价值的工作其实很具体：

- crawler allow / deny 策略
- sitemap 和 URL 稳定性
- 产品事实表达是否清楚
- FAQ / docs 覆盖是否到位
- 定价是否清晰
- trust / entity 页面是否完整
- changelog 是否提供 freshness signal
- structured data 是否合理
- 页面是否对机器可读
- 开源仓库是否容易被引用

`geo-skill` 的目标就是把这些变成可执行、可复用、可对比的流程。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
geo-skill skills list
```

## 常见工作流

审计本地构建产物：

```bash
geo-skill audit ./public
```

审计线上站点并导出 markdown：

```bash
geo-skill audit --url https://example.com --format markdown > geo-audit.md
```

生成基础 discovery assets：

```bash
geo-skill generate robots --domain https://example.com
geo-skill generate llms --project "Example" --summary "AI workflow product" --url https://example.com
geo-skill generate schema software-application --name "Example" --url https://example.com --summary "AI workflow product"
```

对比改版前后 GEO 报告：

```bash
geo-skill compare before.json after.json --format markdown > geo-diff.md
```

## CLI 命令

```bash
geo-skill skills list
geo-skill skills show openai-chatgpt-search --agent hermes
geo-skill install --agent codex --all
geo-skill install --agent claude --skill geo-site-readiness
geo-skill benchmarks list
geo-skill audit ./site
geo-skill audit --url https://example.com
geo-skill audit ./site --format json
geo-skill audit ./site --format markdown
geo-skill audit ./site --format sarif
geo-skill compare before.json after.json
geo-skill compare before.json after.json --format markdown
geo-skill generate robots --domain https://example.com
geo-skill generate llms --project GeoSkill --summary "Open-source GEO skill pack" --url https://example.com
```

## 内置 benchmark fixtures

- `weak-marketing-site` —— 很薄的营销页，crawl / support coverage 都偏弱
- `docs-strong-site` —— docs / pricing / changelog 更完整的较强 GEO 示例
- `oss-release-site` —— 更适合开源项目的 release / docs / repo discoverability 示例

这些 benchmark 不只在仓库里可看，在安装后的包里也可用。

## Agent 兼容性

### Hermes Agent
- 路径：`skills/hermes/<skill-name>/SKILL.md`
- 安装目标：`~/.hermes/skills/geo/`

### Claude Code
- 路径：`.claude/skills/*.md`
- 安装目标：`~/.claude/skills/`

### Codex
- 路径：`.agents/skills/<skill-name>/SKILL.md`
- 遵循 Codex skill 目录约定

## 内置 GEO skills

### Search surface
- `openai-chatgpt-search`
- `doubao-bytespider`
- `geo-bing-webmaster-foundation`
- `geo-site-readiness`
- `geo-structured-data-software-sites`

### Content / page modeling
- `geo-content-modeling`
- `geo-homepage-positioning`
- `geo-feature-pages`
- `geo-pricing-pages`
- `geo-faq-coverage`
- `geo-docs-help-center`
- `geo-changelog-freshness`
- `geo-comparison-pages`
- `geo-trust-and-entity-pages`

### Distribution / repo
- `geo-oss-repo-geo`
- `geo-launch-distribution`

### Expansion
- `geo-multilingual-localization`
- `geo-api-docs-geo`
- `geo-case-studies-social-proof`
- `geo-site-migration-url-stability`

## 仓库结构

```text
.agents/skills/          Codex-ready skills
.claude/skills/          Claude-ready skills
benchmarks/              仓库内可直接阅读的 benchmark fixtures
skills/hermes/           Hermes-ready skills
src/geo_skill/           CLI 实现
src/geo_skill/data/      安装包内自带 benchmark 数据
tests/                   单元测试
docs/plans/              实现计划
```

## 设计原则

- 零运行时依赖
- CLI 对 agent / script 友好
- README 面向外部用户，而不是只面向维护者
- OpenAI GEO 与 ByteDance GEO 分开建模
- 页面类型是 GEO 工作的一等公民
- 产品事实表达比 slogan 更重要

## 路线图

### P0
- 更丰富的页面类型 heuristics
- 更丰富的 benchmark fixtures
- compare 阈值与 CI gate

### P1
- repo-scoped installer helpers
- Codex plugin packaging
- 更多 localized / API-first benchmark packs

### P2
- 更多 agent-specific skill 变体
- 超大 sitemap index crawling
- 大规模 live audit 的并发能力

## Contributing

欢迎 issue 和 PR。若你要补新的 GEO workflow，尽量保持：

- README 示例对外部用户友好
- benchmark fixtures 在 GitHub 里可直接读
- CLI 输出对 agent 和脚本稳定
- Hermes / Claude / Codex 的 skill 变体尽量保持一致

## License

MIT
