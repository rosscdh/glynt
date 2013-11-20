# -*- coding: UTF-8 -*-
from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.admin.sites import AdminSite

from model_mommy import mommy

from glynt.casper import PyQueryMixin

from glynt.apps.project.admin import ProjectAdmin
from glynt.apps.project.models import Project
from glynt.apps.project.forms import AdminMatchingEmailCustomContentForm


class ProjectLawyerMatchEmailTest(PyQueryMixin, TestCase):
    def setUp(self):
        super(ProjectLawyerMatchEmailTest, self).setUp()

        client = mommy.prepare('auth.User', username='lawyer_match', email='lawyer_match@lawpal.com', first_name='Bob', last_name='McGee')
        lawyers = [mommy.prepare('lawyer.Lawyer'), mommy.prepare('lawyer.Lawyer')]

        form = AdminMatchingEmailCustomContentForm({'intro': 'Hi there and welcome, here are some lawyers that may match'}) # Custom intro value
        self.assertTrue(form.is_valid())  # must call this to init cleaned_fields on form

        self.subject = ProjectAdmin(Project, AdminSite())
        self.subject.send_matches(request={}, obj={}, client=client, lawyers=lawyers, form=form)

        self.email = mail.outbox[0]

    def test_email_in_outbox(self):
        """
        Test the email that gets sent in the admin
        for Project Lawyer Matches
        """
        self.assertEquals(len(mail.outbox), 1)

    def test_email_values(self):
        self.assertEquals(self.email.bcc, ['founders@lawpal.com'])
        self.assertEquals(self.email.to, ['"Bob McGee" <lawyer_match@lawpal.com>'])
        self.assertEquals(self.email.subject, 'Choose an attorney')

    def test_email_body(self):
        body = self.email.alternatives[0][0]
        context = self.pq(body)

        intro_content = context('#intro_content h2')
        self.assertEquals(intro_content.text(), 'Hi there and welcome, here are some lawyers that may match')

        lawyers = context('table#lawyers tr')
        self.assertEquals(len(lawyers), 2)

        avatars = context('table#lawyers td.avatar-cell img.avatar')
        self.assertEquals(len(avatars), 2)

        for a in avatars:
            self.assertEquals(a.attrib['src'], 'http://example.com/static/img/default_avatar.png')


