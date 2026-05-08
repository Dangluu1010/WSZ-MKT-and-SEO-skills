# WSZ Marketing & SEO Skills for Claude Code

59 professional skills for Claude Code covering Blog, Marketing, SEO, and UI/UX workflows. Optimized for Google rankings (E-E-A-T, December 2025 Core Update) and AI citations (GEO/AEO for ChatGPT, Perplexity, Google AI Overviews).

## Quick Start

Open a **new terminal window** and run:

```bash
# 1. Clone the repository
git clone https://github.com/Dangluu1010/WSZ-MKT-and-SEO-skills.git

# 2. Enter the directory
cd WSZ-MKT-and-SEO-skills

# 3. Make the installer executable and run it
chmod +x install.sh
./install.sh
```

The installer will:
1. Check/install **Node.js** (via nvm if not found)
2. Check/install **Claude Code** (via npm)
3. Copy all 59 skill folders to `~/.claude/skills/`
4. Set up Python virtual environments and install dependencies for skills that need them (seo, blog-google, blog-audio, blog-notebooklm)
5. Install Playwright browsers for visual analysis (optional)

After installation, start Claude Code:

```bash
claude
```

Type `/` to browse all available skills, or use any slash command directly (e.g., `/blog write "Topic"`, `/seo audit https://example.com`).

## Prerequisites

- **macOS or Linux** (Windows WSL should work but is untested)
- **Git** (to clone the repo)
- **Python 3.10+** (optional, needed for seo/blog-google/blog-audio/blog-notebooklm skills)
- **An Anthropic account** (you'll be prompted to log in when you first run `claude`)

Node.js and Claude Code will be installed automatically if not present.

---

## Skills Reference

### Blog Skills (22)

| Skill | Command | Description |
|---|---|---|
| **blog** | `/blog` | Full-lifecycle blog engine with 21 commands covering writing, rewriting, analyzing, auditing, outlining, and repurposing. Dual-optimized for Google rankings (E-E-A-T) and AI citations (GEO/AEO). Works with any platform (WordPress, Next.js, Hugo, Ghost, etc.). |
| **blog-analyze** | `/blog analyze` | Scores blog posts on a 0-100 scale across 5 categories: content quality, SEO, E-E-A-T, technical elements, and AI citation readiness. Includes AI content detection analysis and prioritized improvement recommendations. |
| **blog-audio** | `/blog audio` | Generates professional audio narration using Google Gemini TTS. Three modes: summary narration, full article read-aloud, or two-speaker podcast dialogue. 30 voice options with HTML5 audio embed output. |
| **blog-audit** | `/blog audit` | Full-site blog health assessment scanning all posts for quality scores, orphan pages, topic cannibalization, stale content, and AI citation readiness. Spawns parallel subagents for comprehensive analysis. |
| **blog-brief** | `/blog brief` | Generates detailed content briefs with target keywords, competitive analysis, statistics recommendations, image/chart suggestions, word count targets, internal linking architecture, and multi-channel distribution plans. |
| **blog-calendar** | `/blog calendar` | Generates editorial calendars with topic clusters, publishing cadence, freshness update schedules, and content decay detection. Optimized for building topical authority and maintaining AI citation freshness. |
| **blog-cannibalization** | `/blog cannibalization` | Detects keyword cannibalization across blog posts by clustering semantically similar targets and flagging posts competing for the same search intent. Supports local-only mode and DataForSEO API mode. |
| **blog-chart** | `/blog chart` | Generates dark-mode-compatible inline SVG charts (bar, donut, line, radar, lollipop, area) with accessible markup and source attribution. Invoked internally by blog-write and blog-rewrite. |
| **blog-factcheck** | `/blog factcheck` | Verifies statistics and claims by fetching cited source URLs and scoring match confidence (exact match, paraphrase, or not found). Flags uncited claims as UNVERIFIED. |
| **blog-geo** | `/blog geo` | AI citation optimization audit scoring posts for ChatGPT, Perplexity, and Google AI Overview citability. Generates citation capsules and a 0-100 AI Citation Readiness score with platform-specific recommendations. |
| **blog-google** | `/blog google` | Google API integration for blog performance: PageSpeed Insights, CrUX Core Web Vitals (25-week history), Search Console, URL Inspection, GA4 organic traffic, NLP entity analysis, YouTube video search, and Keyword Planner. |
| **blog-image** | `/blog image` | AI image generation powered by Gemini via MCP. Generates hero images, inline illustrations, social preview cards, and OG images using optimized 6-component prompts (Subject + Action + Context + Composition + Lighting + Style). |
| **blog-notebooklm** | `/blog notebooklm` | Queries Google NotebookLM notebooks for source-grounded, citation-backed answers from user-uploaded documents with zero hallucination risk. Works standalone or internally from blog-write for Tier 1 research. |
| **blog-outline** | `/blog outline` | SERP-informed outline generation with H2/H3 heading hierarchy, competitive content gap analysis, section word count targets, chart/image placement markers, FAQ question planning, and internal linking zones. |
| **blog-persona** | `/blog persona` | Creates and manages writing personas using the NNGroup 4-dimension tone framework (Funny-Serious, Formal-Casual, Respectful-Irreverent, Enthusiastic-Matter-of-fact). Enforces consistent voice across all blog content. |
| **blog-repurpose** | `/blog repurpose` | Transforms blog posts into platform-optimized content: Twitter/X threads, LinkedIn articles, YouTube scripts, Reddit discussion posts, and email newsletter excerpts. Adapts tone for each platform. |
| **blog-rewrite** | `/blog rewrite` | Rewrites existing blog posts for Google rankings and AI citations. Replaces fabricated statistics with sourced data, adds images/SVG charts, injects FAQ schema, applies answer-first formatting, and performs AI content detection. |
| **blog-schema** | `/blog schema` | Generates complete JSON-LD schema markup: BlogPosting, Person, Organization, BreadcrumbList, FAQPage, and ImageObject using the `@graph` pattern for entity linking. |
| **blog-seo-check** | `/blog seo-check` | Post-writing SEO validation checklist: title tag, meta description, heading hierarchy, internal/external links, canonical URL, Open Graph tags, Twitter Cards, URL structure, and image alt text. |
| **blog-strategy** | `/blog strategy` | Develops blog strategies including topic cluster architecture (hub-and-spoke), audience mapping, competitive landscape analysis, AI citation surface strategy, distribution channel planning, and measurement frameworks. |
| **blog-taxonomy** | `/blog taxonomy` | Extracts, suggests, and syncs tags/categories across CMS platforms (WordPress REST, Shopify GraphQL, Ghost, Strapi, Sanity GROQ). Enforces minimum post-count thresholds to prevent thin tag archives. |
| **blog-write** | `/blog write` | Writes complete new blog articles from scratch. Produces full articles with answer-first formatting, Key Takeaways boxes, sourced statistics, Pixabay/Unsplash images, SVG charts, FAQ schema, and internal linking zones. |

### Marketing Skills (15)

| Skill | Command | Description |
|---|---|---|
| **market** | `/market` | Main orchestrator for the AI Marketing Suite with 14 sub-commands covering audits, copy, emails, social, ads, funnels, competitors, landing pages, launches, proposals, and reports. Routes to appropriate sub-skill. |
| **market-ads** | `/market ads` | Generates complete ad campaigns across Google, Meta, LinkedIn, and more. Includes full copy variations, audience targeting, budget recommendations, and creative specifications from any target URL. |
| **market-audit** | `/market audit` | Full marketing audit launching 5 parallel subagents for simultaneous website analysis. Produces a scored, prioritized, client-ready MARKETING-AUDIT.md report. |
| **market-brand** | `/market brand` | Analyzes brand voice, tone, and messaging across all channels (homepage, about, social, email) and generates comprehensive brand voice guidelines for consistent team usage. |
| **market-competitors** | `/market competitors` | Competitive intelligence analysis identifying direct, indirect, and aspirational competitors. Produces detailed comparison of marketing strategies, positioning gaps, and steal-worthy tactics. |
| **market-copy** | `/market copy` | Analyzes existing website copy, scores it using proven copywriting frameworks, and generates optimized before/after alternatives for every major page section. |
| **market-emails** | `/market emails` | Generates complete, ready-to-send email sequences (welcome, nurture, launch, win-back) with subject lines, body copy, timing, and segmentation strategies calibrated to industry benchmarks. |
| **market-funnel** | `/market funnel` | Maps the complete conversion path from first visit to purchase. Identifies drop-off points, quantifies friction, and recommends optimizations with revenue impact estimates prioritized by lift and effort. |
| **market-landing** | `/market landing` | Comprehensive CRO (Conversion Rate Optimization) analysis with a 7-point framework, section-by-section scoring, and prioritized actionable fixes that directly impact conversion rates. |
| **market-launch** | `/market launch` | Generates a complete week-by-week product/service launch playbook with templates, checklists, email sequences, social posts, and multi-channel coordination. |
| **market-proposal** | `/market proposal` | Generates professional, client-ready marketing services proposals with tiered pricing, ROI projections, and positioning that frames the agency/consultant as the clear choice. |
| **market-report** | `/market report` | Compiles data from all audit and analysis results into a comprehensive Markdown marketing report with scores, findings, and a prioritized action plan with revenue impact estimates. |
| **market-report-pdf** | `/market report-pdf` | Generates a visually polished PDF marketing report with score gauges, bar charts, comparison tables, and branded layout for client presentations. |
| **market-seo** | `/market seo` | SEO audit covering on-page SEO, content quality (E-E-A-T), keyword analysis, technical SEO, and content strategy recommendations. |
| **market-social** | `/market social` | Generates a complete 30-day social media content calendar with platform-specific posts, hooks, and hashtags. Every post is ready to publish or hand to a social media manager. |

### SEO Skills (20)

| Skill | Command | Description |
|---|---|---|
| **seo** | `/seo` | Universal SEO analysis orchestrator covering full site audits, single-page analysis, technical SEO, schema, content quality (E-E-A-T), image optimization, sitemaps, and GEO for AI Overviews. Delegates to 16 sub-skills and 11 subagents. |
| **seo-audit** | `/seo audit` | Full website SEO audit crawling up to 500 pages. Detects business type and delegates to 10 specialist subagents (technical, content, schema, sitemap, performance, local, maps, GEO, Google APIs). Produces an overall health score. |
| **seo-backlinks** | `/seo backlinks` | Backlink profile analysis: referring domains, anchor text distribution, toxic link detection, and competitor gap analysis. Works with free APIs (Common Crawl, Moz, Bing Webmaster) and DataForSEO premium data. |
| **seo-competitor-pages** | `/seo competitor-pages` | Generates SEO-optimized competitor comparison pages ("X vs Y") and "alternatives to X" pages with feature matrices, schema markup, and conversion optimization. |
| **seo-content** | `/seo content` | Content quality and E-E-A-T analysis with AI citation readiness assessment. Checks experience signals, expertise markers, readability, thin content detection, and produces content audit reports. |
| **seo-dataforseo** | `/seo dataforseo` | Live SEO data via the DataForSEO MCP server: SERP analysis, keyword research (volume, difficulty, intent), backlink profiles, on-page analysis, competitor data, AI visibility (ChatGPT/LLM mention tracking), and domain analytics. 79 tools across 9 API modules. |
| **seo-firecrawl** | `/seo firecrawl` | Full-site crawling, scraping, and site mapping via Firecrawl MCP with JavaScript rendering support. Discovers all pages, finds broken links, and maps site structure. |
| **seo-geo** | `/seo geo` | Generative Engine Optimization (GEO) for AI-powered search: Google AI Overviews, ChatGPT web search, and Perplexity. Covers brand mention signals, AI crawler accessibility, llms.txt compliance, and passage-level citability scoring. |
| **seo-google** | `/seo google` | Direct access to Google SEO APIs: Search Console (Search Analytics, URL Inspection, Sitemaps), PageSpeed Insights v5, CrUX field data (25-week history), Indexing API v3, and GA4 organic traffic. Real Chrome user metrics. |
| **seo-hreflang** | `/seo hreflang` | Hreflang and international SEO audit, validation, and generation. Detects common mistakes, validates language/region codes, verifies return tags, and generates correct implementations (HTML, HTTP headers, XML sitemaps). |
| **seo-image-gen** | `/seo image-gen` | AI image generation for SEO assets: OG/social preview images, blog hero images, schema images, product photography, and infographics. Powered by Gemini via the nanobanana MCP extension. |
| **seo-images** | `/seo images` | Image optimization analysis: alt text quality, file sizes, formats (WebP/AVIF), responsive image implementation, lazy loading, and CLS prevention. |
| **seo-local** | `/seo local` | Local SEO analysis: Google Business Profile optimization, NAP consistency, citation health, review signals, local schema, location page quality, and industry-specific recommendations for brick-and-mortar, SAB, and hybrid businesses. |
| **seo-maps** | `/seo maps` | Maps intelligence: geo-grid rank tracking, GBP profile auditing via API, review intelligence (Google/Tripadvisor/Trustpilot), cross-platform NAP verification (Google/Bing/Apple/OSM), and competitor radius mapping. |
| **seo-page** | `/seo page` | Deep single-page SEO analysis: on-page elements (title, meta, headings, links), content quality, technical meta tags, schema markup, image optimization, and performance for any URL. |
| **seo-plan** | `/seo plan` | Strategic SEO planning with industry-specific templates (SaaS, e-commerce, local service, publisher, agency), competitive analysis, content strategy, site architecture, and a prioritized implementation roadmap. |
| **seo-programmatic** | `/seo programmatic` | Programmatic SEO for pages generated at scale from data sources. Covers template engines, URL patterns, internal linking automation, thin content safeguards, and index bloat prevention. |
| **seo-schema** | `/seo schema` | Detects, validates, and generates Schema.org structured data (JSON-LD). Checks required properties per type, validates against Google's rich result requirements, and produces ready-to-implement markup. |
| **seo-sitemap** | `/seo sitemap` | Analyzes XML sitemaps for format validity, URL status, and structural quality. Generates new sitemaps from industry-specific templates with proper format and completeness. |
| **seo-technical** | `/seo technical` | Technical SEO audit across 9 categories: crawlability, indexability, security headers, URL structure, mobile optimization, Core Web Vitals (with INP), structured data, JavaScript rendering, and IndexNow protocol. |

### Other Skills (2)

| Skill | Command | Description |
|---|---|---|
| **ui-ux-pro-max** | `/ui-ux-pro-max` | Comprehensive UI/UX design intelligence with 67 styles, 96 color palettes, 57 font pairings, 25 chart types, and 99 UX guidelines across 13 tech stacks (React, Next.js, Vue, Svelte, Tailwind, shadcn/ui, SwiftUI, Flutter, React Native, etc.). |
| **worksheet-metadata** | `/worksheet-metadata` | Generates publication-ready metadata for educational worksheets: SEO-optimized titles, meta descriptions, URL slugs, tags, categories, and 400-600 word descriptions. Aligned to CCSS, NGSS, and TEKS standards. Built for US teachers and TpT sellers. |

---

## Uninstall

Remove all installed skills:

```bash
rm -rf ~/.claude/skills
```

## Updating

Pull the latest changes and re-run the installer:

```bash
cd WSZ-MKT-and-SEO-skills
git pull
./install.sh
```

This will overwrite existing skill files with the latest versions.

## Troubleshooting

**Skills not showing up after install:**
- Restart Claude Code (`claude` in terminal)
- Check that files exist: `ls ~/.claude/skills/`

**Python dependency errors:**
- Ensure Python 3.10+ is installed: `python3 --version`
- Re-run venv setup manually: `python3 -m venv ~/.claude/skills/seo/.venv && ~/.claude/skills/seo/.venv/bin/pip install -r ~/.claude/skills/seo/requirements.txt`

**Permission denied on install.sh:**
- Run `chmod +x install.sh` first

## License

Internal use only — WSZ team.
