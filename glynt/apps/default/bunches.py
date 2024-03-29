# -*- coding: UTF-8 -*-
"""
"""
from bunch import Bunch
import json
import logging
logger = logging.getLogger('lawpal.services')


class ModelDataBagFieldNotDefinedException(Exception):
    msg = 'The DataBagBunch must have a ._model_databag_field set (field on the model that contains the JSON data)'


class ModelDataBagFieldDoesNotExistException(Exception):
    msg = 'The DataBagBunch _instance must have a ._model_databag_field set'


class BaseDataBagBunch(Bunch):
    _model_databag_field = 'data'
    _model_data_key = None
    instance = None

    def __init__(self, instance, **kwargs):

        if self._model_databag_field is None:
            raise ModelDataBagFieldNotDefinedException

        if instance and not hasattr(instance, self._model_databag_field):
            raise ModelDataBagFieldDoesNotExistException

        self.instance = instance

    def as_json(self):
        return json.dumps(self.data_bag)

    @property
    def data_bag(self):
        # set default value
        _data_bag = {}

        # try to extract the field but return the _data_bag dict if none found
        _data_bag = getattr(self.instance, self._model_databag_field, _data_bag)

        # Return entire databag model field
        return _data_bag

    def save(self, **kwargs):
        # get the current databag
        data = self.data_bag

        if self._model_data_key is not None:
            data = data.get(self._model_data_key, {})

        # set the databag key to the kwargs
        if kwargs is None:
            return None
        else:
            # Update the databag
            data.update(kwargs)

            # set the model field to the updated databag
            setattr(self.instance, self._model_databag_field, data)

            return self.instance.save(update_fields=[self._model_databag_field])
