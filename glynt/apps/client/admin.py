# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import ClientProfile


class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_class',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

    def queryset (self, request):
        qs = ClientProfile.objects.select_related('user').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

# necesary to first unregister as we want our own settings and
# django registers this already as we specify it as the profile 
# model in settings.py
admin.site.unregister(ClientProfile)
admin.site.register(ClientProfile, ClientProfileAdmin)
