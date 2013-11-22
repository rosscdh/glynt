# -*- coding: UTF-8 -*-
from django.contrib import admin

from .models import Signature


class SignatureAdmin(admin.ModelAdmin):
    list_display = ('requested_by', 'document', 'signature_request_id', 'is_complete', 'is_deleted')
    search_fields = ('signature_request_id',)

    def queryset(self, request):
        qs = Signature.objects.prefetch_related('requested_by', 'document').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


admin.site.register(Signature, SignatureAdmin)
