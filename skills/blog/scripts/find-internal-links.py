#!/usr/bin/env python3
"""
find-internal-links.py — Find internal link candidates from a site's URL list.

Searches {domain}.txt by keyword relevance and outputs a ## Link Candidates block
that the blog skill can use directly for link injection.

Usage:
  python3 find-internal-links.py worksheetzone.org "3rd grade math" "multiplication"
  python3 find-internal-links.py worksheetzone.org "handwriting" --type blog --top 15
  python3 find-internal-links.py worksheetzone.org "coloring pages" --type coloring-pages

Options:
  --top N       Return top N results (default: 20)
  --type TYPE   Filter by URL section: blog, coloring-pages, worksheets, or all (default: all)
  --min-score N Minimum keyword match score (default: 1)
  --json        Output as JSON instead of markdown table
"""

import sys
import re
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse
from typing import List, Dict, Tuple, Optional

SCRIPT_DIR = Path(__file__).parent
SITE_URLS_DIR = SCRIPT_DIR.parent / 'references' / 'site-urls'

# Grade level synonyms — helps match "grade 3" to "3rd" etc.
GRADE_SYNONYMS: Dict[str, List[str]] = {
    'prek': ['pre-k', 'preschool', 'kindergarten'],
    'k': ['kindergarten', 'kinder'],
    '1st': ['first', '1st', 'grade-1'],
    '2nd': ['second', '2nd', 'grade-2'],
    '3rd': ['third', '3rd', 'grade-3'],
    '4th': ['fourth', '4th', 'grade-4'],
    '5th': ['fifth', '5th', 'grade-5'],
    '6th': ['sixth', '6th', 'grade-6'],
    '7th': ['seventh', '7th', 'grade-7'],
    '8th': ['eighth', '8th', 'grade-8'],
}


def classify_url(url: str) -> str:
    """Return the top-level section of a URL path."""
    try:
        path = urlparse(url).path.lstrip('/')
        parts = path.split('/')
        return parts[0] if parts else 'root'
    except Exception:
        return 'unknown'


def url_to_tokens(url: str) -> set:
    """Break a URL into searchable tokens (words from path segments)."""
    path = urlparse(url).path.lower()
    tokens = set(re.findall(r'[a-z0-9]+', path))
    return tokens


def keyword_to_tokens(keyword: str) -> list[str]:
    """Normalize a keyword into search tokens, expanding grade synonyms."""
    tokens = re.findall(r'[a-z0-9]+', keyword.lower())
    expanded = list(tokens)
    for token in tokens:
        synonyms = GRADE_SYNONYMS.get(token, [])
        for syn in synonyms:
            expanded.extend(re.findall(r'[a-z0-9]+', syn.lower()))
    return list(set(expanded))


def score_url(url: str, keyword_token_groups: list[list[str]]) -> tuple[int, list[str]]:
    """
    Score a URL against keyword groups.
    Each keyword group represents one search term (possibly multi-word).
    Returns (score, list_of_matched_keywords).
    """
    url_tokens = url_to_tokens(url)
    score = 0
    matched = []

    for group_tokens in keyword_token_groups:
        # Count how many tokens from this keyword are present in the URL
        hits = sum(1 for t in group_tokens if t in url_tokens)
        if hits > 0:
            score += hits
            # Reconstruct the keyword string for reporting
            matched.append('-'.join(group_tokens[:2]))  # abbreviated

    return score, matched


def anchor_hint(url: str) -> str:
    """Suggest an appropriate anchor text style based on URL section."""
    section = classify_url(url)
    hints = {
        'blog': 'informational (tips, guide, ideas, activities, how to)',
        'coloring-pages': 'visual (coloring pages, printable, coloring sheets)',
        'worksheets': 'resource (worksheets, printables, practice sheets)',
        'lesson-plans': 'curriculum (lesson plans, teaching resources)',
    }
    return hints.get(section, 'descriptive')


def find_candidates(
    domain: str,
    keywords: list[str],
    url_type: str = 'all',
    top: int = 20,
    min_score: int = 1,
) -> list[dict]:
    """Return scored URL candidates from {domain}.txt matching the keywords."""
    url_file = SITE_URLS_DIR / f'{domain}.txt'

    if not url_file.exists():
        print(f"Error: URL list not found: {url_file}", file=sys.stderr)
        print(f"Run: python3 fetch-site-urls.py <sitemap-url> to generate it", file=sys.stderr)
        sys.exit(1)

    all_urls = [u.strip() for u in url_file.read_text(encoding='utf-8').splitlines() if u.strip()]

    # Filter by URL section type
    if url_type != 'all':
        all_urls = [u for u in all_urls if f'/{url_type}/' in u or
                    urlparse(u).path.lstrip('/').startswith(url_type)]

    # Tokenize each keyword
    keyword_groups = [keyword_to_tokens(kw) for kw in keywords]

    results = []
    for url in all_urls:
        score, matched = score_url(url, keyword_groups)
        if score >= min_score:
            slug = urlparse(url).path.rstrip('/').split('/')[-1]
            results.append({
                'score': score,
                'url': url,
                'type': classify_url(url),
                'slug': slug,
                'matched': matched,
                'anchor_hint': anchor_hint(url),
            })

    # Sort: highest score first, then alphabetically by slug for ties
    results.sort(key=lambda x: (-x['score'], x['slug']))
    return results[:top]


def output_markdown(
    domain: str,
    keywords: list[str],
    results: list[dict],
    total_searched: int,
) -> None:
    """Print results as a ## Link Candidates markdown block."""
    print(f"## Link Candidates")
    print(f"")
    print(f"Site: {domain} | Keywords: {', '.join(keywords)} | "
          f"Searched: {total_searched:,} URLs | Found: {len(results)}")
    print(f"")

    if not results:
        print("_No matching URLs found. Try broader keywords._")
        return

    print("| Score | Type | Slug | Anchor Style | URL |")
    print("|------:|------|------|--------------|-----|")
    for r in results:
        print(f"| {r['score']} | {r['type']} | `{r['slug']}` | "
              f"{r['anchor_hint']} | {r['url']} |")


def output_json(results: list[dict]) -> None:
    """Print results as JSON."""
    print(json.dumps(results, indent=2, ensure_ascii=False))


def count_urls(domain: str) -> int:
    """Count URLs in domain.txt."""
    url_file = SITE_URLS_DIR / f'{domain}.txt'
    if not url_file.exists():
        return 0
    return sum(1 for line in url_file.read_text(encoding='utf-8').splitlines() if line.strip())


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Find internal link candidates from a site URL list',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('domain', help='Site domain (e.g. worksheetzone.org)')
    parser.add_argument('keywords', nargs='+', help='Keywords to match against URLs')
    parser.add_argument('--top', type=int, default=20,
                        help='Return top N results (default: 20)')
    parser.add_argument('--type', default='all', dest='url_type',
                        help='Filter by section: blog, coloring-pages, worksheets, or all')
    parser.add_argument('--min-score', type=int, default=1,
                        help='Minimum keyword match score (default: 1)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON instead of markdown')
    args = parser.parse_args()

    total_searched = count_urls(args.domain)
    results = find_candidates(
        domain=args.domain,
        keywords=args.keywords,
        url_type=args.url_type,
        top=args.top,
        min_score=args.min_score,
    )

    if args.json:
        output_json(results)
    else:
        output_markdown(args.domain, args.keywords, results, total_searched)


if __name__ == '__main__':
    main()
