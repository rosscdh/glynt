# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger('django.request')


class HelloSignEventView(View):
    template_name='sign/hellosign_event.html'

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        if self.request.method == 'POST':
            return self.post(request=self.request, **kwargs)
        else:
            return self.get(request=self.request, **kwargs)


    def get(self, request, *args, **kwargs):
        logger.info('Recieved GET Event: %s' % request.GET)
        return render_to_response(self.template_name, {})

    def post(self, request, *args, **kwargs):
        logger.info('Recieved POST Event: %s' % request.POST)
        return render_to_response(self.template_name, {})