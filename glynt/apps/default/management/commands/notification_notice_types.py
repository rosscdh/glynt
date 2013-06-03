# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import signals
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_noop as _


from notification import models as notification


def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.NoticeType.create("engagement_request_new", _("New Engagement Request"), _("a new engagement request has been created"))
    notification.NoticeType.create("engagement_request_update", _("Update to an Engagement Request"), _("an update to your engagement request"))


class Command(BaseCommand):
    help = 'Create Glynt Notice Types'

    def handle(self, *args, **options):
        create_notice_types(app='engage', created_models=[], verbosity=1)

signals.post_syncdb.connect(create_notice_types, sender=notification)