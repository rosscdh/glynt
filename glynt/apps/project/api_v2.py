# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_unicode
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ParseError
from rest_framework.generics import (RetrieveAPIView, ListCreateAPIView,
                                     RetrieveUpdateAPIView)


from threadedcomments.models import ThreadedComment

from .models import Project, ProjectLawyer
from .serializers import (ProjectSerializer, TeamSerializer,
                          DiscussionSerializer, DiscussionThreadSerializer,)

import StringIO
import logging
logger = logging.getLogger('django.request')


class ProjectViewSet(ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'uuid'


class TeamListView(RetrieveUpdateAPIView):
    """
    Endpoint that shows team for a project
    """
    lawyers = []
    customers = []
    participants = []

    queryset = Project.objects.all()
    serializer_class = TeamSerializer
    lookup_field = 'uuid'

    def __init__(self, *args, **kwargs):
        super(TeamListView, self).__init__(*args, **kwargs)
        # full reset
        self.lawyers = []
        self.customers = []
        self.participants = []

    def put(self, request, **kwargs):
        return HttpResponseNotAllowed('PUT not allowed')

    def patch(self, request, **kwargs):
        """
        request.DATA should provide: [74,3,22] a list of User pks
        we then calculate the user type and update the appropriate field
        on the project
        """
        project_team = request.DATA
        if type(project_team) not in [dict] or project_team.get('team', False) is False:
            return HttpResponseBadRequest('You must PATCH a dict in the following form into this view e.g. PATCH:{"team": [74, 3, 22]}')

        user_ids = project_team['team']

        if type(user_ids) not in [list] or len(user_ids) is 0:
            return HttpResponseBadRequest('You must PATCH a dict in the following form into this view e.g. PATCH:{"team": [74, 3, 22]}')
        
        self.project = self.get_object()

        for u in User.objects.filter(pk__in=user_ids):
            self.set_participant(user=u)

        self.save_all()

        serializer = self.get_serializer(self.project)

        return Response(data=serializer.data, status=202)

    def set_participant(self, user):
        self.participants.append(user)

        if user.profile.is_lawyer is True:
            self.set_lawyer(lawyer_profile=user.lawyer_profile)

        elif user.profile.is_customer is True:
            self.set_customer(customer_profile=user.customer_profile)

    def set_lawyer(self, lawyer_profile):
        self.lawyers.append(lawyer_profile)

    def set_customer(self, customer_profile):
        self.customers.append(customer_profile)

    def save_all(self):
        """
        save all our bits
        """
        self.save_lawyers()
        self.save_customer()
        self.save_participants()

        # Save the changes made to the participants and lawyers
        self.project.save()

    def save_lawyers(self):
        if len(self.lawyers) > 0:
            project = self.project

            # get the current lawyers
            project_lawyers = project.lawyers.all()

            # remove those no longer present
            for lawyer in project_lawyers:
                if lawyer not in self.lawyers:
                    ProjectLawyer.objects.get(project=project, lawyer=lawyer).delete()

            # update the set
            project_lawyers = project.lawyers.all()

            # add new ones
            for lawyer in self.lawyers:
                if lawyer not in project_lawyers:
                    #project.lawyers.add(lawyer) # CANT USE ADD due to custom through table
                    # ProjectLawyer.objects.get_or_create(project=project, lawyer=lawyer, status=ProjectLawyer._LAWYER_STATUS.potential)  # removed temporarily until we talk about status
                    ProjectLawyer.objects.get_or_create(project=project, lawyer=lawyer, status=ProjectLawyer._LAWYER_STATUS.assigned)

    def save_customer(self):
        """
        customer never changes @NOTE this may change in the future thus the interface
        """
        pass

    def save_participants(self):
        """
        save the participants
        this is important as its participants that form
        the notification chain
        """
        if len(self.participants) > 0:
            project = self.project

            # get the current participants
            project_participants = project.participants.all()

            # remove those no longer present
            for participant in project_participants:
                if participant not in self.participants:
                    project.participants.remove(participant)
                    logger.debug('Removing participant: %s' % participant)

            # update the set
            project_participants = project.participants.all()

            # add new ones
            for participant in self.participants:
                if participant not in project_participants:
                    project.participants.add(participant)
                    logger.debug('Adding participant: %s' % participant)


class DiscussionListView(ListCreateAPIView):
    """
    Endpoint that shows discussion threads
    django_comments & threaded_comments & fluent_comments
    """
    queryset = ThreadedComment.objects.prefetch_related('user').all().order_by('-id')
    serializer_class = DiscussionSerializer

    def get_queryset(self):
        """
        """
        project_uuid = self.kwargs.get('uuid')
        project = get_object_or_404(Project, uuid=project_uuid)

        return self.queryset.filter(content_type=Project.content_type(),
                                    object_pk=project.pk)


class DiscussionDetailView(RetrieveAPIView):
    queryset = ThreadedComment.objects.prefetch_related('user').all().order_by('-id')
    serializer_class = DiscussionThreadSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        parent_pk = self.kwargs.get('pk')
        project_uuid = self.kwargs.get('uuid')
        get_object_or_404(Project, uuid=project_uuid)  # ensure that we have the project

        return self.queryset.filter(pk=parent_pk)


class DiscussionTagView(APIView):
    queryset = ThreadedComment.objects.prefetch_related('user').all().order_by('-id')

    def get_params(self):
        parent_pk = self.kwargs.get('pk')
        project_uuid = self.kwargs.get('uuid')
        get_object_or_404(Project, uuid=project_uuid)  # ensure that we have the project
        return (parent_pk, project_uuid)

    def get_queryset(self):
        parent_pk, project_uuid = self.get_params()
        return self.queryset.get(pk=parent_pk).tags

    def response(self, status):
        qs = self.get_queryset()
        return Response([tag.name for tag in qs.all()], status=status)

    def decode_from_body(self, data):
        stream = StringIO.StringIO(data.encode("utf-8"))
        posted_tags = JSONParser().parse(stream)

        if type(posted_tags) not in [list]:
            raise ParseError(detail='Must post a list of at least 1 tag ["tag number 1"]')

        posted_tags = [smart_unicode(tag) for tag in posted_tags]  # decode to unicode

        return posted_tags

    def get(self, request, **kwargs):
        return self.response(status=200)

    def post(self, request, **kwargs):
        posted_tags = self.decode_from_body(data=request.POST.get("_content"))

        qs = self.get_queryset()
        qs.add(*posted_tags)

        return self.response(status=201)

    def delete(self, request, **kwargs):
        posted_tag = kwargs.get('tag', None)

        if posted_tag in [None, '']:
            raise ParseError(detail='Must include a tag in the url i.e. /api/v2/project/:project_uuid/discussion/:discussion_pk/tags/:tag/')

        qs = self.get_queryset()
        qs.remove(posted_tag)

        return self.response(status=202)
