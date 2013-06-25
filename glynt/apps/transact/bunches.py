# coding: utf-8
""" Bunches that prepare and save the pre-validation questions
as well as the transactional info

Bunches DO NOT perform database actions, they ONLY provide the data to be saved
Services is where the magic happens

todos are defined as a tuple of tuples that define the general structure

('todo slug', 'todo name', (
    (Todo, (Validation ruleset)),
    (Todo, (Validation ruleset)),
))

"""
from bunch import Bunch

from glynt.apps.todo.models import ToDo

import logging
logger = logging.getLogger('lawpal.services')


class IncorporationBunch(Bunch):
    """ class defined the names of fields to extract from a transaction data field """
    name = 'Incorporation'
    transaction_slug = 'incorporation'
    todos = (
        ('general', 'General Questions', (
            (ToDo(name='Certificate of Incorporation (DE)'), (),),
            (ToDo(name='Action by Written Consent of Incorporator'), (),),
            (ToDo(name='Initial Written Consent of Board in Lieu of First Meeting'), (),),
            (ToDo(name='Bylaws'), (),),
            (ToDo(name='Shareholders Agreement'), (),),
            (ToDo(name='Form SS-4 application for Employer Identification Number (EIN) from the IRS'), ('if founders > 1'),),
            (ToDo(name='EIN Assignment Letter from the IRS'), (),),
        )),
        ('qualification', 'Qualification to do business in other states or countries', (
            (ToDo(name='Statement and Designation by Foreign Corporation', description='File the Statement and Designation by Foreign Corporation with the California Secretary of State.'), (),),
            (ToDo(name='Form State employer identification number for the Company in California', description='File Form DE-1 (State employer identification number for the Company in California) '), ('if state == CA'),),
            (ToDo(name='Other State EIN'), ('if state != CA'),),
            (ToDo(name='Other Country EIN'), ('if country != US'),),
        )),
        # repeat per number of founders
        ('founders_docs', 'Founders Documents', (
            (ToDo(name='Stock Purchase Agreement for {{ founder_name }}'), (),),
            (ToDo(name='Confidential Information and Invention Assignment Agreement for {{ founder_name }}'), (),),
            (ToDo(name='Notice of Stock Issuance for {{ founder_name }}'), (),),
            (ToDo(name='Stock Certificate(s) for {{ founder_name }}'), (),),
            (ToDo(name='83(b) Election for {{ founder_name }}'), (),),
        )),
        ('option_plan', 'Option Plan', (
            (ToDo(name='Stock Plan'), (),),
            (ToDo(name='Stock Plan Summary'), (),),
            (ToDo(name='Forms of stock option grant and restricted stock purchase agreements under the stock plan'), (),),
            (ToDo(name='Board Approval of Stock Plan'), (),),
            (ToDo(name='Stockholder Approval of Stock Plan'), (),),
        )),
        # repeat for number of option holders
        ('options', 'Option Issuance', (
            (ToDo(name='Stock option grant and restricted stock purchase agreements for {{ name }}'), (),),
            (ToDo(name='Board approval of Option Grant for {{ name }}'), (),),
            (ToDo(name='83(b) Election Form for {{ name }}'), (),),
        )),
        # repeat for num directors and officers
        ('directors_and_officers', 'Directors and Officers', (
            (ToDo(name='Indemnification Agreement for {{ name }}'), (),),
            (ToDo(name='Stockholder Approval of Indemnification Agreement for {{ name }}'), (),),
        )),
        # repeat for num employees
        ('employment_docs', 'Employment Documents', (
            (ToDo(name='Employment Offer Letter for {{ name }}'), (),),
            (ToDo(name='Employment for {{ name }}'), (),),
            (ToDo(name='Confidential Information and Invention Assignment Agreement for {{ name }}', description='Form of Confidential Information and Invention Assignment Agreement for employees'), (),),
            (ToDo(name=' Nondisclosure Agreement for {{ name }}'), (),),
        )),
        ('consultant_docs', 'Consultant Documents', (
            (ToDo(name='Consultant Agreement for {{ name }}'), (),),
            (ToDo(name='Confidential Information and Invention Assignment Agreement for {{ name }}'), (),),
            (ToDo(name='Nondisclosure Agreement for {{ name }}'), (),),
        )),
        ('intellectual_property', 'Intellectual Property', (

        )),
        ('misc', 'Miscellaneous', (
            (ToDo(name='Cap Table'), (),),
            (ToDo(name='Stock Ledger'), (),),
            (ToDo(name='Blue Sky Filings'), (),),
        )),
    )