# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Company, Founder

admin.site.register([Company, Founder])
