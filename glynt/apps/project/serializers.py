# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Project
from threadedcomments.models import ThreadedComment

from glynt.apps.customer.serializers import UserSerializer

import re

UUID4HEX_LONG = re.compile('[0-9a-f]{32}\Z', re.I)
UUID4HEX_SHORT = re.compile('[0-9a-f]{11}\Z', re.I)


class GetContentObjectByTypeAndPkMixin(object):
    """
    Mixin to allow searching for ContentType objects
    by pk or by uuid
    """
    def is_uuid(self, value):
        if type(value) in [unicode, str]:
            if UUID4HEX_LONG.match(value) or UUID4HEX_SHORT.match(value):
                # is a uuid
                return True
        return False

    def get_content_type_obj(self, content_type_id):
        return ContentType.objects.get(pk=content_type_id)

    def get_object_by_key(self, content_type_id, key):
        # get the type of object
        content_type = self.get_content_type_obj(content_type_id=content_type_id)

        # get the specific object being referenced
        if self.is_uuid(value=key):
            return content_type.get_object_for_this_type(uuid=key)
        else:
            return content_type.get_object_for_this_type(pk=key)


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
            return UserSerializer(user).data

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
                        'username': lawyer.user.username,
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


class TeamSerializer(serializers.Serializer):
    """
    Compile a set of user objects that make up a Projects team
    customer, lawyers, parties
    """
    team = serializers.SerializerMethodField('get_team')

    def get_team(self, obj):
        if obj is not None:

            participants = list(obj.notification_recipients())  # returns itertools chain

            # append potential lawyers as they are not naturally provided
            # by project.notification_recipients
            # potential_lawyers = ProjectLawyer.objects.potential(project=obj)
            # if potential_lawyers:
            #     participants += [join.lawyer.user for join in potential_lawyers]

            for u in participants:
                yield UserSerializer(u).data


class DiscussionSerializer(GetContentObjectByTypeAndPkMixin, serializers.ModelSerializer):
    site_id = serializers.IntegerField(default=settings.SITE_ID, required=False)

    content_type_id = serializers.IntegerField()
    object_pk = serializers.CharField()
    parent_id = serializers.IntegerField(required=False)
    last_child = serializers.IntegerField(source='last_child_id', required=False, read_only=True)

    user = serializers.IntegerField(source='user_id')
    title = serializers.CharField(required=False)
    comment = serializers.CharField()

    tags = serializers.IntegerField(source='tags.all', required=False)
    meta = serializers.SerializerMethodField('get_meta')
    last_child = serializers.SerializerMethodField('get_last_child')

    class Meta:
        model = ThreadedComment
        queryset = ThreadedComment.objects.select_related('user', 'tagged_items__tag').all().order_by('-id')

        fields = ('id', 'object_pk', 'title', 'comment', 'user',
                  'content_type_id', 'parent_id',
                  'tags', 'site_id',
                  'last_child', 'meta',)


    def validate_object_pk(self, attrs, source):
        key = attrs[source]
        content_type_id = attrs.get('content_type_id')

        # get the content_object for this content type and uuid
        content_object = self.get_object_by_key(content_type_id=content_type_id, key=key)

        # set the pk to that objects pk
        attrs[source] = content_object.pk

        return attrs

    def validate_site_id(self, attrs, source):
        """
        force correct site_id
        """
        attrs[source] = settings.SITE_ID
        return attrs

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

    def get_last_child(self, obj):
        if obj is not None and obj.last_child is not None:
            return DiscussionSerializer(obj.last_child).data
        else:
            return None


class DiscussionThreadSerializer(DiscussionSerializer):
    thread = serializers.SerializerMethodField('get_thread')

    class Meta(DiscussionSerializer.Meta):
        fields = ('id', 'object_pk', 'title', 'comment', 'user',
                  'content_type_id', 'parent_id',
                  'tags', 'site_id',
                  'meta', 'thread',)

    def get_thread(self, obj):
        for comment in obj.children.all():
            yield DiscussionSerializer(comment).data    
