# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter

from .models import Signature
from .serializers import SignatureSerializer

import django_filters

DEFAULT_FILTERS = ['icontains', 'contains', 'startswith']


class SignatureViewSet(ModelViewSet):
    """
    API endpoint that allows Signatures to be viewed or edited.
    """
    queryset = Signature.objects.select_related().all()
    serializer_class = SignatureSerializer

    def get_queryset(self):
        project_uuid = self.kwargs.get('uuid')
        project = get_object_or_404(Project, uuid=project_uuid)
        return self.queryset.filter(project=project)