from django import template
from forms import InviteEmailForm

register = template.Library()


@register.inclusion_tag('invite/invite.html', takes_context=True)
def invite_to_lawpal(context, document, target_element):
    return {
        'form': InviteEmailForm()
        ,'STATIC_URL': context['STATIC_URL']
    }
