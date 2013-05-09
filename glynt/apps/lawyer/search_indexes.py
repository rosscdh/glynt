# -*- coding: utf-8 -*-
import datetime
from haystack import indexes
from models import Lawyer


class LawyerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    user_pk = indexes.CharField(model_attr='user__pk')
    lawyer_pk = indexes.CharField(model_attr='pk')
    username = indexes.CharField(model_attr='user__username')
    full_name = indexes.CharField(model_attr='user__get_full_name')
    profile_photo = indexes.CharField(model_attr='profile_photo')
    position = indexes.CharField(model_attr='position')
    firm_name = indexes.CharField(model_attr='firm_name', null=True)
    summary = indexes.CharField(model_attr='summary')
    geo_loc = indexes.LocationField(model_attr='geo_loc', null=True)

    def get_model(self):
        return Lawyer

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().approved.all()