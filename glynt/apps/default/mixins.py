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
            attrs.update({
                'data-ng-model': field,
                'data-ng-init': self.fields[field].initial if self.fields[field].initial is not None else '',
            })

            self.fields[field].widget.attrs = attrs