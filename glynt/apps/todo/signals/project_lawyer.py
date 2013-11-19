# -*- coding: utf-8 -*-
"""
Project Lawyer Signals
Should probably go in project app
"""
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from glynt.apps.project.models import ProjectLawyer

import logging
logger = logging.getLogger('django.request')


@receiver(post_save, sender=ProjectLawyer, dispatch_uid='projectlawyer.assigned')
def projectlawyer_assigned(sender, **kwargs):
    """
    On save of a ProjectLawyer instance where the status is ASSIGNED
    Set all the todos.user of that project to the lawyer
    excluding those todos that already have a user
    """
    instance = kwargs.get('instance')

    if instance.status == ProjectLawyer._LAWYER_STATUS.assigned:
        logger.info('Assigned Lawyer: {lawyer} to Project: {project}'.format(lawyer=instance.lawyer, project=instance.project))
        instance.project.todo_set.filter(user=None).update(user=instance.lawyer.user)


@receiver(post_delete, sender=ProjectLawyer, dispatch_uid='projectlawyer.delete')
def projectlawyer_deleted(sender, **kwargs):
    """
    On delete of a ProjectLawyer instance
    Set all the todos.user of that project to None
    where those todos.user == instance.lawyer
    """
    instance = kwargs.get('instance')
    try:
        logger.info('Deleted Lawyer: {lawyer} to Project: {project}'.format(lawyer=instance.lawyer, project=instance.project))
        instance.project.todo_set.filter(user=instance.lawyer.user).update(user=None)
    except:
        pass