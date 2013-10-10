# -*- coding: UTF-8 -*-
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView

from threadedcomments.models import ThreadedComment

from . import PROJECT_CONTENT_TYPE
from .serializers import (ProjectSerializer, DiscussionSerializer, )
from .models import Project


class ProjectViewSet(ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'uuid'


class DiscussionListView(ListCreateAPIView):
    """
    Endpoint that shows discussion threads
    django_comments & threaded_comments & fluent_comments
    """
    queryset = ThreadedComment.objects.all()
    serializer_class = DiscussionSerializer

    def get_queryset(self):
        """
        """
        project_uuid = self.kwargs.get('uuid')
        project = get_object_or_404(Project, uuid=project_uuid)

        return self.queryset.filter(content_type=PROJECT_CONTENT_TYPE,
                                    object_pk=project.pk)


class TeamListView(ListCreateAPIView, RetrieveUpdateAPIView):
    """
    Endpoint that shows team for a project
    """
    queryset = ThreadedComment.objects.all()
    serializer_class = DiscussionSerializer

    def get_queryset(self):
        """
        """
        project_uuid = self.kwargs.get('uuid')
        project = get_object_or_404(Project, uuid=project_uuid)

        return self.queryset.filter(content_type=PROJECT_CONTENT_TYPE,
                                    object_pk=project.pk)


class DiscussionDetailView(RetrieveUpdateDestroyAPIView, DiscussionListView):
    lookup_field = 'pk'
