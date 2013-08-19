# -*- coding: utf-8 -*-
from django import template

register = template.Library()

from notifications.models import Notification

from glynt.apps.project.models import Project, ProjectLawyer
from glynt.apps.project.utils import PROJECT_CONTENT_TYPE


@register.simple_tag(takes_context=True)
def project_name(context, project, index=1):
    transactions = [t.title for t in project.transactions.all()]
    return u'#{index} {company}: {transactions}'.format(**{'company': project.company, 'index': index, 'transactions': ', '.join(transactions)})


@register.inclusion_tag('project/partials/activity_list.html')
def project_activity_stream(project, limit=10):
    return {
        'object_list': Notification.objects.filter(target_object_id=project.pk, target_content_type=PROJECT_CONTENT_TYPE)[:limit]
    }


@register.inclusion_tag('project/partials/project_lawyers.html')
def project_lawyers(project, display_type='default'):
    context = {}

    if display_type == 'assigned':
        lawyer_join = ProjectLawyer.objects.assigned(project=project).prefetch_related('project', 'lawyer')

    elif display_type == 'potential':
        lawyer_join = ProjectLawyer.objects.potential(project=project).prefetch_related('project', 'lawyer')

    else:
        lawyer_join = ProjectLawyer.objects.filter(project=project)

    num_lawyers = len(lawyer_join)

    context.update({
        'project': project,
        'lawyers': [j.lawyer for j in lawyer_join],
        'num_lawyers': num_lawyers,
        'display_type': display_type
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
                    projects = Project.objects.filter(lawyers=lawyer, customer=user.customer_profile)

    return {
        'projects': projects,
        'num_projects': len(projects),
        'is_own_profile': is_own_profile
    }


@register.inclusion_tag('lawyer/partials/engage_lawyer.html', takes_context=True)
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
