# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from rest_framework import serializers

from .services import CrocdocAttachmentService
from .models import Attachment


def _user_dict(user):
    return {
        'pk': user.pk,
        'username': user.username,
        'full_name': user.get_full_name(),
        'photo': user.profile.get_mugshot_url()
    } if user is not None else {}


class AttachmentSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField('get_filename')
    uploaded_by = serializers.SerializerMethodField('get_uploaded_by')
    deleted_by = serializers.SerializerMethodField('get_deleted_by')
    crocdoc_url = serializers.SerializerMethodField('get_crocdoc_url')
    filepicker_url = serializers.SerializerMethodField('get_filepicker_url')

    class Meta:
        model = Attachment
        queryset = Attachment.objects.all()
        fields = ('id', 'uuid', 'filename', 'uploaded_by', 'deleted_by', 
                  'project', 'todo', 'crocdoc_url', 'filepicker_url',
                  'date_created')

    def get_filename(self, obj):
        return obj.filename

    def get_uploaded_by(self, obj):
        user = obj.uploaded_by
        return _user_dict(user=user)

    def get_deleted_by(self, obj):
        user = obj.deleted_by
        return _user_dict(user=user)

    def get_crocdoc_url(self, obj):
        return reverse('todo:crocdoc_302', kwargs={'pk': obj.pk})

    def get_filepicker_url(self, obj):
        return obj.inkfilepicker_url