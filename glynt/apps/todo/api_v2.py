# -*- coding: UTF-8 -*-
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from actstream.models import Action
from rest_framework.viewsets import ModelViewSet

from threadedcomments.models import ThreadedComment

from glynt.apps.project.models import Project
from glynt.apps.project.serializers import (DiscussionThreadSerializer,
                                            ProjectActivitySerializer,)

from .serializers import AttachmentSerializer, FeedbackRequestSerializer
from .models import ToDo, Attachment, FeedbackRequest


class AttachmentViewSet(ModelViewSet):
    """
    API endpoint that allows todo attachments
    """
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def get_queryset(self):
        project = get_object_or_404(Project, uuid=self.kwargs.get('uuid'))
        todo = get_object_or_404(ToDo, slug=self.kwargs.get('slug'))

        return self.queryset.filter(project=project, todo=todo)

    def create(self, request):
        raise PermissionDenied

    def update(self, request, pk=None):
        raise PermissionDenied

    def partial_update(self, request, pk=None):
        raise PermissionDenied

    def destroy(self, request, pk=None):
        raise PermissionDenied


class ToDoActivityView(ModelViewSet):
    queryset = Action.objects.prefetch_related().all()
    serializer_class = ProjectActivitySerializer

    def get_queryset(self):
        project = get_object_or_404(Project, uuid=self.kwargs.get('uuid'))  # ensure that we have the project
        todo = get_object_or_404(ToDo, project=project, slug=self.kwargs.get('slug'))  # ensure that we have the project

        return todo.activity_stream()


class ToDoDiscussionDetailView(ModelViewSet):
    queryset = ThreadedComment.objects.select_related('user', 'tagged_items__tag').all().order_by('-id')
    serializer_class = DiscussionThreadSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        filters = {}

        parent_pk = self.kwargs.get('parent_pk')
        if parent_pk is not None:
            filters.update({"parent_pk": parent_pk})

        project = get_object_or_404(Project, uuid=self.kwargs.get('uuid'))  # ensure that we have the project
        todo = get_object_or_404(ToDo.objects.filter(project=project), slug=self.kwargs.get('slug'))  # ensure we have the slug
        if todo is not None:
            filters.update({"object_pk": todo.pk ,'content_type_id': todo.content_type_id})
        #
        # @BUSINESS RULE: /discussion/:pk/ should return the parent
        # as well as a the children as a "thread": []
        #
        return self.queryset.filter(**filters)


class ToDoFeedbackRequestView(ModelViewSet):
    queryset = FeedbackRequest.objects.prefetch_related().all()
    serializer_class = FeedbackRequestSerializer

    def get_queryset(self):
        filters = {}

        pk = self.kwargs.get('pk')
        if pk is not None:
            filters.update({"pk": pk})

        project = get_object_or_404(Project, uuid=self.kwargs.get('uuid'))  # ensure that we have the project
        todo = get_object_or_404(ToDo.objects.filter(project=project), slug=self.kwargs.get('slug'))  # ensure we have the slug

        if todo is not None:
            filters.update({"attachment__in": todo.attachments.all()})


        return self.queryset.filter(**filters)
