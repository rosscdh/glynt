# -*- coding: utf-8 -*-
from django import template

register = template.Library()

import user_streams
from notifications.models import Notification

from glynt.apps.project.models import Project
from glynt.apps.project.utils import PROJECT_CONTENT_TYPE


@register.simple_tag(takes_context=True)
def project_name(context, project, index=1):
    user = context.get('user')
    transactions = [t.title for t in project.transactions.all()]
    return u'#{index} {company}: {transactions}'.format(**{'company': project.company, 'index': index, 'transactions': ', '.join(transactions)})


@register.inclusion_tag('project/partials/activity_list.html')
def project_activity_stream(project, limit=10):
  return {
    'object_list': Notification.objects.filter(target_object_id=project.pk, target_content_type=PROJECT_CONTENT_TYPE)[:limit]
  }


@register.inclusion_tag('project/partials/project_lawyers.html')
def project_lawyers(project):
    context = {}
    lawyers = project.lawyers.all()
    num_lawyers = len(lawyers)
    context.update({
        'project': project,
        'lawyers': lawyers,
        'num_lawyers': num_lawyers,
    })
    return context


@register.inclusion_tag('project/partials/project_intro.html', takes_context=True)
def project_intro(context, project):
    context.update({
        'project': project,
    })
    return context


def project_dict(context, user=None):
    projects = []
    user = context.get('user', user)
    lawyer = context.get('lawyer', None)
    is_own_profile = True if lawyer.user.pk == user.pk else False

    if user is not None:
        if user.is_authenticated():
            if not is_own_profile:
                if user.profile.is_customer:
                    projects = Project.objects.filter(lawyer=lawyer, customer=user.customer_profile)

    return {
        'projects': projects,
        'num_projects': len(projects),
        'is_own_profile': is_own_profile
    }


@register.inclusion_tag('project/partials/project_with_lawyer.html', takes_context=True)
def project_with_lawyer(context, lawyer):
    context.update({
        'lawyer': lawyer,
    })

    context.update(
        project_dict(context)
    )

    return context


@register.inclusion_tag('project/partials/project_with_lawyer_button.html', takes_context=True)
def engage_with_lawyer_button(context, lawyer=None, user=None):
    user = context.get('user', user)
    lawyer = context.get('lawyer', lawyer)
    data = {}
    data.update({
        'lawyer': lawyer,
    })
    data.update(project_dict(context=context, user=user))
    data.update({
        'has_projects': True if data.get('projects') else False,
    })
    context.update(data)
    return context


@register.inclusion_tag('project/partials/user_project_notification_count.js', takes_context=False)
def user_project_notification_count(user):
    unread = {}

    # get a grouped by result set
    unread_qs = Notification.objects.filter(recipient=user, unread=True, target_content_type=PROJECT_CONTENT_TYPE)

    # build a nice jsonifyable dict
    for u in unread_qs:
        # target_object_id is the id of the content object (project)
        if u.target_object_id not in unread:
            unread[u.target_object_id] = unread.get(u.target_object_id, 1)
        else:
            unread[u.target_object_id] += 1
    return {
        'unread': unread
    }
