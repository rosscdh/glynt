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
                # use the form.initial before trying the field.initial otherwise its jsut an empty string
                'data-ng-init': self.initial[field] if field in self.initial and self.initial[field] is not None else self.fields[field].initial if self.fields[field].initial is not None else '',
            })

            self.fields[field].widget.attrs = attrs