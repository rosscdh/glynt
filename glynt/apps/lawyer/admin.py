# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Lawyer
from glynt.apps.firm.models import Firm


class FirmInline(admin.TabularInline):
    model = Firm.lawyers.through
    extra = 1


class LawyerAdmin(admin.ModelAdmin):
    list_filter = ['role', 'is_active']
    list_display = ('username', 'full_name', 'primary_firm', 'email', 'summary', 'last_login', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'firm_lawyers__name')
    order = ('last_login')
    inlines = [
        FirmInline,
    ]


admin.site.register(Lawyer, LawyerAdmin)