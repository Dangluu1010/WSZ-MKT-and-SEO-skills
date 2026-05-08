#!/usr/bin/env python3
"""
fetch-site-urls.py — Fetch all URLs from a site's sitemap-index.xml.

Saves URLs to:  references/site-urls/{domain}.txt
Config stored:  references/site-urls/config.json

Usage:
  # Register a new site and fetch its URLs
  python3 fetch-site-urls.py https://worksheetzone.org/sitemap-index.xml

  # Force-refresh even if < 7 days old
  python3 fetch-site-urls.py https://worksheetzone.org/sitemap-index.xml --force

  # Auto-refresh all registered sites that are > 7 days old
  python3 fetch-site-urls.py --auto

  # List all registered sites
  python3 fetch-site-urls.py --list

  # Check if any site needs updating (used by blog skills)
  python3 fetch-site-urls.py --check worksheetzone.org
"""

import urllib.request
import xml.etree.ElementTree as ET
import os
import json
import sys
import time
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional, List, Dict

SCRIPT_DIR = Path(__file__).parent
REFERENCES_DIR = SCRIPT_DIR.parent / 'references'
SITE_URLS_DIR = REFERENCES_DIR / 'site-urls'
CONFIG_FILE = SITE_URLS_DIR / 'config.json'
UPDATE_INTERVAL_DAYS = 7
REQUEST_DELAY = 0.3  # seconds between sitemap fetches (polite crawling)


def fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch a URL and return content as string."""
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (blog-skill-url-fetcher/1.0; +auto-internal-linking)'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  ⚠ Failed to fetch {url}: {e}", file=sys.stderr)
        return None


def strip_ns(content: str) -> str:
    """Remove XML namespace declarations for simpler parsing."""
    content = re.sub(r'\s+xmlns(?::\w+)?="[^"]*"', '', content)
    content = re.sub(r'<(\w+):', '<', content)
    content = re.sub(r'</(\w+):', '</', content)
    return content


def parse_locs(content: str) -> list[str]:
    """Extract all <loc> values from sitemap XML."""
    urls = []
    try:
        root = ET.fromstring(strip_ns(content))
        for elem in root.iter('loc'):
            if elem.text and elem.text.strip():
                urls.append(elem.text.strip())
    except ET.ParseError as e:
        # Fallback: regex extraction
        urls = re.findall(r'<loc>\s*(https?://[^\s<]+)\s*</loc>', content)
        if not urls:
            print(f"  ⚠ XML parse error: {e}", file=sys.stderr)
    return urls


def is_sitemap_index(content: str) -> bool:
    """True if the XML contains <sitemapindex> or nested <sitemap> elements."""
    return '<sitemapindex' in content or (
        '<sitemap>' in content and '<urlset' not in content
    )


def fetch_all_urls(sitemap_url: str, depth: int = 0) -> list[str]:
    """Recursively follow sitemap indexes and collect all page URLs."""
    indent = '  ' * depth
    print(f"{indent}→ {sitemap_url}")

    content = fetch_url(sitemap_url)
    if not content:
        return []

    all_urls = []

    if is_sitemap_index(content):
        child_sitemaps = parse_locs(content)
        # Filter to only sitemap URLs (exclude page URLs that might appear in index)
        child_sitemaps = [u for u in child_sitemaps
                         if 'sitemap' in u.lower() or u.endswith('.xml')]
        if not child_sitemaps:
            # No .xml URLs found — all locs are child sitemaps
            child_sitemaps = parse_locs(content)

        print(f"{indent}  📂 {len(child_sitemaps)} child sitemaps")

        for i, child_url in enumerate(child_sitemaps):
            if depth == 0:
                print(f"  [{i+1:3d}/{len(child_sitemaps)}] ", end='', flush=True)
            urls = fetch_all_urls(child_url, depth + 1)
            all_urls.extend(urls)
            if depth == 0:
                print(f"  +{len(urls):,} URLs", end='\n' if (i+1) % 5 == 0 else '')
            if REQUEST_DELAY > 0:
                time.sleep(REQUEST_DELAY)
    else:
        # Regular URL sitemap
        page_urls = parse_locs(content)
        all_urls.extend(page_urls)

    return all_urls


def load_config() -> dict:
    """Load site configuration from config.json."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_config(config: dict) -> None:
    """Persist config.json."""
    SITE_URLS_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False))


def needs_update(domain: str, config: dict, force: bool = False) -> bool:
    """Return True if the URL list for domain is stale or missing."""
    if force:
        return True
    url_file = SITE_URLS_DIR / f'{domain}.txt'
    if not url_file.exists():
        return True
    site_cfg = config.get(domain, {})
    last_updated = site_cfg.get('last_updated')
    if not last_updated:
        return True
    try:
        last_date = datetime.fromisoformat(last_updated)
        return datetime.now() - last_date > timedelta(days=UPDATE_INTERVAL_DAYS)
    except ValueError:
        return True


def run_update(domain: str, sitemap_url: str, config: dict) -> bool:
    """Fetch all URLs from sitemap and write to domain.txt. Returns True on success."""
    url_file = SITE_URLS_DIR / f'{domain}.txt'

    print(f"\n{'='*60}")
    print(f"  Site:    {domain}")
    print(f"  Sitemap: {sitemap_url}")
    print(f"  Output:  {url_file}")
    print(f"{'='*60}\n")

    start = time.time()
    urls = fetch_all_urls(sitemap_url)

    if not urls:
        print(f"\n❌ No URLs found. Check that {sitemap_url} is accessible.")
        return False

    # Deduplicate, strip whitespace, keep only http(s) URLs
    urls = sorted(set(u for u in urls if u.startswith('http')))

    # Write URL list
    SITE_URLS_DIR.mkdir(parents=True, exist_ok=True)
    url_file.write_text('\n'.join(urls) + '\n', encoding='utf-8')

    elapsed = time.time() - start
    print(f"\n\n✅ Done in {elapsed:.1f}s")
    print(f"   {len(urls):,} unique URLs saved to {url_file}")

    # Update config
    config[domain] = {
        'sitemap': sitemap_url,
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'url_count': len(urls),
        'update_interval_days': UPDATE_INTERVAL_DAYS,
    }
    save_config(config)
    return True


def cmd_list(config: dict) -> None:
    """Print all registered sites."""
    if not config:
        print("No sites registered. Run: python3 fetch-site-urls.py <sitemap-url>")
        return
    print(f"{'Domain':<35} {'URLs':>8}  {'Last Updated':<12}  {'Status'}")
    print('-' * 75)
    for domain, cfg in sorted(config.items()):
        url_count = cfg.get('url_count', '?')
        last_updated = cfg.get('last_updated', 'never')
        stale = needs_update(domain, config)
        status = '⚠ NEEDS UPDATE' if stale else '✓ fresh'
        print(f"{domain:<35} {str(url_count):>8}  {last_updated:<12}  {status}")


def cmd_check(domain: str, config: dict) -> None:
    """Exit 0 if up-to-date, exit 1 if needs update (for use in scripts)."""
    if needs_update(domain, config):
        print(f"NEEDS_UPDATE: {domain}")
        sys.exit(1)
    else:
        print(f"UP_TO_DATE: {domain}")
        sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Fetch and maintain site URL lists for internal linking',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('sitemap_url', nargs='?', help='Sitemap index URL to fetch')
    parser.add_argument('--force', action='store_true',
                        help='Force update even if list is < 7 days old')
    parser.add_argument('--auto', action='store_true',
                        help='Auto-refresh all sites older than 7 days')
    parser.add_argument('--list', action='store_true',
                        help='List all registered sites and their status')
    parser.add_argument('--check', metavar='DOMAIN',
                        help='Exit 1 if domain URL list needs updating')
    parser.add_argument('--domain', metavar='DOMAIN',
                        help='Override domain name (auto-detected from URL)')
    args = parser.parse_args()

    SITE_URLS_DIR.mkdir(parents=True, exist_ok=True)
    config = load_config()

    if args.list:
        cmd_list(config)
        return

    if args.check:
        cmd_check(args.check, config)
        return

    if args.auto:
        updated = 0
        for domain, cfg in config.items():
            if needs_update(domain, config, args.force):
                sitemap_url = cfg.get('sitemap')
                if sitemap_url:
                    success = run_update(domain, sitemap_url, config)
                    if success:
                        updated += 1
        if updated == 0:
            print(f"All sites are up to date (< {UPDATE_INTERVAL_DAYS} days). Use --force to refresh.")
        return

    if not args.sitemap_url:
        parser.print_help()
        return

    # Fetch a new or existing site
    parsed = urlparse(args.sitemap_url)
    domain = args.domain or parsed.netloc

    if not domain:
        print(f"Error: could not detect domain from '{args.sitemap_url}'", file=sys.stderr)
        sys.exit(1)

    run_update(domain, args.sitemap_url, config)


if __name__ == '__main__':
    main()
