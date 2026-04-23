import requests
import xml.etree.ElementTree as ET
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

RSS_URL = 'https://androphil.tistory.com/rss'
OUTPUT_FILE = 'data.json'


def fetch_rss(url):
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; BlogDashboard/1.0)'}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_date(raw):
    try:
        return parsedate_to_datetime(raw).isoformat()
    except Exception:
        return raw


def strip_html(html):
    text = re.sub(r'<[^>]+>', '', html)
    return re.sub(r'\s+', ' ', text).strip()[:300]


def parse_rss(content):
    root = ET.fromstring(content)
    channel = root.find('channel')

    posts = []
    cat_count = defaultdict(int)
    tag_count = defaultdict(int)
    month_count = defaultdict(int)

    for item in channel.findall('item'):
        title = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        pub_date_raw = (item.findtext('pubDate') or '').strip()
        desc_raw = (item.findtext('description') or '').strip()

        all_cats = [c.text.strip() for c in item.findall('category') if c.text and c.text.strip()]
        main_cat = all_cats[0] if all_cats else '미분류'
        tags = all_cats[1:] if len(all_cats) > 1 else []

        parsed_date = parse_date(pub_date_raw)

        try:
            dt = parsedate_to_datetime(pub_date_raw)
            month_count[dt.strftime('%Y-%m')] += 1
        except Exception:
            pass

        cat_count[main_cat] += 1
        for tag in tags:
            tag_count[tag] += 1

        posts.append({
            'title': title,
            'link': link,
            'pubDate': parsed_date,
            'category': main_cat,
            'tags': tags,
            'excerpt': strip_html(desc_raw),
        })

    return {
        'fetchedAt': datetime.now(timezone.utc).isoformat(),
        'stats': {
            'totalPosts': len(posts),
            'categoryCount': dict(cat_count),
            'tagCount': dict(sorted(tag_count.items(), key=lambda x: -x[1])[:50]),
            'monthlyCount': dict(sorted(month_count.items())),
        },
        'posts': posts,
    }


def main():
    print(f'Fetching {RSS_URL} ...')
    try:
        content = fetch_rss(RSS_URL)
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)

    data = parse_rss(content)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Wrote {OUTPUT_FILE}')
    print(f'  posts: {data["stats"]["totalPosts"]}')
    print(f'  categories: {list(data["stats"]["categoryCount"].keys())}')
    print(f'  unique tags: {len(data["stats"]["tagCount"])}')


if __name__ == '__main__':
    main()
