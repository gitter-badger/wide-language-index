#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fetch_sbs.py
#  languagegame
#

"""
Add recent podcasts from SBS Australia to the index.
"""

import os
import sys
import optparse
import time
import datetime

from pyquery import PyQuery
import requests
import yaml
import parse
import parsedatetime.parsedatetime as pdt
from bson import ObjectId
from datetime_tz import datetime_tz

from .core import Sample

DEST_DIR = 'data/split.pending'


def fetch_sbs(url, language=None):
    if not language:
        p = parse.Parser(
            'http://www.sbs.com.au/yourlanguage/{}/highlight/page/id/{}'
        )
        language = p.parse(url).fixed[0].title()

    if '/chinese/' in url:
        title, href, date = _scrape_metadata_chinese(url)
    else:
        title, href, date = _scrape_metadata(url)

    base = os.path.join('/tmp', str(ObjectId()))
    sound_file = base + '.mp3'
    metadata_file = base + '.yaml'

    sound = get(href)
    with open(sound_file, 'w') as ostream:
        ostream.write(sound)

    rec = {
        'language': language,
        'title': title,
        'source_name': 'SBS %s' % language,
        'location': 'Australia',
        'source_url': url,
        'date': str(date),
    }
    with open(metadata_file, 'w') as ostream:
        yaml.safe_dump(rec, ostream, default_flow_style=False,
                       explicit_start=True)

    s = Sample(sound_file)
    s.normalize_volume()
    s.move(DEST_DIR)

    os.system('cat %s' % s.meta)


def get(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise IOError('url failed with status %s' % r.status_code)

    return r.content


def _scrape_metadata(url):
    page = PyQuery(get(url))
    title = page('h1.page_title').text()
    href = [a for a in page('div.fl > a') if 'To download' in
            a.attrib['title']][0].attrib['href']
    cal = pdt.Calendar()
    date_text = page('div.date').text().split(' By')[0]
    d = datetime.date.fromtimestamp(time.mktime(cal.parseDateText(date_text)))
    return title, href, d


def _scrape_metadata_chinese(url):
    page = PyQuery(get(url))
    title = page('h1').text()
    href, = ['http://www.sbs.com.au' + a.attrib['href']
             for a in list(page('a'))
             if 'title' in a.attrib and 'To download' in a.attrib['title']]
    p = parse.Parser('{}, {:d} {} {:d}.')
    date_s = ' '.join(map(str, p.parse(page('span.c_bar').text()).fixed[1:]))
    date = datetime_tz.smartparse(date_s).date()

    return title, href, date


def _create_option_parser():
    usage = \
"""%prog [options] url

Fetch audio from the given url."""  # nopep8

    parser = optparse.OptionParser(usage)
    parser.add_option('-l', action='store', dest='language')

    return parser


def main():
    argv = sys.argv[1:]
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    fetch_sbs(*args, language=options.language)


if __name__ == '__main__':
    main()
