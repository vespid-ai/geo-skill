# geo-skill

[English](./README.md) | [简体中文](./README.zh-CN.md) | 日本語

`geo-skill` は、製品ページ、ドキュメント、料金ページ、FAQ、更新履歴を AI 検索や回答エンジンで見つけやすくし、引用されやすくしたいチーム向けのオープンソース GEO ツールキットです。

提供する価値は 2 つです。

1. GEO readiness を監査し、機械可読な基本アセットを生成する Python CLI
2. Hermes Agent、Claude Code、Codex で再利用できる agent skills

この README は、内部向けの進捗メモではなく、外部ユーザー向けの入口として書き直しています。

## どんな人向けか

- AI プロダクトや agent プロダクトのサイト担当者
- docs-first / API-first で、ドキュメントを AI 検索に強くしたいチーム
- README、docs、release をより引用されやすくしたい OSS プロジェクト
- GEO ワークフローを agent に組み込みたい開発者

## geo-skill でできること

- ローカルの静的サイトや公開 URL の GEO readiness を監査する
- `robots.txt`、`llms.txt`、JSON-LD schema などを生成する
- リニューアル前後・移行前後の GEO レポートを比較する
- markdown / SARIF で人向け・CI 向けのレポートを出力する
- GEO skills を Hermes / Claude / Codex にインストールする
- 弱い GEO / 強い GEO の benchmark fixture を参照する

## なぜ使うのか

GEO の話は抽象的すぎることが多く、実装に落ちません。実際に必要なのは、次のような具体的な仕事です。

- crawler allow / deny ポリシー
- sitemap と URL の健全性
- 製品の事実が明確に書かれているか
- FAQ / docs のカバレッジ
- 料金情報の明確さ
- trust / entity ページの整備
- changelog による freshness signal
- structured data
- 機械可読なページ構造
- OSS リポジトリの discoverability

`geo-skill` は、これらを実務で使える監査・生成・比較ワークフローに変えます。

## クイックスタート

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
geo-skill skills list
```

## よくあるワークフロー

ローカル成果物を監査する：

```bash
geo-skill audit ./public
```

公開サイトを監査して markdown を出力する：

```bash
geo-skill audit --url https://example.com --format markdown > geo-audit.md
```

基本アセットを生成する：

```bash
geo-skill generate robots --domain https://example.com
geo-skill generate llms --project "Example" --summary "AI workflow product" --url https://example.com
geo-skill generate schema software-application --name "Example" --url https://example.com --summary "AI workflow product"
```

変更前後の GEO レポートを比較する：

```bash
geo-skill compare before.json after.json --format markdown > geo-diff.md
```

## CLI コマンド

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

## 内蔵 benchmark fixtures

- `weak-marketing-site` — 薄いマーケティング面で、crawl / support coverage が弱い例
- `docs-strong-site` — docs / pricing / changelog が強い GEO 例
- `oss-release-site` — OSS の release / docs / repo discoverability を意識した例

これらの benchmark はリポジトリ内だけでなく、インストール後のパッケージにも含まれます。

## Agent 互換性

### Hermes Agent
- `skills/hermes/<skill-name>/SKILL.md`
- インストール先: `~/.hermes/skills/geo/`

### Claude Code
- `.claude/skills/*.md`
- インストール先: `~/.claude/skills/`

### Codex
- `.agents/skills/<skill-name>/SKILL.md`
- Codex の skill ディレクトリ規約に沿っています

## 内蔵 GEO skills

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

## リポジトリ構成

```text
.agents/skills/          Codex-ready skills
.claude/skills/          Claude-ready skills
benchmarks/              GitHub 上で読める benchmark fixtures
skills/hermes/           Hermes-ready skills
src/geo_skill/           CLI 実装
src/geo_skill/data/      インストール済みパッケージ用 benchmark データ
tests/                   単体テスト
docs/plans/              実装プラン
```

## 設計原則

- runtime dependency を増やさない
- CLI は agent / script から呼びやすく保つ
- README は外部ユーザー向けにわかりやすくする
- OpenAI GEO と ByteDance GEO は別の discovery surface として扱う
- ページタイプを GEO の第一級対象として扱う
- slogan より製品の事実を重視する

## Roadmap

### P0
- より豊富なページタイプ heuristics
- benchmark fixture の拡張
- compare の threshold と CI gate

### P1
- repo-scoped installer helpers
- Codex plugin packaging
- localized / API-first benchmark packs

### P2
- より多くの agent-specific skill variants
- 巨大な sitemap index への対応
- 大規模 live audit 向けの並列処理

## Contributing

Issue と PR は歓迎です。新しい GEO workflow を追加する場合は、以下をできるだけ維持してください。

- README の例は外部ユーザーにわかりやすく
- benchmark fixtures は GitHub 上で読みやすく
- CLI 出力は agent / script に安定的
- Hermes / Claude / Codex の skill variants はできるだけ揃える

## License

MIT
