# -*- coding: utf-8 -*-
import os
from django.utils.encoding import smart_unicode
from django.template.loader import render_to_string


class SignaturePageService(object):
    """ Service used to generate a signature page 
    html file """
    template = 'export/signature_page.html'
    def __init__(self, document):
        self.document = document

    def get_objects(self):
        signatures = []
        for sig in self.document.documentsignature_set.select_related('user'):
            s = {
                'signature_url': sig.signature_pic_url
                ,'has_signed': sig.is_signed
                ,'name': sig.signee_name
                ,'email': sig.signee_email
                ,'date_signed': sig.date_signed
                ,'date_invited': sig.date_invited
                ,'ip_address': sig.signee_ip_address
            }
            signatures.append(s)
        return signatures

    def get_context(self):
        return {
            'object_list': self.get_objects()
        }

    def render(self):
        render_to_string(self.template, context)
        