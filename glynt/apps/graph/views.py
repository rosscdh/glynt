from django.http import HttpResponse
from bulbs.neo4jserver import Graph
from glynt.apps.graph.models import GraphConnection
from glynt.apps.graph.neo4j import Person, Knows

graph = Graph()
graph.add_proxy("people", Person)
graph.add_proxy("knows", Knows)

def connections_for_user(user_id)
    user = User.objects.select_related('social_auth').get(id=user_id)
    linkedin_id = user.social_auth.filter(provider="linkedin")[0].uid
    vertices = list(graph.people.index.lookup(linkedin=linkedin_id))
    connections = vertices[0].bothV("knows")
    conns = []
    
    for connection in connections:
        conns.append(connection.id)
    
    return set(conns)

def user(request, user_id):
    user = User.objects.select_related('social_auth').get(id=user_id)
    linkedin_id = user.social_auth.filter(provider="linkedin")[0].uid
    vertices = list(graph.people.index.lookup(linkedin=linkedin_id))
    connections = vertices[0].bothV("knows")
    counts = []
    for connection in connections:
        counts.append(connection.id)
        sconnections = connection.bothV("knows")
        for sconnection in connections:
            counts.append(sconnection.id)
    return len(set(counts))

def user_to_user(request, from_user, to_user):
    from_user_connections = connections_for_user(from_user)
    to_user_connections = connections_for_user(to_user)
    return from_user_connections & to_user_connections #linked_in ids
    
def me(request):
    user_id = 0 # get real user id
    user(request, user_id)


    