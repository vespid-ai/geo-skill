---
name: openai-chatgpt-search
description: Use when the task is about improving discoverability in ChatGPT Search, separating search visibility from training permission, or fixing OAI-SearchBot / GPTBot / Bing-facing GEO issues.
---

# OpenAI / ChatGPT Search GEO

Improve ChatGPT Search visibility with OAI-SearchBot, Bing-facing indexing, sitemap hygiene, and machine-readable product pages.

## When to use

Use when the task is about improving discoverability in ChatGPT Search, separating search visibility from training permission, or fixing OAI-SearchBot / GPTBot / Bing-facing GEO issues.

- Keep search and training separate: OAI-SearchBot is the search surface, GPTBot is the training surface, and ChatGPT-User is user-triggered access rather than automatic discovery.
## Procedure
1. Confirm robots.txt explicitly allows OAI-SearchBot.
2. Decide whether GPTBot should be allowed or blocked for training.
3. Ensure sitemap.xml exists, is reachable, and contains canonical URLs only.
4. Make sure key product/docs/faq/pricing pages return 200 without login walls or bot challenges.
5. Improve Bing-side discoverability because ChatGPT Search uses third-party search providers and Bing is explicitly referenced in OpenAI help documentation.
6. Add structured data where useful and make product facts explicit in HTML.
7. Verify changelog / freshness pages exist for frequently changing products.
## CLI hooks
- `geo-skill audit <site-root>` to check technical readiness.
- `geo-skill generate robots --domain https://example.com` for a starter robots.txt policy.
- Do not claim that allowing GPTBot is sufficient for ChatGPT Search visibility.
