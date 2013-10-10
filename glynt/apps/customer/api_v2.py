# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows user to be viewed or edited.
    """
    queryset = User.objects.select_related('profile').all()
    serializer_class = UserSerializer
    lookup_field = 'pk'