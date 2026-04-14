---
name: geo-site-migration-url-stability
description: Use when moving domains, restructuring docs, redesigning the site, or changing URL patterns without losing accumulated GEO signals.
---

# GEO Site Migration and URL Stability

Protect GEO during site migrations with URL inventories, redirects, canonical continuity, sitemap updates, and post-migration validation.

## When to use

Use when moving domains, restructuring docs, redesigning the site, or changing URL patterns without losing accumulated GEO signals.

- A migration can erase accumulated discovery signals if redirects and canonical mappings are sloppy.
## Procedure
1. Inventory the current high-value URLs before changing structure.
2. Map old URLs to the most relevant new URLs with permanent redirects.
3. Keep titles, product facts, and canonical intent stable during the transition.
4. Regenerate sitemap.xml and update any submission workflows after the cutover.
5. Recheck robots.txt, structured data, and trust pages on the new paths.
6. Watch for broken docs, pricing, FAQ, and changelog links after launch.
## CLI hooks
- `geo-skill audit <site-root>` before and after migration to catch missing technical basics.
- Do not launch a new IA or domain without a redirect map for the old answer surfaces.
