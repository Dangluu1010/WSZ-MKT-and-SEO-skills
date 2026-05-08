# WSZ Marketing & SEO Skills for Claude Code

59 skills for Claude Code covering Blog, Marketing, SEO, and UI/UX workflows.

## Installation

```bash
git clone https://github.com/Dangluu1010/WSZ-MKT-and-SEO-skills.git
cd WSZ-MKT-and-SEO-skills
./install.sh
```

The installer will:
1. Check/install Node.js and Claude Code
2. Copy all skill files to `~/.claude/skills/`
3. Install Python dependencies for skills that need them (seo, blog-google, blog-audio, blog-notebooklm)

## Skills Included

### Blog (22 skills)
`blog` `blog-analyze` `blog-audio` `blog-audit` `blog-brief` `blog-calendar` `blog-cannibalization` `blog-chart` `blog-factcheck` `blog-geo` `blog-google` `blog-image` `blog-notebooklm` `blog-outline` `blog-persona` `blog-repurpose` `blog-rewrite` `blog-schema` `blog-seo-check` `blog-strategy` `blog-taxonomy` `blog-write`

### Marketing (15 skills)
`market` `market-ads` `market-audit` `market-brand` `market-competitors` `market-copy` `market-emails` `market-funnel` `market-landing` `market-launch` `market-proposal` `market-report` `market-report-pdf` `market-seo` `market-social`

### SEO (20 skills)
`seo` `seo-audit` `seo-backlinks` `seo-competitor-pages` `seo-content` `seo-dataforseo` `seo-firecrawl` `seo-geo` `seo-google` `seo-hreflang` `seo-image-gen` `seo-images` `seo-local` `seo-maps` `seo-page` `seo-plan` `seo-programmatic` `seo-schema` `seo-sitemap` `seo-technical`

### Other (2 skills)
`ui-ux-pro-max` `worksheet-metadata`

## Usage

After installation, start Claude Code and use skills as slash commands:

```
claude
/blog write "Topic here"
/seo audit https://example.com
/market launch "Product name"
/ui-ux-pro-max
```

Type `/` in Claude Code to browse all available skills.

## Uninstall

Remove the installed skills:

```bash
rm -rf ~/.claude/skills
```
