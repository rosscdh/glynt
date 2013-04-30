# -*- coding: utf-8 -*-
from neo4django.db import models


class Person(models.NodeModel):
    name = models.StringProperty()
    is_lawyer = models.BooleanProperty(indexed=True)

    contacts = models.Relationship('self', rel_type='connected_with')