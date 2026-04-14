# doubao-bytespider

Use when the task is about helping a site be easier to discover through ByteDance search surfaces, Bytespider crawling, or practical 豆包 GEO work.

## Goal

Improve ByteDance-side GEO with Bytespider access, sitemap submission, rendered HTML, and Chinese-language product fact pages.

- Treat 豆包 GEO as a real search/crawl problem, not as a mysterious hidden bot interface.
## Procedure
1. Ensure robots.txt allows Bytespider.
2. Ensure WAF/CDN/bot protection does not block Bytespider by UA or IP policy.
3. Publish sitemap.xml with reachable canonical URLs only.
4. Prefer rendered HTML instead of empty client-side shells.
5. Build Chinese-language FAQ and scenario pages that match natural product discovery queries.
6. Include official identity pages: company/about/contact/privacy/terms.
7. When available, use 头条搜索站长平台 to verify the site and submit sitemap.
## CLI hooks
- `geo-skill audit <site-root>` for local readiness checks.
- `geo-skill generate robots --domain https://example.com` for a starter policy that includes Bytespider.
- Do not invent a fake 'DoubaoBot' dependency when public crawler guidance points to Bytespider / 头条搜索 surfaces.
