#!/usr/bin/env python3
import xml.etree.ElementTree as etree
import requests
import sys
import urllib.parse


XML_URL = 'http://www.billboard.com/rss/charts/hot-100'
ROW_TMPL = """
<tr>
<td>{rank}</td>
<td>{lastrank}</td>
<td><a href="{link}">{title}</a></td>
<td>{artist}</td>
</tr>
"""
PAGE_TMPL = """
<!DOCTYPE html>
<html>
<head>
    <title>Hot 100</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
</head>
<body>
<table class="table table-striped"">
<thead><tr>
    <th>Rank</th>
    <th>Last Rank</th>
    <th>Title</th>
    <th>Artist</th>
</tr></thead>
<tbody>{body}</tbody>
</table>
</body>
</html>
"""
YOUTUBE_SEARCH_URL = 'https://youtube.com/results'


def fetch():
    req = requests.get(XML_URL)
    return etree.fromstring(req.text)


def get(tree):
    for item in tree.findall('.//item'):
        artist = item.findtext('./artist')
        title = item.findtext('./title')
        _, title = title.split(': ', 1)
        url = '{}?{}'.format(
            YOUTUBE_SEARCH_URL,
            urllib.parse.urlencode({
                'q': '{} {}'.format(artist, title).lower(),
            }),
        )

        yield {
            'artist': artist,
            'title': title,
            'rank': int(item.findtext('./rank_this_week')),
            'lastrank': int(item.findtext('./rank_last_week')) or '&mdash;',
            'link': url,
        }


def dump(items):
    body_parts = []
    for item in items:
        body_parts.append(ROW_TMPL.format(**item))
    return PAGE_TMPL.format(body=''.join(body_parts))


if __name__ == '__main__':
    sys.stdout.write(dump(get(fetch())))
