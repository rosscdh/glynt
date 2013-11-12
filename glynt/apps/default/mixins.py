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
            })

            self.fields[field].widget.attrs = attrs


class ChangeUserDetailsMixin(object):
    """ Mixin used to change the users' details"""
    data = []
    user = None

    def update_user(self):
        if not self.user:
            raise Exception('No User was provided for this object')

        fields_to_update = []

        if self.data.get('first_name', None) is not None:
            self.user.first_name = self.data.get('first_name')
            fields_to_update.append('first_name')

        if self.data.get('last_name', None) is not None:
            self.user.last_name = self.data.get('last_name')
            fields_to_update.append('last_name')

        if self.data.get('email', None) is not None:
            self.user.email = self.data.get('email')
            fields_to_update.append('email')

        # update the user only if changes happened
        if len(fields_to_update) > 0:
            self.user.save(update_fields=fields_to_update)
