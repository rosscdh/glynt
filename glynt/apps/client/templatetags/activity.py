from django import template

import user_streams

register = template.Library()

@register.inclusion_tag('activity/activity_list.html')
def user_activity_stream(user, limit=10):
  return {
    'object_list': user_streams.get_stream_items(user)[:limit]
  }