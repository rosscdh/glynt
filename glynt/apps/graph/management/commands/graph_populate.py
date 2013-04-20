# -*- coding: utf-8 -*-
"""
Command to populate Neo4j graph server with relationships
"""
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from glynt.apps.graph import graph
from glynt.apps.graph.models import GraphConnection

import logging
logger = logging.getLogger('lawpal.graph')


class Command(BaseCommand):

    help = 'Adds relationships to neo4j'

    def handle(self, *args, **options):
        # Clean out the database first
        if graph.E:
            for e in graph.E:
                graph.edges.delete(e.eid)

        if graph.V:
            for v in graph.V:
                graph.vertices.delete(v.eid)

        # Create a unique list of all the nodes we need
        user_nodes = {}

        # Users
        users = User.objects.select_related('social_auth').filter(id__gte=0)
        for user in users:
            node = {'id': user.id, 'full_name': user.get_full_name()}
            for auth in user.social_auth.all():
                node[auth.provider] = auth.uid
            user_nodes[user.id] = node

        # Create user nodes
        user_cache = {}
        for iid, node in user_nodes.items():
            v = graph.vertices.create(**node)
            user_cache[iid] = v

        # Connections
        connections = GraphConnection.objects.select_related('to_user', 'from_users').all()
        for conn in connections:
            # each connection will require at least 2 nodes (1 from and 1 to)
            # create to node
            if conn.to_user:
                to_vert = user_cache[conn.to_user.id]
            else:
                to_vert = graph.vertices.create({'full_name': conn.full_name, conn.provider: conn.uid})

            # create from node(s)
            for from_user in conn.from_users.all():
                from_vert = user_cache[from_user.id]
                # TODO: this is terrible:
                # we should probably make shared "enum" of these providers (they're also used in social auth)
                edgetype = 'angellist' if conn.provider == 1 else 'linkedin'
                graph.edges.create(from_vert, edgetype, to_vert)
