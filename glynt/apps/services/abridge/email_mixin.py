# -*- coding: UTF-8 -*-
from .abridge_service import LawPalAbridgeService

from glynt.apps.default.templatetags.glynt_helpers import current_site_domain

from bunch import Bunch

import waffle

import logging
logger = logging.getLogger('lawpal.services')


class SendEmailAsAbridgeEventMixin(object):
    """
    Mixin used to provide the ability to send emails
    as abridge service events
    """
    abridge_service = None

    def __init__(self, *args, **kwargs):
        # initializers

        self.abridge_service = self.use_abridge(content_group=kwargs.pop('content_group', False))

        if self.from_email is None:
            raise Exception('You must define a self.from_email')

    def use_abridge(self, content_group):
        """
        Use the waffle flag switching system to ensure we can use
        abridge mailout service
        @TODO ugly
        """
        abridge_service = None

        if waffle.switch_is_active('abridge-mailout'):
            logger.info('Waffle abridge-mailout key is Active')

            # Must have content group
            use_abridge = True if content_group is not False else False

            if use_abridge is False:
                logger.info('Abridge Content Group has not been defined')

            else:
                try:
                    abridge_service = LawPalAbridgeService(user=Bunch(email=self.from_email),
                                                                content_group=content_group,
                                                                check_user=False)
                    use_abridge = True

                    logger.info('Created an abridge_service instance content: {content_group}'.format(content_group=content_group))

                except Exception as e:
                    logger.critical('Could not create to the Abridge Service: %s' % e)
                    use_abridge = False

        else:
            logger.info('Waffle abridge-mailout key is Not Active')
            use_abridge = False

        if use_abridge is True and abridge_service is not None:
            return abridge_service
        else:
            return None

    def abridge_profile_photo(self, user):
        """
        send the notification to our abridge service
        """
        try:
            return '{base}{path}'.format(base=current_site_domain(), path=user.profile.get_mugshot_url()) 
        except:
            return None

    def abridge_send(self, context, recipients, template_name=None):
        """
        Try to send the notification via Abridge
        """
        # send the notification to our abridge service
        if self.abridge_service is not None:

            # get teh senders photo
            # @TODO this should be cleaned up and moved higher up in the chain
            profile_photo = self.abridge_profile_photo(user=context.get('actor'))

            # Try to send the event
            try:
                for to_name, to_email in recipients:
                    # add the notification event
                    self.abridge_service.add_event(content=context.get('message'),
                                                   user=Bunch(email=to_email, first_name='', last_name=''),
                                                   url=context.get('url'),
                                                   profile_photo=profile_photo,
                                                   template_name=template_name)

                self.abridge_service.send()
                return True

            except Exception as e:
                logger.critical('Could not send to the Abridge Service: %s' % e)
                return False