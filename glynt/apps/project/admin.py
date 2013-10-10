# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.admin.util import unquote
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import get_text_list
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect

from bunch import Bunch
from templated_email import send_templated_mail

from glynt.apps.project.models import Project, ProjectLawyer

import logging
logger = logging.getLogger('lawpal.project')

csrf_protect_m = method_decorator(csrf_protect)


class ProjectLawyerInline(admin.TabularInline):
    model = ProjectLawyer
    extra = 2


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectLawyerInline]
    list_display = ('__unicode__', 'date_created', 'date_modified', 'uuid')
    list_filter = ['status', 'transactions']
    search_fields = ('company', 'customer', 'lawyers', 'transactions', 'uuid')
    send_matches_confirmation_template = None

    def get_queryset(self, request):
        qs = Project.objects.select_related('company', 'customer', 'customer__user').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_urls(self):
        urls = super(ProjectAdmin, self).get_urls()

        # info = self.model._meta.app_label, self.model._meta.model_name
        info = self.model._meta.app_label, 'project'

        my_urls = patterns(
            '',
            url(
                r'^(.+)/send_matches/$',
                self.admin_site.admin_view(self.send_matches_view),
                name='%s_%s_send_matches' % info
            ),
        )

        return my_urls + urls

    def send_matches(self, request, obj, client, lawyers):
        """
        Sent the matches email.
        """
        logger.info('Sending project matches email')

        recipient = '"{name}" <{email}>'.format(name=client.get_full_name(), email=client.email)
        email = Bunch(
            template_name='project_matches',
            from_email='"LawPal ({company})" <noreply@lawpal.com>'.format(company=obj.company),
            recipient_list=[recipient],
            bcc=['founders@lawpal.com'],
            context={
                'lawyers': lawyers,
                'to_name': client.first_name,
                'url': reverse('dashboard:overview'),
            }
        )

        if settings.DEBUG:
            email.pop('bcc')

        send_templated_mail(**email)

    def log_send_matches(self, request, object, object_repr, lawyers):
        """
        Log that a matches email has been successfully sent.
        """
        from django.contrib.admin.models import LogEntry, CHANGE

        lawyers_repr = []
        for lawyer in lawyers:
            lawyers_repr.append(lawyer)

        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(object).pk,
            object_id=object.pk,
            object_repr=object_repr,
            action_flag=CHANGE,
            change_message=_("Sent matches email (Lawyers: %s.)") % get_text_list(lawyers_repr, _('and'))
        )

    def response_send_matches(self, request, obj_display):
        """
        Determines the HttpResponse for the send_matches_view stage.
        """
        opts = self.model._meta

        self.message_user(request, _(
            'The matches email for "%(obj)s" was sent successfully.') % {'obj': force_text(obj_display)},
            messages.SUCCESS)

        post_url = reverse('admin:%s_%s_changelist' %
                           # (opts.app_label, opts.model_name),
                           (opts.app_label, 'project'),
                           current_app=self.admin_site.name)

        return HttpResponseRedirect(post_url)

    def render_send_matches_form(self, request, context):
        opts = self.model._meta
        app_label = opts.app_label

        return TemplateResponse(request, self.send_matches_confirmation_template or [
            # "admin/{}/{}/send_matches_confirmation.html".format(app_label, opts.model_name),
            "admin/{}/{}/send_matches_confirmation.html".format(app_label, 'project'),
            "admin/{}/send_matches_confirmation.html".format(app_label),
            "admin/send_matches_confirmation.html"
        ], context, current_app=self.admin_site.name)

    @csrf_protect_m
    def send_matches_view(self, request, object_id, extra_context=None):
        "The 'send matches' admin view for this model."
        opts = self.model._meta
        app_label = opts.app_label

        obj = get_object_or_404(self.get_queryset(request), pk=unquote(object_id))

        client = obj.customer.user
        lawyers = obj.lawyers.all()

        if request.POST:  # The user has already confirmed.
            obj_display = force_text(obj)
            self.log_send_matches(request, obj, obj_display, lawyers)
            self.send_matches(request, obj, client, lawyers)

            return self.response_send_matches(request, obj_display)

        object_name = force_text(opts.verbose_name)

        title = _("Are you sure?")
        context = dict(
            title=title,
            object_name=object_name,
            object=obj,
            client=client,
            lawyers=lawyers,
            opts=opts,
            app_label=app_label,
        )
        context.update(extra_context or {})

        return self.render_send_matches_form(request, context)


class ProjectLawyerAdmin(admin.ModelAdmin):
    list_display = ('project', 'lawyer', 'display_status',)
    list_filter = ['status']
    search_fields = ('project', 'lawyer',)

    def get_queryset(self, request):
        qs = ProjectLawyer.objects.select_related('project__company', 'project__customer', 'project__customer__user').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectLawyer, ProjectLawyerAdmin)
