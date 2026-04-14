---
name: geo-bing-webmaster-foundation
description: Use when the task is to improve Bing-facing discovery, sitemap submission, or the search-engine foundation that supports OpenAI search visibility.
version: 0.1.0
author: vespid-ai
license: MIT
metadata:
  hermes:
    tags: [geo, generative-engine-optimization, search, cli, agent]
---

# Bing Webmaster GEO Foundation

Strengthen Bing-side discovery with site verification, sitemap submission, URL submission, crawl diagnostics, and IndexNow-aware operational GEO.

## Trigger

Use when the task is to improve Bing-facing discovery, sitemap submission, or the search-engine foundation that supports OpenAI search visibility.

- Treat Bing as a practical submission and diagnostics layer for OpenAI-adjacent GEO work, not as the entire ranking story.
## Procedure
1. Verify the site in Bing Webmaster Tools.
2. Submit sitemap.xml and keep it current.
3. Use URL submission or IndexNow for key new pages when appropriate.
4. Review crawl, indexing, and site-scan diagnostics for blocked or low-quality pages.
5. Make sure canonical URLs, titles, descriptions, and structured data are consistent before submitting.
6. Focus submission effort on product, feature, pricing, docs, FAQ, and changelog pages first.
## CLI hooks
- `geo-skill audit <site-root>` before manual search-engine submission work.
- Do not treat Bing submission as a substitute for fixing weak page quality or crawlability.
