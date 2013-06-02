# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.models import User
from bulbs.neo4jserver import Graph

from glynt.apps.graph.models import GraphConnection
from glynt.apps.graph.neo4j import Person, Knows

import json
from bunch import Bunch

graph = Graph()
graph.add_proxy("people", Person)
graph.add_proxy("knows", Knows)

import logging
logger = logging.getLogger('django.request')

api_response = Bunch(meta={
    'from_user': None,
    'total': 0,
    }, items=[])


def user(request, user_id):
    counts = []
    connections = None
    user = User.objects.select_related('social_auth').get(id=user_id)
    logger.info('Graph connections for user %s'% user)

    try:
        linkedin_id = user.social_auth.filter(provider="linkedin")[0].uid
        logger.info('Graph connections for linkedin: %s user %s'% (linkedin_id,user,))
    except IndexError:
        linkedin_id = None

    if linkedin_id is not None:
        graph_user = graph.people.index.lookup(linkedin=linkedin_id)
        if graph_user:
            connections = graph_user.bothV("knows")
            logger.info('Graph connections for linkedin: %s user %s -> %s'% (linkedin_id,user,connections,))

    assert False
    if connections:
        for connection in connections:
            counts.append(connection.id)
            sconnections = connection.bothV("knows")

            for sconnection in connections:
                counts.append(sconnection.id)

    api_response.update({
        'meta': {
            'from_user': user.pk,
            'total': 0,
        },
        'items': counts
        })
    return api_response


def user_to_user(request, from_user, to_user):
    from_user_connections = connections_for_user(from_user)
    to_user_connections = connections_for_user(to_user)
    return HttpResponse(json.dumps(from_user_connections & to_user_connections)) #linked_in ids

def connections_for_user(request, pk):
    return HttpResponse(json.dumps(user(request, pk)))

def me(request):
    user_id = request.user.pk # get real user id
    return HttpResponse(json.dumps(user(request, user_id)))
