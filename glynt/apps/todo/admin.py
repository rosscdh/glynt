# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import ToDo, Attachment, FeedbackRequest


class ToDoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    search_fields = ('name', 'category', 'slug')

    def queryset(self, request):
        qs = ToDo.objects.prefetch_related('project').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'project', 'filename', 'mimetype', 'date_created')
    search_fields = ('uuid',)

    def queryset(self, request):
        qs = Attachment.objects.prefetch_related('project').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(ToDo, ToDoAdmin)
admin.site.register(Attachment, AttachmentAdmin)

admin.site.register([FeedbackRequest])
