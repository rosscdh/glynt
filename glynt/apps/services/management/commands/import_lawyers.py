# -*- coding: utf-8 -*-
import os
from django.db.utils import IntegrityError
from optparse import make_option
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode

from django.contrib.auth.models import User
from glynt.apps.lawyer.services import EnsureLawyerService

import csv


class Command(BaseCommand):
    """ Imports Lawyers from the GDrive LawyerDB spreadsheet
    initially as a dwnloaded csv but eventually directly from gdocs """
    option_list = BaseCommand.option_list + (
        make_option('--local_file',
            action='store_true',
            dest='local_file',
            default='/Users/rossc/Downloads/LawyerDB-Lawyer.csv',
            help='Path to the local csv file'),
        )
    local_file = None

    def handle(self, *args, **options):
        self.local_file = options['local_file']

        if self.local_file and os.path.exists(self.local_file):
            self.import_csv(self.local_file)
        else:
            print("could not find file at: %s" % self.local_file)

    def import_csv(self, csv_file):
        """
        First name, Last name, Firm , Title, Angelist URL, email, City/Location,phone,LinkedIn,Facebook,Twitter,Other start-ups advised
        """
        with open(csv_file, 'rb') as csv_file:
            print("starting csv")
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            csv_file.seek(0)

            for i, r in enumerate(csv.reader(csv_file, dialect)):
                # skip title row
                if i > 0:
                    # get nice names
                    for k,v in enumerate(r):
                        r[k] = smart_unicode(v)

                    username = slugify(u'%s-%s'% (r[0], r[1],))

                    try:
                        user, user_is_new = User.objects.get_or_create(username=username, first_name=r[0], last_name=r[1], email=r[5])
                    except IntegrityError:
                        username = slugify(u'%s-%s%s'% (r[0], r[1], r[5],))
                        user, user_is_new = User.objects.get_or_create(username=username, first_name=r[0], last_name=r[1], email=r[5])
    
                    firm_name = r[2]
                    offices = r[6]

                    lawyer_service = EnsureLawyerService(user=user, firm_name=firm_name, offices=[offices])
                    lawyer_service.process()
