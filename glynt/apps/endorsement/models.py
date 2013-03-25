from django.db import models
from django.contrib.auth.models import User

from glynt.apps.utils import get_namedtuple_choices


class LawyerEndorsement(models.Model):
    """ Endorsement model
    Provides a means to allow users to endorse
    a Lawyer
    """
    summary = models.CharField(max_length=255)
    lawyer = models.ManyToManyField(User, related_name='lawyerendorsement_lawyer')
    endorser = models.ManyToManyField(User, related_name='lawyerendorsement_endorser')
    date_created = models.DateField(auto_now=False, auto_now_add=True, db_index=True)
    date_modified = models.DateField(auto_now=True, auto_now_add=True, db_index=True)


class InvestorEndorsement(models.Model):
    """ Endorsement model
    Provides a means to allow users to endorse
    an Investor
    """
    summary = models.CharField(max_length=255)
    investor = models.ManyToManyField(User, related_name='investorendorsement_lawyer')
    endorser = models.ManyToManyField(User, related_name='investorendorsement_endorser')
    date_created = models.DateField(auto_now=False, auto_now_add=True, db_index=True)
    date_modified = models.DateField(auto_now=True, auto_now_add=True, db_index=True)
