# -*- coding: utf-8 -*-
"""
Command to populate Neo4j graph server with relationships
"""
from django.core.management.base import BaseCommand
from optparse import make_option

from django.contrib.auth.models import User

from bunch import Bunch

from bulbs.neo4jserver import Graph
from glynt.apps.graph.models import GraphConnection
from glynt.apps.graph.neo4j import Person, Knows

from glynt.apps.graph.bunches import GlyntPerson

import pdb

import logging
logger = logging.getLogger('lawpal.graph')

graph = Graph()
graph.add_proxy("people", Person)
graph.add_proxy("knows", Knows)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--rebuild',
            dest='rebuild',
            default=False,
            help='Rebuild all relationships'),
    )
    help = 'Adds relationships to neo4j'

    def handle(self, *args, **options):
        if options.get('rebuild', False) != False:
            self.delete_neo4j_entries()

        self.perform()

    def perform(self):
        # Connections
        #g_connections = GraphConnection.objects.select_related('users').filter(provider=GraphConnection.PROVIDERS.linkedin)
        g_connections = GraphConnection.objects.select_related('users').exclude(user=None).filter(provider=GraphConnection.PROVIDERS.linkedin)

        for conn in g_connections:
            # each connection will require at least 2 nodes (1 from and 1 to)
            # create to node

            # @TODO turn this into a transportable bunch
            full_name = '%s %s' % (conn.extra_data.get('firstName'), conn.extra_data.get('lastName'),)

            node = Bunch(GlyntPerson.copy())
            node.update({
                'provider_id': conn.extra_data.get('id'),
                'full_name': full_name,
            })

            from_user = graph.people.index.lookup(provider_id=node.provider_id)
            if from_user is None:
                from_user = graph.people.create(**node)
                logger.info('new neo from_user %s'%from_user)
            else:
                from_user = from_user.next()

            for user in conn.users.all().select_related('graph_connection'):
                to_user = Bunch(GlyntPerson.copy())

                try:
                    provider_id = user.graphconnection_set.all()[0].provider_uid
                except IndexError:
                    provider_id = None

                #if provider_id is not None:
                to_user.update({
                    'glynt_user_id': user.pk,
                    'provider_id': provider_id, 
                    'full_name': user.get_full_name(),
                })

                found_to_user = graph.people.index.lookup(name=to_user.full_name)
                if found_to_user is None:
                    to_user = graph.people.create(**to_user)
                    logger.info('new neo to_user %s'%from_user)
                else:
                    to_user = found_to_user.next()

                # associate the two together
                if from_user.provider_id not in [p.provider_id for p in to_user.outV() or {}]:
                    graph.knows.create(from_user, to_user)
                    logger.info('no relationship found... creating for %s and %s'%(from_user,to_user))

                if to_user.provider_id not in [p.provider_id for p in from_user.outV() or {}]:
                    graph.knows.create(to_user, from_user)
                    logger.info('no relationship found... creating for %s and %s'%(to_user,from_user))

    def delete_neo4j_entries(self):
        if graph.E:
            for e in graph.E:
                graph.edges.delete(e.eid)

        if graph.V:
            for v in graph.V:
                graph.vertices.delete(v.eid)
