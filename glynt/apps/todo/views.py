# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, DetailView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages

from glynt.apps.project.services.project_checklist import ProjectCheckListService
from glynt.apps.project.models import Project

from braces.views import JSONResponseMixin

from .forms import CutomerToDoForm, AttachmentForm
from .models import ToDo, Attachment
from .services import CrocdocAttachmentService


class ProjectToDoView(ListView):
    model = ToDo
    paginate_by = 1  # 10

    def get_queryset(self):
        """
        Provide a list of todos for the current user
        """
        order_by = self.request.GET.get('order_by', '-id')  # newest first

        fltr = {
            'status': self.request.GET.get('status', 1)  # newest first
        }

        # filter by the current user always
        # & filter by the params passed in
        queryset = self.model.objects.prefetch_related('user', 'project') \
                                     .filter(user=self.request.user) \
                                     .filter(**fltr)

        return queryset.order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super(ProjectToDoView, self).get_context_data(**kwargs)

        self.project = get_object_or_404(Project, uuid=self.kwargs.get('uuid'))
        self.checklist_service = ProjectCheckListService(project=self.project)

        context.update({
            'project': self.project,
            'checklist': self.checklist_service,
            'counts': {
                'new': self.model.objects.unassigned(project=self.project, user=self.request.user).count(),
                'open': self.model.objects.assigned(project=self.project, user=self.request.user).count(),
                'closed': self.model.objects.closed(project=self.project, user=self.request.user).count(),
            }
        })
        return context


class BaseToDoDetailMixin(SingleObjectMixin):
    model = ToDo

    def get_context_data(self, **kwargs):
        context = super(BaseToDoDetailMixin, self).get_context_data(**kwargs)
        context.update({
            'project': self.project_service.project,
        })
        return context

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        slug = self.kwargs.get(self.slug_url_kwarg, 'slug')

        self.project = get_object_or_404(Project, uuid=self.kwargs.get('project_uuid'))
        self.project_service = ProjectCheckListService(project=self.project)

        self.items = self.project_service.todo_item_by_slug(slug=slug)

        item = self.items.current

        if item is None:
            return None
        else:
            # if slug in [None, u'None']:
            #     # TODO abstract this into a service method
            #     slug = self.project_service.item_slug(item=Bunch(name=self.request.POST.get('name')), rand=random.random())

            obj, is_new = self.model.objects.get_or_create(slug=slug, project=self.project)

            if is_new and item:
                obj.name = item.name
                obj.category = item.category
                obj.description = item.description
                obj.status = item.status
                obj.data = item
                obj.save()

            return obj


class ToDoDetailView(DetailView, BaseToDoDetailMixin):
    template_name = 'todo/todo_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ToDoDetailView, self).get_context_data(**kwargs)
        context.update({
            'attachment_form': AttachmentForm(initial={'project': self.project.pk, 'todo': self.object.pk}),
            'back_and_forth': self.items,
        })
        return context


class ToDoDiscussionView(DetailView, BaseToDoDetailMixin):
    template_name = 'todo/discussion.html'


class ToDoEditView(UpdateView, BaseToDoDetailMixin, ModelFormMixin):
    template_name = 'todo/todo_form.html'
    form_class = CutomerToDoForm

    def get_success_url(self):
        return self.project.get_checklist_absolute_url()

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(ToDoEditView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'project_service': self.project_service,
            'project_uuid': self.kwargs.get('project_uuid'), 
            'slug': self.kwargs.get('slug'), 
        })
        return kwargs

    def form_valid(self, form):
        #messages.success(self.request, 'Sucessfully updated this item. <a href="{href}">view</a>'.format(href=self.object.get_absolute_url()), extra_tags='safe')
        return super(ToDoEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating this item')
        return super(ToDoEditView, self).form_valid(form)


class ToDoCreateView(ToDoEditView):
    template_name = 'todo/todo_form.html'
    form_class = CutomerToDoForm


class ToDoAttachmentView(DetailView, BaseToDoDetailMixin):
    template_name = 'todo/attachments.html'


class ToDoAssignView(DetailView, BaseToDoDetailMixin):
    template_name = 'todo/assign.html'



class AttachmentSessionView(JSONResponseMixin, DetailView):
    model = Attachment
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    json_dumps_kwargs = {'indent': 3}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        service = CrocdocAttachmentService(attachment=self.object)

        context_dict = {
            'session_key': service.session_key(),
            'uuid': service.uuid,
            'view_url': service.view_url(),
        }

        return self.render_json_response(context_dict)