# -*- coding: utf-8 -*-
from django.views.generic import View
from braces.views import JSONResponseMixin

from .services import HelloSignWebhookService

import logging
logger = logging.getLogger('django.request')


class HelloSignEventView(JSONResponseMixin, View):
    template_name='sign/hellosign_event.html'
    json_dumps_kwargs = {'indent': 3}

    def get(self, request, *args, **kwargs):
        logger.info('Recieved GET Event: %s' % request.GET)

        context_dict = {
            'message': 'Please POST to this endpoint',
        }
        return self.render_json_response(context_dict)

    def post(self, request, *args, **kwargs):
        logger.info('Recieved POST Event: %s' % request.POST)
        context_dict = {
            'message': 'POST recieved',
        }
        return self.render_json_response(context_dict)