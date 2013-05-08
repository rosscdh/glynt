# -*- coding: utf-8 -*-
import datetime
from haystack import indexes
from models import Lawyer


class LawyerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    full_name = indexes.CharField(model_attr='user__get_full_name')
    role = indexes.CharField(model_attr='position')
    summary = indexes.CharField(model_attr='summary')
    geo_loc = indexes.LocationField(model_attr='geo_loc', null=True)

    def get_model(self):
        return Lawyer

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(user__is_active=True, user__is_superuser=False, user__is_staff=False)