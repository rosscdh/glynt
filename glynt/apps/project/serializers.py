# -*- coding: UTF-8 -*-
from rest_framework import serializers

from .models import Project
from threadedcomments.models import ThreadedComment


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
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
        user = obj.customer.user
        return {
            'pk': user.pk,
            'full_name': user.get_full_name(),
            'photo': user.profile.get_mugshot_url(),
        }

    def get_company(self, obj):
        return {
            'pk': obj.company.pk,
            'name': obj.data.get('company_name'),
        }

    def get_lawyers(self, obj):
        return [{
                    'pk': lawyer.pk,
                    'user_pk': lawyer.user.pk,
                    'full_name': lawyer.user.get_full_name(),
                    'photo': lawyer.profile_photo,
                    'url': lawyer.get_absolute_url(),
                } for lawyer in obj.lawyers.all()]

    def get_transactions(self, obj):
        return [{'type': t.slug, 'name': t.title} for t in obj.transactions.all()]

    def get_status(self, obj):
        return {
            'id': obj.status,
            'name': obj.display_status,
        }


class DiscussionSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field(source='id')
    user = serializers.SerializerMethodField('get_user')
    timestamp = serializers.SerializerMethodField('get_timestamp')
    comment_info =  serializers.SerializerMethodField('get_comment_tree')

    class Meta:
        model = ThreadedComment
        queryset = ThreadedComment.objects.prefetch_related('user').all()
        fields = ('pk', 'title', 'comment', 'user', 'timestamp', 'comment_info')

    def get_user(self, obj):
        user = obj.user
        return {
            'pk': user.pk,
            'full_name': obj.user_name,
            'photo': user.profile.get_mugshot_url(),
        }

    def get_timestamp(self, obj):
        return obj.submit_date.strftime('%s')

    def get_comment_tree(self, obj):
        return {
            'is_removed': obj.is_removed,
            'tree_path': obj.tree_path,
            'parent_id': obj.parent_id,
            'last_child': obj.last_child,
            'is_public': obj.is_public
        }
        