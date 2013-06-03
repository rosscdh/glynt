# encoding: utf-8

from postman.utils import notification, email


def notify_user(object, action):
    """Notify a user."""
    if action == 'rejection':
        user = object.sender
        label = 'postman_rejection'
    elif action == 'acceptance':
        user = object.recipient
        parent = object.parent
        label = 'postman_reply' if (parent and parent.sender_id == object.recipient_id) else 'postman_message'
    elif action == 'engagement_message':
        user = object.recipient
        parent = object.parent
        label = 'postman_engagement'
    else:
        return
    if notification:
        # the context key 'message' is already used in django-notification/models.py/send_now() (v0.2.0)
        notification.send(users=[user], label=label, extra_context={'pm_message': object, 'pm_action': action})
    else:
        if not DISABLE_USER_EMAILING and user.email and user.is_active:
            email('postman/email_user_subject.txt', 'postman/email_user.txt', [user.email], object, action)
