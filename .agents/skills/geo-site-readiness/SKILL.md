---
name: geo-site-readiness
description: Use when the task is to assess whether a website is technically ready for GEO before content rewrites or distribution work.
---

# GEO Site Readiness

Audit the technical baseline for GEO: robots, sitemap, llms.txt, metadata, HTML access, FAQ coverage, and structured data.

## When to use

Use when the task is to assess whether a website is technically ready for GEO before content rewrites or distribution work.

- Run the technical baseline before spending time on content strategy.
## Procedure
1. Check robots.txt, sitemap.xml, and llms.txt presence.
2. Confirm indexable entry pages contain title and meta description.
3. Confirm Open Graph basics exist for important pages.
4. Sample HTML pages and look for JSON-LD structured data.
5. Check whether FAQ-like content exists in page copy.
6. Review whether there are distinct URLs for product, feature, docs, pricing, FAQ, changelog, and trust pages.
## CLI hooks
- `geo-skill audit <site-root>`.
- Treat a missing technical baseline as a blocker for GEO claims.
