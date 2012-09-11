# -*- coding: utf-8 -*-
# tasks to handle the sending of signature invitations
from celery import task

@task()
def send_signature_invite_email(sender):
	# get document info
	# get email
	# process email
	pass