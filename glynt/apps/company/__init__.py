# coding: utf-8
from glynt.apps.utils import get_namedtuple_choices


COMPANY_STATUS_CHOICES = get_namedtuple_choices('COMPANY_STATUS_CHOICES', (
                            (1, 'pre_funding', 'Pre-funding'),
                            (2, 'currently_fund_raising', 'Currently fund raising'),
                            (3, 'have_term_sheet', 'Have term sheet'),
                            (4, 'already_funded', 'Already funded'),
                         ))


OPTION_PLAN_STATUS_CHOICES = get_namedtuple_choices('OPTION_PLAN_STATUS_CHOICES', (
                            (1, 'already_in_place', 'We already have an option plan in place'),
                            (2, 'would_like', 'We would like to implement an option plan'),
                            (3, 'no_plans', 'We do not need an option at this time'),
                         ))
