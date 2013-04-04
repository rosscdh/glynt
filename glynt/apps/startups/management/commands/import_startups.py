# -*- coding: utf-8 -*-
import time
import re
from optparse import make_option

import requests
import lxml.html

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Imports startups from 500 startups (http://500.co/startups) and angellist (http://angel.co)
     """
    #option_list = BaseCommand.option_list + (
    #    make_option('--local_file',
    #        action='store_true',
    #        dest='local_file',
    #        default='/Users/rossc/Downloads/LawyerDB-Firms.csv',
    #        help='Path to the local csv file'),
    #    )
    #local_file = None

    def handle(self, *args, **options):
        pass

    # angellist

    def fetch_angellist(self):
        """ Fetches startups from angel.co

        They are pretty explicit about not using their api for scraping,
        so we'll just take a small sample (a couple hundred companies or so)

        Their tags are in a tree-structure starting from
            Market: All Markets (9217)
            Location: Earth (1643)

        If we select startups starting at these points, the assumption is
        that we should hit every company in their database.

        However, for development data, we will concentrate on the
        following tag:
            Location: Earth: North America: United States (1688)
        """
        startups = self.get_angellist_startups_for_tag(1688, limit=100)
        return startups

    def get_angellist_startups_for_tag(self, tag_id, limit=None):
        def get_page(page):
            return requests.get('https://api.angel.co/1/tags/%s/startups' % tag_id, params={'page': page}).json()

        page = 1
        results = []
        while True:
            response = get_page(page)
            results.extend([s for s in response['startups'] if s.get('hidden') is False])

            if response['page'] >= response['last_page'] or (limit and len(results) >= limit):
                return results[:limit]

            time.sleep(4)  # angellist has a req/hour limit of 1000 or about one per 3.75 sec
            page += 1

    # 500startups

    def fetch_500startups(self):
        """ Fetches startups from 500.co/startups.
        """
        # get the list of startup urls
        # normally i would use lxml, but their html is horribly broken
        # not even beautifulsoup can handle it
        r = requests.get('http://500.co/startups/')
        urls = list(set(re.findall(r'http://500\.co/startup-profiles/.+/', r.text)))

        # fetch each indidual startup
        results = []
        for url in reversed(urls):
            results.append(self.fetch_single_500startup(url))
            time.sleep(1)  # be (a little) nice

        return results

    def fetch_single_500startup(self, url):
        doc = lxml.html.parse(url)
        root = doc.getroot()
        sidebar = root.cssselect('div#sidebar')[0]

        logo_src = sidebar.cssselect('img.wp-post-image')[0].get('src')
        name = sidebar.cssselect('span.name')[0].text_content()
        link = sidebar.cssselect('span.byline a')[0].get('href')

        paragraphs = sidebar.cssselect('p')
        caption = []
        for p in paragraphs:
            text = p.text_content().strip()
            if text:
                caption.append(text)
        caption = "".join(caption)

        ul_links = sidebar.cssselect('ul.social-links a')
        social_links = []
        for a in ul_links:
            social_links.append((a.get('class'), a.get('href')))

        return dict(name=name, link=link, text=caption, logo=logo_src, social=social_links)
