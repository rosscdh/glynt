# coding: utf-8
from django.conf import settings
from bulbs.neo4jserver import Graph, Config, NEO4J_URI


conf = Config(getattr(settings, 'NEO4J_URL', NEO4J_URI),
              getattr(settings, 'NEO4J_USERNAME', None),
              getattr(settings, 'NEO4J_PASSWORD', None))

graph = Graph(conf)
