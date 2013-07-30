# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import ToDo, Attachment


admin.site.register([ToDo, Attachment])
