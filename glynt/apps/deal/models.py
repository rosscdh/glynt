from django.db import models
from django.contrib.auth.models import User

from glynt.apps.utils import get_namedtuple_choices


class Deal(models.Model):
    """ Base deal structure 
    defines a deal and provides the connection
    between the lawyers responsible for its creation
    the investors providing the investment
    and the recipients
    """
    DEAL_TYPES = get_namedtuple_choices('DEAL_TYPES', (
        (1, 'formation', 'Company Formation and Setup'),
        (2, 'seed', 'Seed Financing'),
        (3, 'series_a', 'Series A'),
    ))
    name = models.CharField(max_length=64)
    summary = models.CharField(max_length=255)
    deal_type = models.IntegerField(choices=DEAL_TYPES.get_choices(), db_index=True)
    volume = models.IntegerField(db_index=True)
    date_finalized = models.DateField(auto_now=False, auto_now_add=False, db_index=True)
    lawyer = models.ManyToManyField(User, related_name='deal_lawyer')
    provider = models.ManyToManyField(User, related_name='deal_provider')
    recipient = models.ManyToManyField(User, related_name='deal_recipient')
