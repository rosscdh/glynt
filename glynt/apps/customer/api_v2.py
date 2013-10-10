# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter

from .serializers import UserSerializer

import django_filters

DEFAULT_FILTERS = ['icontains', 'contains', 'startswith']


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_type='startswith')
    email = django_filters.CharFilter(lookup_type='startswith')

    class Meta:
        model = User
        fields = ['username', 'email']


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows user to be viewed or edited.
    """
    queryset = User.objects.select_related('profile').all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    
    def create(self, request):
        raise PermissionDenied

    def update(self, request, pk=None):
        raise PermissionDenied

    def partial_update(self, request, pk=None):
        raise PermissionDenied

    def destroy(self, request, pk=None):
        raise PermissionDenied