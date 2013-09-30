# -*- coding: UTF-8 -*-
"""
Mixins that relate to the ToDo app
"""

class NumAttachmentsMixin(object):
    """
    A mixin specifically and only for ToDo ORM objects
    That allows us to store in the .data JSON object the number of attachments
    associated with this ToDo Object
    """
    @property
    def num_attachments(self):
        num = self.data.get('num_attachments', None)
        if num is None:
            num = self.attachments.count()
            self.data['num_attachments'] = num
            self.save(update_fields=['data'])
        return num

    def num_attachments_plus(self):
        num_attachments = self.data.get('num_attachments', 0)
        num_attachments += 1
        self.data['num_attachments'] = num_attachments
        self.save(update_fields=['data'])

    def num_attachments_minus(self):
        num_attachments = self.data.get('num_attachments', 0)
        if num_attachments > 0:
            num_attachments -= 1
            self.data['num_attachments'] = num_attachments
            self.save(update_fields=['data'])