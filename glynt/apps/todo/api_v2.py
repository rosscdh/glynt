# -*- coding: UTF-8 -*-
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from glynt.apps.project.models import Project

from .serializers import AttachmentSerializer
from .models import ToDo, Attachment


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
