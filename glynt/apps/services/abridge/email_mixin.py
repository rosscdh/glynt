# -*- coding: UTF-8 -*-
from .abridge_service import LawPalAbridgeService

from glynt.apps.default.templatetags.glynt_helpers import current_site_domain

from bunch import Bunch


class SendEmailAsAbridgeEventMixin(object):
    """
    Mixin used to provide the ability to send emails
    as abridge service events
    """
    abridge_service = None

    def __init__(self, *args, **kwargs):
        # initializers
        self.abridge_content_group = kwargs.pop('content_group', False)
        self.use_abridge = True if self.abridge_content_group is not False else False

        if self.use_abridge is True:
            self.abridge_service = LawPalAbridgeService(user=Bunch(email=self.from_email),
                                                        content_group=self.abridge_content_group,
                                                        check_user=False)

    def abridge_send(self, context, recipients):
        """
        Try to send the notification via Abridge
        """
        # send the notification to our abridge service
        if self.use_abridge is True:
            # send the notification to our abridge service
            try:
                profile_photo = '{base}{path}'.format(base=current_site_domain(), path=context.get('actor').profile.get_mugshot_url()) 
            except:
                profile_photo = None

            # try:

            for to_name, to_email in recipients:
                # add the notification event

                self.abridge_service.add_event(content=context.get('message'),
                                               user=Bunch(email=to_email, first_name='', last_name=''),
                                               url=context.get('url'),
                                               profile_photo=profile_photo)

            self.abridge_service.send()
            return True

            # except Exception as e:
            #     logger.critical('Could not send to the Abridge Service: %s' % e)
            #     return False