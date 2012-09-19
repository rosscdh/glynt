import os
from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

import sh

NOTIFICATION_TEMPLATE_DIR = getattr(settings, 'NOTIFICATION_TEMPLATE_DIR', settings.TEMPLATE_DIRS[0])
NOTIFICATION_CREATE_TEMPLATES = getattr(settings, 'NOTIFICATION_CREATE_TEMPLATES', True)
NOTICE_TYPES = (
  ("invite_to_sign_doc", _("Invitation to Sign Document"), _("You have been invited to Sign a Document"), ),
  ("signed_doc", _("Document has been Signed"), _("Your document has been signed"), ),
)

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
      NOTICE_TEMPLATES = ('short.txt', 'full.txt', 'notice.html')#, 'full.html')
      for notice in NOTICE_TYPES:
          name, title, desc = notice
          print "Creating Glynt NoticeType %s" % (name,)
          notification.create_notice_type(name, title, desc)

          # create template folder and files
          template_folder = '%s/notification/%s' % (NOTIFICATION_TEMPLATE_DIR, name,)
          if not os.path.exists(template_folder):
            sh.mkdir("-p", template_folder)
            #print template_folder

          for notice_file in NOTICE_TEMPLATES:
              template_file = '%s/%s' % (template_folder, notice_file,)
              if not os.path.exists(template_file):
                sh.touch(template_file)
                #print template_file


    signals.post_syncdb.connect(create_notice_types, sender=notification)

else:
    print "Skipping creation of NoticeTypes as notification app not found"
