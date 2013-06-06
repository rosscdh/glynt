# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse

from django.contrib.comments.templatetags.comments import RenderCommentListNode
from django.template.loader import render_to_string

register = template.Library()

from glynt.apps.engage.models import Engagement


@register.inclusion_tag('engage/partials/engagement_intro.html', takes_context=True)
def engagement_intro(context, enagement):
    context.update({
        'enagement': enagement,
    })
    return context


def engagement_dict(context, user=None):
    engagement_list = []
    user = user if user is not None else context.get('user', None)
    lawyer = context.get('lawyer', None)
    own_profile = True if lawyer.user.pk == user.pk else False

    if user is not None:
        if user.is_authenticated():
            if not own_profile:
                if user.profile.is_founder:
                    engagement_list = Engagement.objects.filter(lawyer=lawyer, founder=user.founder_profile)

    return {
        'engagement_list': engagement_list,
        'own_profile' : own_profile,
    }


@register.inclusion_tag('engage/partials/engagement_with_lawyer.html', takes_context=True)
def engagement_with_lawyer(context, lawyer):

    context.update({
        'lawyer': lawyer,
    })

    context.update(
        engagement_dict(context)
    )

    return context


@register.assignment_tag(takes_context=True)
def is_lawyer_engaged_with_user(context, lawyer, user=None):
    user = user if user is not None else context.get('user', None)
    context.update({
        'lawyer': lawyer,
    })

    lawyer_enganged = False
    data = engagement_dict(context=context, user=user)

    if data.get('engagement_list'):
        lawyer_enganged = True

    return lawyer_enganged



class RenderCommentListReversedNode(RenderCommentListNode):
    """Render the comment list directly in reverse """

    def render(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if object_pk:
            template_search_list = [
                "comments/%s/%s/list.html" % (ctype.app_label, ctype.model),
                "comments/%s/list.html" % ctype.app_label,
                "comments/list.html"
            ]
            qs = self.get_query_set(context).order_by('-id')
            context.push()
            liststr = render_to_string(template_search_list, {
                "comment_list" : self.get_context_value_from_queryset(context, qs)
            }, context)
            context.pop()
            return liststr
        else:
            return ''

@register.tag
def render_comment_list_reversed(parser, token):
    """
    Render the comment list (as returned by ``{% get_comment_list %}``)
    through the ``comments/list.html`` template

    but in reverse order

    Syntax::

        {% render_comment_list_reversed for [object] %}
        {% render_comment_list_reversed for [app].[model] [object_id] %}

    Example usage::

        {% render_comment_list_reversed for event %}

    """
    return RenderCommentListReversedNode.handle_token(parser, token)