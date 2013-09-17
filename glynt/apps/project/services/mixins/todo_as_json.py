# -*- coding: UTF-8 -*-
from glynt.apps.todo.api import ToDoResource


class TodoAsJSONMixin(object):
    """
    Mixin that provides JSON response of the checklist todos
    Currently makes use of TastyPie Resources
    """
    def bundelize(self, resource, request, list_result):
        bundles = []

        for obj in list_result:
            bundle = resource.build_bundle(obj=obj, request=request)
            bundles.append(resource.full_dehydrate(bundle, for_list=True))

        return bundles

    def asJSON(self, request):
        res = ToDoResource()
        request_bundle = res.build_bundle(request=request)

        bundles = self.bundelize(resource=res,
                                 request=request,
                                 list_result=res.obj_get_list(request_bundle))

        return res.serialize(None, bundles, "application/json")
