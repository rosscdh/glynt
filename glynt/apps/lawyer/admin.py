# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Lawyer
from glynt.apps.firm.models import Firm
from django.contrib.auth.models import User


class FirmInline(admin.TabularInline):
    model = Firm.lawyers.through
    extra = 1


class LawyerAdmin(admin.ModelAdmin):
    list_filter = ['role']
    list_display = ('username', 'full_name', 'firm_name', 'email', 'summary', 'last_login')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__firm_lawyers__name')
    order = ('last_login')
    inlines = [
        FirmInline,
    ]

admin.site.register(Lawyer,LawyerAdmin)