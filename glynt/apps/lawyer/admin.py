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
    ordering = ['is_active', 'user__last_name', 'user__first_name']
    inlines = [
        FirmInline,
    ]

    def queryset (self, request):
        qs = Lawyer.objects.select_related('user', 'firm_lawyers').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(Lawyer, LawyerAdmin)