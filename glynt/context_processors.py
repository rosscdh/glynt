# -*- coding: utf-8 -*-
import os
from django.conf import settings

from glynt.apps.project.models import Project, ProjectLawyer



def project_info(request):
    PROJECT_NAME = getattr(settings, 'PROJECT_NAME', 'LawPal')
    return {
      'PROJECT_NAME': PROJECT_NAME
    }


def project_environment(request):
    PROJECT_ENVIRONMENT = getattr(settings, 'PROJECT_ENVIRONMENT', 'prod')
    return {
      'PROJECT_ENVIRONMENT': PROJECT_ENVIRONMENT
    }


def default_profile_image(request):
    image = getattr(settings, 'DEFAULT_PROFILE_IMAGE', None)
    return {
        'default_profile_image': os.path.abspath('%s%s' % (settings.STATIC_URL, image))
    }


def USE_THREADEDCOMMENTS(request):
    return {
        'USE_THREADEDCOMMENTS': True if 'threadedcomments' in settings.INSTALLED_APPS else False
    }


def PUSHER_DATA(request):
    return {
      'PUSHER_APP_ID': getattr(settings, 'PUSHER_APP_ID'),
      'PUSHER_KEY': getattr(settings, 'PUSHER_KEY')
    }

def user_projects(request):
    """
    Ensures the users projects and project are in the context at all times
    """
    projects = []
    project = None

    if request.user.is_authenticated() and not request.user.is_staff and not request.user.is_superuser:

        if request.user.profile.is_lawyer:
            projects = [join.project for join in ProjectLawyer.objects.assigned(lawyer=request.user.lawyer_profile)]
            try:
                project = projects[0]
            except IndexError:
                pass
        elif request.user.profile.is_customer:
            projects = Project.objects.current(customer=request.user.customer_profile)
            try:
                project = projects[0]
            except IndexError:
                pass
    return {
        'projects': projects,
        'project': project,
    }