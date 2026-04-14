---
name: geo-feature-pages
description: Use when a product has multiple capabilities but they are collapsed into one page, making it hard for search systems to quote and compare specific features.
---

# GEO Feature Pages

Create dedicated feature pages that isolate capabilities, use cases, and evidence so AI systems can cite the right page for the right question.

## When to use

Use when a product has multiple capabilities but they are collapsed into one page, making it hard for search systems to quote and compare specific features.

- Feature pages improve precision: one capability, one page, one clear answer surface.
## Procedure
1. Split major capabilities into distinct URLs.
2. Give each page a clear title, summary, inputs, outputs, and user value.
3. Add links to pricing, docs, API references, and related feature pages.
4. Include constraints, deployment notes, or supported integrations when relevant.
5. Use screenshots as support, not as the only carrier of product facts.
## CLI hooks
- `geo-skill generate llms --project NAME --summary "Feature page summary" --url https://example.com/feature` as a drafting aid.
- Avoid giant all-in-one pages where every feature competes for the same keywords and answer intents.
