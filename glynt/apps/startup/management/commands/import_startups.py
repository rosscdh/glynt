# -*- coding: utf-8 -*-
import time
import re
import requests
import urllib
import lxml.html
from django.core.management.base import BaseCommand
from django.core.files import File

from glynt.apps.startup.services import EnsureStartupService

import logging
logger = logging.getLogger('lawpal.commands.import_startups')


class Command(BaseCommand):
    """ Import Startups
    Imports startups from 500 startups (http://500.co/startups)
    and angellist (http://angel.co)
    """

    def handle(self, *args, **options):
        logger.info("Fetching 500startups")
        # startups_500 = self.fetch_500startups()
        # for s in startups_500:
        #     self.create_startup(s)

        logger.info("Fetching angellist")
        startups_angellist = self.fetch_angellist()
        for s in startups_angellist:
            self.create_startup(s)

    # common

    def create_startup(self, data):
        if 'photo_url' in data:
            data['photo'] = self.fetch_image(data['photo_url'])
        service = EnsureStartupService(**data)
        service.process()

    def fetch_image(self, src):
        filename, _ = urllib.urlretrieve(src)
        return File(open(filename))

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
        startups = self.get_angellist_startups_for_tag(1688, limit=1000)
        return startups

    def get_angellist_startups_for_tag(self, tag_id, limit=None):
        def get_page(page):
            logger.info("Fetching page %s for tag %s", page, tag_id)
            r = requests.get('https://api.angel.co/1/tags/%s/startups' % tag_id, params={'page': page})
            return r.json()

        page = 1
        results = []

        logger.info("Fetching %s startups from angellist tag %s", limit if limit else 'all', tag_id)
        while True:
            response = get_page(page)
            for startup in response['startups']:
                if startup.get('hidden') is False:
                    results.append(self.format_angellist_startup(startup))

            if response['page'] >= response['last_page'] or (limit and len(results) >= limit):
                return results[:limit]

            time.sleep(4)  # angellist has a req/hour limit of 1000 or about one per 3.75 sec
            page += 1

    def format_angellist_startup(self, data):
        data['photo_url'] = data.pop('logo_url', None)
        data['summary'] = data.pop('product_desc', None)
        data['website'] = data.pop('company_url', None)
        data['twitter'] = data.pop('twitter_url', None)
        return data

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
        logger.info("Got %s urls from 500startups:", len(urls))
        for url in urls:
            results.append(self.fetch_single_500startup(url))
            time.sleep(1)  # be (a little) nice

        return results

    def fetch_single_500startup(self, url):
        logger.info("Fetching %s", url)
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
            text = text.replace(u'\xc2\xa0', u' ')  # fix some stupid &nbsp; encoding
            if text:
                caption.append(text)
        caption = " ".join(caption)

        twitter = None
        ul_links = sidebar.cssselect('ul.social-links a')
        social_links = []
        for a in ul_links:
            if a.get('class') == 'twitter':
                twitter = a.get('href')
            else:
                social_links.append((a.get('class'), a.get('href')))

        return dict(name=name, website=link, summary=caption, twitter=twitter, photo_url=logo_src, social=social_links)
