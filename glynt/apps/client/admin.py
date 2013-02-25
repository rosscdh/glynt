# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import UserSignup


# admin.site.unregister([UserenaProfile])
admin.site.register([UserSignup])

