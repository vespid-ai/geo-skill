# geo-skill

[English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md) | Español

`geo-skill` es un toolkit GEO de código abierto para equipos que quieren que su producto, documentación, precios, FAQ y changelog sean más fáciles de descubrir y citar en superficies de búsqueda con IA.

Ofrece dos capacidades principales:

1. un CLI en Python para auditar GEO readiness y generar activos legibles por máquinas
2. un conjunto de skills reutilizables para Hermes Agent, Claude Code y Codex

Este README está pensado para usuarios externos, no como una nota interna de mantenimiento.

## Para quién es

- equipos de producto AI / agent / SaaS
- productos docs-first o API-first que necesitan mejor cobertura en answer engines
- proyectos open source que quieren que su README, docs y releases sean más citables
- builders que quieren meter GEO workflows dentro de sus agentes

## Qué puedes hacer con geo-skill

- auditar un sitio público o una exportación estática local
- generar `robots.txt`, `llms.txt` y schema JSON-LD iniciales
- comparar reportes antes y después de una migración o un cambio de contenido
- exportar reportes en markdown o SARIF para revisión humana y pipelines CI
- instalar GEO skills en Hermes / Claude / Codex
- usar benchmarks incluidos para comparar patrones GEO débiles vs más sólidos

## Por qué sirve

Mucho contenido sobre GEO sigue siendo demasiado abstracto. El trabajo real suele ser operativo:

- políticas crawler allow / deny
- higiene de sitemap y URLs
- claridad de hechos del producto
- cobertura de FAQ y docs
- claridad de pricing
- páginas de trust y entity
- freshness vía changelog
- structured data
- diseño legible por máquinas
- discoverability del repositorio OSS

`geo-skill` convierte eso en checks y workflows repetibles.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
geo-skill skills list
```

## Casos de uso en 30 segundos

- Acabas de lanzar una docs site y quieres saber si pricing, docs, FAQ y trust pages son visibles para AI search.
- Migraste URLs y necesitas un before/after compare report para el equipo.
- Quieres generar `llms.txt`, `robots.txt` y schema starters antes de pulir el contenido manualmente.
- Quieres que tu agente ejecute checks GEO repetibles en lugar de revisar cada página a mano.

## Workflow rápido

Consulta el diagrama principal en el README en inglés:
- [geo-skill workflow](./docs/assets/geo-skill-workflow.png)

## Ejemplos de uso

Auditar un build local:

```bash
geo-skill audit ./public
```

Auditar un sitio en producción y exportar markdown:

```bash
geo-skill audit --url https://example.com --format markdown > geo-audit.md
```

Generar assets iniciales:

```bash
geo-skill generate robots --domain https://example.com
geo-skill generate llms --project "Example" --summary "AI workflow product" --url https://example.com
geo-skill generate schema software-application --name "Example" --url https://example.com --summary "AI workflow product"
```

Comparar before / after GEO reports:

```bash
geo-skill compare before.json after.json --format markdown > geo-diff.md
```

## Benchmark fixtures incluidos

- `weak-marketing-site` — ejemplo de marketing site muy débil en crawl y support coverage
- `docs-strong-site` — ejemplo más fuerte con docs / pricing / changelog mejor resueltos
- `oss-release-site` — ejemplo orientado a open source, releases y docs

Estos benchmarks funcionan tanto dentro del repositorio como después de instalar el paquete.

## Compatibilidad con agentes

### Hermes Agent
- `skills/hermes/<skill-name>/SKILL.md`
- destino típico: `~/.hermes/skills/geo/`

### Claude Code
- `.claude/skills/*.md`
- destino típico: `~/.claude/skills/`

### Codex
- `.agents/skills/<skill-name>/SKILL.md`
- compatible con la convención de skills de Codex

## Licencia

MIT
