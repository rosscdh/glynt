# -*- coding: utf-8 -*-
""" 
Various bunches as they relate to the Graph
"""
from bunch import Bunch


GlyntPerson = Bunch(**{
                'glynt_user_id': None,
                'provider_id': None,
                'full_name': None,
                'provider': 'linkedin',
            })
