---
name: geo-site-readiness
description: Use when the task is to assess whether a website is technically ready for GEO before content rewrites or distribution work.
version: 0.1.0
author: vespid-ai
license: MIT
metadata:
  hermes:
    tags: [geo, generative-engine-optimization, search, cli, agent]
---

# GEO Site Readiness

Audit the technical baseline for GEO: robots, sitemap, llms.txt, metadata, HTML access, FAQ coverage, and structured data.

## Trigger

Use when the task is to assess whether a website is technically ready for GEO before content rewrites or distribution work.

- Run the technical baseline before spending time on content strategy.
## Procedure
1. Check robots.txt, sitemap.xml, and llms.txt presence.
2. Confirm index.html or equivalent entry pages contain title and meta description.
3. Confirm Open Graph basics exist for key pages.
4. Sample HTML pages and look for JSON-LD structured data.
5. Check whether FAQ-like content exists in page copy.
6. Review whether there are distinct URLs for product, feature, docs, pricing, FAQ, changelog, and trust pages.
## CLI hooks
- `geo-skill audit <site-root>`
- Treat a missing technical baseline as a blocker for GEO claims.
