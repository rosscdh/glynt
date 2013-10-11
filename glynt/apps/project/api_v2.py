# -*- coding: UTF-8 -*-
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView

from threadedcomments.models import ThreadedComment

from . import PROJECT_CONTENT_TYPE
from .models import Project, ProjectLawyer
from .serializers import (ProjectSerializer, TeamSerializer,
                          DiscussionSerializer, )

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

    def put(self, request, **kwargs):
        raise PermissionDenied

    def patch(self, request, **kwargs):
        """
        request.DATA should provide: [74,3,22] a list of User pks
        we then calculate the user type and update the appropriate field
        on the project
        """
        user_ids = request.DATA

        if type(user_ids) not in [list] or len(user_ids) is 0:
            raise ValidationError('You must PATCH a list into this view e.g. PATCH:[74,3,22]')
        
        self.project = self.get_object()

        for u in User.objects.filter(pk__in=user_ids):
            self.set_participant(user=u)

        self.save_all()

        serializer = self.get_serializer()

        return Response(data=serializer.get_team(obj=self.project), status=202)

    def set_lawyer(self, lawyer_profile):
        self.lawyers.append(lawyer_profile)

    def set_customer(self, customer_profile):
        self.customers.append(customer_profile)

    def set_participant(self, user):
        self.participants.append(user)

        if user.profile.is_lawyer is True:
            self.set_lawyer(lawyer_profile=user.lawyer_profile)

        elif user.profile.is_customer is True:
            self.set_customer(customer_profile=user.customer_profile)

    def save_all(self):
        """
        save all our bits
        """
        self.save_lawyers()
        self.save_customer()
        self.save_participants()

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
                    # ProjectLawyer.objects.get_or_create(project=project, lawyer=lawyer, status=ProjectLawyer.LAWYER_STATUS.potential)  # removed temporarily until we talk about status
                    ProjectLawyer.objects.get_or_create(project=project, lawyer=lawyer, status=ProjectLawyer.LAWYER_STATUS.assigned)

    def save_customer(self):
        """
        customer never changes
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
    queryset = ThreadedComment.objects.all()
    serializer_class = DiscussionSerializer

    def get_queryset(self):
        """
        """
        project_uuid = self.kwargs.get('uuid')
        project = get_object_or_404(Project, uuid=project_uuid)

        return self.queryset.filter(content_type=PROJECT_CONTENT_TYPE,
                                    object_pk=project.pk)


class DiscussionDetailView(RetrieveUpdateDestroyAPIView, DiscussionListView):
    lookup_field = 'pk'
