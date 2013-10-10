# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Project
from threadedcomments.models import ThreadedComment


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='__unicode__')
    customer = serializers.SerializerMethodField('get_customer')
    company = serializers.SerializerMethodField('get_company')
    transactions = serializers.SerializerMethodField('get_transactions')
    lawyers = serializers.SerializerMethodField('get_lawyers')

    status = serializers.SerializerMethodField('get_status')

    class Meta:
        model = Project
        queryset = Project.objects.prefetch_related('customer', 'customer__user', 'company', 'transactions', 'lawyers', 'lawyers__user').all()
        fields = ('uuid', 'name', 'customer', 'company',
                  'transactions', 'lawyers',
                  'status',)

    def get_customer(self, obj):
        if obj is not None:
            user = obj.customer.user
            return {
                'pk': user.pk,
                'full_name': user.get_full_name(),
                'photo': user.profile.get_mugshot_url(),
            }

    def get_company(self, obj):
        if obj is not None:
            return {
                'pk': obj.company.pk,
                'name': obj.data.get('company_name'),
            }

    def get_lawyers(self, obj):
        if obj is not None:
            return [{
                        'pk': lawyer.pk,
                        'user_pk': lawyer.user.pk,
                        'full_name': lawyer.user.get_full_name(),
                        'photo': lawyer.profile_photo,
                        'url': lawyer.get_absolute_url(),
                    } for lawyer in obj.lawyers.all()]

    def get_transactions(self, obj):
        if obj is not None:
            return [{'type': t.slug, 'name': t.title} for t in obj.transactions.all()]

    def get_status(self, obj):
        if obj is not None:
            return {
                'id': obj.status,
                'name': obj.display_status,
            }


class DiscussionSerializer(serializers.ModelSerializer):
    site_id = serializers.IntegerField(default=settings.SITE_ID)

    content_type_id = serializers.IntegerField()
    object_pk = serializers.IntegerField()
    parent_id = serializers.IntegerField(required=False)
    last_child = serializers.IntegerField(source='last_child_id', read_only=True)

    user = serializers.IntegerField(source='user_id')
    title = serializers.CharField(required=False)
    comment = serializers.CharField()

    meta = serializers.SerializerMethodField('get_meta')

    class Meta:
        model = ThreadedComment
        queryset = ThreadedComment.objects.prefetch_related('user').all().order_by('-id')

        fields = ('id', 'object_pk', 'title', 'comment', 'user',
                  'content_type_id', 'parent_id', 'last_child',
                  'meta', 'site_id')

    def get_meta(self, obj):
        if obj is not None:
            user = obj.user
            return {
                'timestamp': obj.submit_date.strftime('%s'),
                'user': {
                            'pk': user.pk,
                            'username': user.username,
                            'full_name': user.get_full_name(),
                            'photo': user.profile.get_mugshot_url()
                        }
            }