# -*- coding: UTF-8 -*-


class AngularAttribsFormFieldsMixin(object):
    """
    Mixin that will add the angular attribs required
    to drive the models
    """
    def __init__(self, *args, **kwargs):
        super(AngularAttribsFormFieldsMixin, self).__init__(*args, **kwargs)

        # Append the ng-model and ng-init
        for field in self.fields:

            attrs = getattr(self.fields[field].widget, 'attrs', {})

            data_ng_init = self.initial[field] if field in self.initial and self.initial[field] is not None else self.fields[field].initial if self.fields[field].initial is not None else ''
            data_ng_init_field = "field='{data_ng_init}'".format(data_ng_init=data_ng_init) if data_ng_init not in [None, ''] else ''

            attrs.update({
                'data-ng-model': field,
                # use the form.initial before trying the field.initial otherwise its jsut an empty string
                'data-ng-init': data_ng_init_field,
            })

            self.fields[field].widget.attrs = attrs