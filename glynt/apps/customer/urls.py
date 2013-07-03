# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from views import CustomerProfileView, CreateCustomerView

urlpatterns = patterns('',
    url(r'^invite/$', login_required(TemplateView.as_view(template_name='customer/invite.html')), name='invite'),
    url(r'^setup/$', login_required(CreateCustomerView.as_view()), name='setup_customer'),
    url(r'^(?P<slug>.+)/$', login_required(CustomerProfileView.as_view()), name='customer_profile'),
)
