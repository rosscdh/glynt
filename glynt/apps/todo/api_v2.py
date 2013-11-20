# -*- coding: UTF-8 -*-
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework.viewsets import ModelViewSet

from threadedcomments.models import ThreadedComment

from glynt.apps.project.models import Project
from glynt.apps.project.serializers import (DiscussionThreadSerializer,)

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


class ToDoDiscussionDetailView(ModelViewSet):
    queryset = ThreadedComment.objects.select_related('user', 'tagged_items__tag').all().order_by('-id')
    serializer_class = DiscussionThreadSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        parent_pk = self.kwargs.get('parent_pk')
        get_object_or_404(Project, uuid=self.kwargs.get('uuid'))  # ensure that we have the project
        get_object_or_404(ToDo, slug=self.kwargs.get('slug'))  # ensure we have the slug
        #
        # @BUSINESS RULE: /discussion/:pk/ should return the parent
        # as well as a the children as a "thread": []
        #
        return self.queryset.filter(pk=parent_pk)


class ToDoFeedbackRequestView(ModelViewSet):
    queryset = FeedbackRequest.objects.prefetch_related().all()
    serializer_class = FeedbackRequestSerializer