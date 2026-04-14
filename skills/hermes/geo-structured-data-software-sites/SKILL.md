---
name: geo-structured-data-software-sites
description: Use when the site needs stronger machine-readable semantics for software, product, organization, FAQ, breadcrumb, and article pages.
version: 0.1.0
author: vespid-ai
license: MIT
metadata:
  hermes:
    tags: [geo, generative-engine-optimization, search, cli, agent]
---

# GEO Structured Data for Software Sites

Use structured data deliberately on software and product sites so search systems can parse entities, offers, FAQs, and content relationships more reliably.

## Trigger

Use when the site needs stronger machine-readable semantics for software, product, organization, FAQ, breadcrumb, and article pages.

- Structured data helps with machine readability, but only when it reflects real page content.
## Procedure
1. Start with Organization and WebSite on top-level identity pages.
2. Use Product or SoftwareApplication on core product pages when the content supports it.
3. Use FAQPage only for actual question-and-answer sections.
4. Add BreadcrumbList where site hierarchy matters.
5. Keep schema fields aligned with visible page content and canonical URLs.
6. Avoid fake review or rating data.
## CLI hooks
- `geo-skill audit <site-root>` to catch whether any JSON-LD is present before improving quality.
- Do not treat schema markup as a substitute for weak content or absent pages.
