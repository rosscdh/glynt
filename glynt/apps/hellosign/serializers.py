# -*- coding: UTF-8 -*-
from rest_framework import serializers

from .models import Signature


class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        queryset = Signature.objects.select_related().all()
