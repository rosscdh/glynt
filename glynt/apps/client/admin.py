# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import UserSignup, ClientProfile
from userena.models import UserenaSignup, UserenaBaseProfile


# admin.site.unregister([UserenaProfile])
admin.site.register([UserSignup])

