# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import View, DetailView

from braces.views import JSONResponseMixin

from .models import Signature
from .services import HelloSignWebhookService

import logging
logger = logging.getLogger('django.request')


class HelloSignSignatureView(DetailView):
    """
    View to show the signature view for a document
    """
    model = Signature

    def get_context_data(self, **kwargs):
        context = super(HelloSignSignatureView, self).get_context_data(**kwargs)
        context.update({
            'HELLOSIGN_CLIENT_ID': getattr(settings, 'HELLOSIGN_CLIENT_ID'),
            'SIGNATURE_URL': self.object.signing_url,
            'DETAILS_URL': self.object.details_url,
        })
        return context

class HelloSignEventView(JSONResponseMixin, View):
    template_name='hellosign/hellosign_event.html'
    json_dumps_kwargs = {'indent': 3}

    def get(self, request, *args, **kwargs):
        logger.info('Recieved GET Event: %s' % request.GET)

        context_dict = {
            'message': 'Please POST to this endpoint',
        }
        return self.render_json_response(context_dict)

    def post(self, request, *args, **kwargs):
        body = request.POST.get('json')

        logger.debug('Recieved POST Event from HelloSign: %s' % body)

        service = HelloSignWebhookService(payload=body)
        service.process()

        context_dict = {
            'message': 'POST recieved',
        }
        return self.render_json_response(context_dict)