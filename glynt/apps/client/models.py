from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.dispatch import receiver

from socialregistration.signals import connect

from userena.models import UserenaBaseProfile


# @TODO Hook the usercreated signal from socialregistration up to create one of these profiles on signup
class ClientProfile(UserenaBaseProfile):
    """ Base User Profile, where we store all the interesting information about users """
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    # company = models.CharField(_('Company'), max_length=5)
    # position = models.CharField(_('Position'), max_length=5)


@receiver(connect)
def create_client_profile(sender, **kwargs):
    user = kwargs['user']
    profile, is_new = ClientProfile.objects.get_or_create(user=user)