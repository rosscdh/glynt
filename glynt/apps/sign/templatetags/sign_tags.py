from django import template

register = template.Library()


@register.inclusion_tag('sign/partials/invite_to_sign.html')
def invite_to_sign(document, target_element):
    return {
    'document': document,
    'target_element': target_element
    }


@register.inclusion_tag('sign/partials/invitee_info.html')
def invitee_detail_list(invitee_list):
    return {
      'object_list': invitee_list
    }
