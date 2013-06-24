# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import redirect

from glynt.apps.engage.models import Engagement
from glynt.apps.startup.models import Founder

import logging
logger = logging.getLogger('django.request')


class FounderDashboardView(TemplateView):
    template_name='dashboard/overview.html'

    def dispatch(self, request, *args, **kwargs):
        founder = Founder.objects.get(user=request.user.id)
        engagements = Engagement.objects.filter(founder=founder)
        if not engagements:
            return redirect('transact:packages')

        return super(FounderDashboardView, self).dispatch(request, *args, **kwargs)