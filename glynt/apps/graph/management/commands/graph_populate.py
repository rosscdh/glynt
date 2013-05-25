# -*- coding: utf-8 -*-
"""
Command to populate Neo4j graph server with relationships
"""
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
#from glynt.apps.graph import graph
from bulbs.neo4jserver import Graph
from glynt.apps.graph.models import GraphConnection
from glynt.apps.graph.neo4j import Person, Knows

import logging
logger = logging.getLogger('lawpal.graph')

graph = Graph()
graph.add_proxy("people", Person)
graph.add_proxy("knows", Knows)

class Command(BaseCommand):

    help = 'Adds relationships to neo4j'

    def clean_database(self):
        if graph.E:
            for e in graph.E:
                graph.edges.delete(e.eid)

        if graph.V:
            for v in graph.V:
                graph.vertices.delete(v.eid)

    def handle(self, *args, **options):
        self.clean_database()

        # Create a unique list of all the nodes we need
        user_nodes = {}

        # Users
        users = User.objects.select_related('social_auth').filter(id__gte=0)
        for user in users:
            node = {'id': user.id, 'full_name': user.get_full_name()}
            for auth in user.social_auth.all():
                node[auth.provider] = auth.uid
            if 'linkedin' in node:
                node['id'] = node['linkedin']
                user_nodes[user.id] = node

        # Create user nodes
        user_cache = {}
        for iid, node in user_nodes.items():
            v = graph.people.create(**node)
            user_cache[iid] = v

        # Connections
        connections = GraphConnection.objects.select_related('users').all()

        for conn in connections:
            # each connection will require at least 2 nodes (1 from and 1 to)
            # create to node

            users = graph.people.index.lookup(linkedin=conn.provider_uid)
            if users:
                for user in users:
                    from_user = user

                for user in conn.users.all():
                    users = graph.people.index.lookup(linkedin=user_nodes[user.id]['id'])
                    for user in users:
                        to_user = user
                    graph.knows.create(from_user, to_user)
                    graph.knows.create(to_user, from_user)

            """
            if conn.users:
                to_vert = user_cache[conn.to_user.id]
            else:
                to_vert = graph.vertices.create({'full_name': conn.full_name, conn.provider: conn.uid})

            # create from node(s)
            for from_user in conn.from_users.all():
                from_vert = user_cache[from_user.id]
                graph.edges.create(from_vert, conn.provider, to_vert)
            """