---
name: geo-content-modeling
description: Use when the task is to rewrite or structure pages so AI systems can understand, quote, and compare the product correctly.
version: 0.1.0
author: vespid-ai
license: MIT
metadata:
  hermes:
    tags: [geo, generative-engine-optimization, search, cli, agent]
---

# GEO Content Modeling

Model product facts for GEO so AI systems can quote what the product is, who it is for, what it does, and how it is priced or deployed.

## Trigger

Use when the task is to rewrite or structure pages so AI systems can understand, quote, and compare the product correctly.

- Optimize for quotable product facts, not vague slogans.
## Procedure
1. Put a one-sentence product definition near the top of each important page.
2. Answer who the product is for and what problem it solves.
3. Make capabilities, pricing, deployment, and availability explicit.
4. Use natural-language FAQ sections aligned with likely search prompts.
5. Publish changelog or dated updates for freshness signals.
6. Avoid hiding critical facts inside images, videos, or interactive widgets only.
## CLI hooks
- `geo-skill generate llms --project NAME --summary "..." --url https://example.com` for a starting llms.txt-style summary.
- Aim for pages that can be cited cleanly by search agents and coding agents alike.
