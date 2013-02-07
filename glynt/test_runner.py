# Make our own testrunner that by default only tests our own apps
import os
from django.conf import settings

# from django_behave.runner import DjangoBehaveTestSuiteRunner
#from django_nose import NoseTestSuiteRunner
from django.test.simple import DjangoTestSuiteRunner


os.getenv('DJANGO_SETTINGS_MODULE', 'settings')


class GlyntAppTestRunner(DjangoTestSuiteRunner):
    def build_suite(self, test_labels, *args, **kwargs):
        PROJECT_APPS = []
        # Remove path info and use only the app "label"
        for app in settings.PROJECT_APPS:
            app_name = app.split('.')[-1]
            PROJECT_APPS.append(app_name)
        return super(GlyntAppTestRunner, self).build_suite(test_labels or PROJECT_APPS, *args, **kwargs)
