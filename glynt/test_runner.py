# Make our own testrunner that by default only tests our own apps
import os
import sys
from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner
#from django_nose import NoseTestSuiteRunner

os.getenv('DJANGO_SETTINGS_MODULE', 'settings')


class GlyntAppTestRunner(DjangoTestSuiteRunner):
    def build_suite(self, test_labels, *args, **kwargs):
        PROJECT_APPS = sys.argv[2:]

        # not args passed in
        if not PROJECT_APPS:
            # Remove path info and use only the app "label"
            for app in settings.PROJECT_APPS:
                app_name = app.split('.')[-1]
                PROJECT_APPS.append(app_name)

        return super(GlyntAppTestRunner, self).build_suite(test_labels or PROJECT_APPS, *args, **kwargs)
