# -*- coding: utf-8 -*-
import os
import time
import re
from optparse import make_option

import requests
import lxml.html

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode


RE_500URL= re.compile(r'http://500\.co/startup-profiles/.+/')


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
        print self.fetch_500startups()

    def fetch_500startups(self):
        """ Fetches startups from 500.co/startups.
        """
        # get the list of startup urls
        # normally i would use lxml, but their html is horribly broken
        # not even beautifulsoup can handle it
        r = requests.get('http://500.co/startups/')
        urls = list(set(RE_500URL.findall(r.text)))

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
