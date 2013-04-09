# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Startup, Founder

admin.site.register([Startup, Founder])
