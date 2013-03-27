# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Firm, Office


admin.site.register([Firm, Office])
