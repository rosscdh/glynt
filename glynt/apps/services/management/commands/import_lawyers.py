# -*- coding: utf-8 -*-
import os
from django.db.utils import IntegrityError
from optparse import make_option
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode

from django.contrib.auth.models import User
from glynt.apps.lawyer.models import Lawyer
from glynt.apps.firm.models import Firm, Office

import csv
import pdb

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
            print "could not find file at: %s" % self.local_file

    def import_csv(self, csv_file):
        """
        ['Title', 'First name', 'Last name', 'Firm ', 'Title', 'Angelist URL', 'email', 'City/Location', 'phone', 'LinkedIn', 'Facebook', 'Twitter', 'Other start-ups advised']
        """
        with open(csv_file, 'rb') as csv_file:
            print "starting csv"
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            csv_file.seek(0)
            for i,r in enumerate(csv.reader(csv_file, dialect)):
                # skip title row
                if i > 0:
                    # get nice names
                    for k,v in enumerate(r):
                        r[k] = smart_unicode(v)

                    username = slugify(u'%s-%s'% (r[1], r[2],))
                    try:
                        u, user_is_new = User.objects.get_or_create(username=username, first_name=r[1], last_name=r[2], email=r[6])
                    except IntegrityError:
                        username = slugify(u'%s-%s%s'% (r[1], r[2],r[6],))
                        u, user_is_new = User.objects.get_or_create(username=username, first_name=r[1], last_name=r[2], email=r[6])

                    data = {'twitter':r[11], 'angel_list':r[5], 'linkedin':r[9], 'facebook':r[10], 'location':r[7], 'phone':r[8]}
                    role = Lawyer.LAWYER_ROLES.get_value_by_name(r[4].lower())
                    l, lawyer_is_new = Lawyer.objects.get_or_create(user=u, bio=r[len(r)-1], role=role, data=data)
                    print u"lawyer: %s" % l

                    f, firm_is_new = Firm.objects.get_or_create(name=r[3])
                    print u"firm: %s" % f

                    try:
                        f.lawyers.remove(u)
                    except:
                        pass
                    f.lawyers.add(u)
                    print u"joined %s with firm: %s" % (l,f,)

                    try:
                        f.office_set.get(address=r[7])
                    except Office.DoesNotExist,AttributeError:
                        # add office
                        data = {'phone':r[8]}
                        o, office_is_new = Office.objects.get_or_create(firm=f, address=r[7], data=data)
                        print u"added office: %s" % o

