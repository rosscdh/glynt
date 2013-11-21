# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Customer


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True, required=False)
    photo = serializers.CharField(source='profile.get_mugshot_url', read_only=True, required=False)
    is_lawyer = serializers.BooleanField(source='profile.is_lawyer', read_only=True, required=False)
    is_customer = serializers.BooleanField(source='profile.is_customer', read_only=True, required=False)

    class Meta:
        model = User
        queryset = User.objects.select_related('profile').all()

        fields = ('id', 'username', 'email', 'full_name',
            'photo', 'is_lawyer', 'is_customer')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
