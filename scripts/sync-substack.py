#!/usr/bin/env python3
"""Sync new Substack posts into index.html's writing section."""

import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

FEED_URL   = 'https://adibhalla.substack.com/feed'
INDEX_FILE = 'index.html'


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'sync-substack/1.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8')


def esc(text):
    return (text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;'))


def parse_posts(xml_str):
    root = ET.fromstring(xml_str)
    posts = []
    for item in root.findall('.//item'):
        title    = item.findtext('title', '').strip()
        subtitle = item.findtext('description', '').strip()
        link     = (item.findtext('link', '').strip()
                    or item.findtext('guid', '').strip())
        pub_raw  = item.findtext('pubDate', '').strip()
        try:
            pub_dt   = datetime.strptime(pub_raw, '%a, %d %b %Y %H:%M:%S %Z')
            date_str = pub_dt.strftime('%B %Y')  # e.g. "May 2026"
        except ValueError:
            date_str = ''
        if title and link:
            posts.append({
                'title':    title,
                'subtitle': subtitle,
                'link':     link,
                'date':     date_str,
            })
    return posts


def existing_urls(html):
    return set(re.findall(r'class="writing-title"\s+href="([^"]+)"', html))


def make_item(post):
    return (
        '\n\n'
        '                <div class="writing-item">\n'
        f'                    <a class="writing-title" href="{esc(post["link"])}" target="_blank">{esc(post["title"])} ↗</a>\n'
        f'                    <div class="writing-meta"><span class="writing-date">{esc(post["date"])}</span></div>\n'
        f'                    <p class="writing-blurb">{esc(post["subtitle"])}</p>\n'
        '                </div>'
    )


def main():
    with open(INDEX_FILE, encoding='utf-8') as f:
        html = f.read()

    posts     = parse_posts(fetch(FEED_URL))
    seen      = existing_urls(html)
    new_posts = [p for p in posts if p['link'] not in seen]

    if not new_posts:
        print('No new posts found.')
        return

    for p in new_posts:
        print(f'Adding: {p["title"]}')

    marker = '<div class="writing-list">'
    pos    = html.find(marker)
    if pos == -1:
        print('ERROR: writing-list div not found in index.html', file=sys.stderr)
        sys.exit(1)

    insert_at = pos + len(marker)
    new_html  = ''.join(make_item(p) for p in new_posts)
    updated   = html[:insert_at] + new_html + html[insert_at:]

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(updated)

    print(f'Done — added {len(new_posts)} post(s).')


if __name__ == '__main__':
    main()
