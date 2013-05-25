# -*- coding: utf-8 -*-
from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime

class Person(Node):
    element_type = "person"

    linkedin = String(indexed=True)

class Knows(Relationship):
    label = "knows"

    created = DateTime(default=current_datetime, nullable=False)