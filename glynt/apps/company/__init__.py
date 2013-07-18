# coding: utf-8
from glynt.apps.utils import get_namedtuple_choices


COMPANY_STATUS_CHOICES = get_namedtuple_choices('COMPANY_STATUS_CHOICES', (
                            (1, 'pre_funding', 'Pre-funding'),
                            (2, 'have_term_sheet', 'Have term sheet'),
                            (3, 'currently_fund_raising', 'Currently fund raising'),
                            (4, 'already_funded', 'Already funded'),
                         ))
