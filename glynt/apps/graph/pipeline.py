# -*- coding: utf-8 -*-
from social_auth.models import UserSocialAuth
from tasks import collect_user_graph_connections


def graph_user_connections(backend, details, response, user=None, is_new=False,
                        *args, **kwargs):
	auth = UserSocialAuth.objects.get(user=user, provider=backend.name)
	try:
		collect_user_graph_connections.delay(auth=auth)
	except:
		collect_user_graph_connections(auth=auth)
