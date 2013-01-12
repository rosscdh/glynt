# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import gettext as _
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from categories.admin import CategoryBaseAdmin
from glynt.apps.flyform.models import FlyForm
from glynt.apps.document.models import DocumentTemplate, DocumentTemplateCategory, ClientCreatedDocument


class FlyFormInline(admin.TabularInline):
  model = FlyForm
  exclude = ['body']
  readonly_fields = ['link']
  extra = 0
  can_delete = False
  verbose_name = _('Associated Form')
  verbose_name_plural = _('Associated Form')

  def link(self, obj):
    url = reverse('admin:flyform_flyform_change', args=(obj.pk,))
    return mark_safe('<a href="%s">%s</a>' % (url, _('Edit Form'),))
  # the following is necessary if 'link' method is also used in list_display
  link.allow_tags = True


class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    # inlines = [
    #   FlyFormInline
    # ]


class DocumentTemplateCategoryAdmin(CategoryBaseAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentTemplateCategory, DocumentTemplateCategoryAdmin)
admin.site.register([ClientCreatedDocument])