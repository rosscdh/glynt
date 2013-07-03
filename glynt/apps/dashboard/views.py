# -*- coding: utf-8 -*-
from django.views.generic import TemplateView


class CustomerDashboardView(TemplateView):
    template_name='dashboard/overview.html'