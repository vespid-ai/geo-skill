---
name: geo-faq-coverage
description: Use when you need to turn real user questions into machine-readable FAQ coverage that maps directly to AI search prompts.
version: 0.1.0
author: vespid-ai
license: MIT
metadata:
  hermes:
    tags: [geo, generative-engine-optimization, search, cli, agent]
---

# GEO FAQ Coverage

Build FAQ pages around real user-language questions so AI systems can answer comparisons, setup, pricing, deployment, privacy, and capability queries.

## Trigger

Use when you need to turn real user questions into machine-readable FAQ coverage that maps directly to AI search prompts.

- FAQ content is one of the cleanest ways to match natural-language prompts.
## Procedure
1. Collect the top repeated sales, support, and onboarding questions.
2. Write each question the way a user would ask it, not in internal taxonomy language.
3. Answer directly in the first sentence, then add detail.
4. Group by product basics, setup, pricing, integrations, privacy, security, and limits.
5. Link each answer to deeper docs or product pages.
6. Consider FAQPage structured data when the content is real and stable.
## CLI hooks
- `geo-skill generate llms --project NAME --summary "FAQ coverage for key user questions" --url https://example.com/faq` for a starting summary block.
- Do not stuff dozens of barely useful keyword variants into one FAQ; prioritize genuine answer quality.
