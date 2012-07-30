# Make our own testrunner that by default only tests our own apps
from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner


class GlyntAppTestRunner(DjangoTestSuiteRunner):
    def build_suite(self, test_labels, *args, **kwargs):
        PROJECT_APPS = []
        # Remove path info and use only the app "label"
        for app in settings.PROJECT_APPS:
            app_name = app.split('.')[-1]
            PROJECT_APPS.append(app_name)
        return super(GlyntAppTestRunner, self).build_suite(test_labels or PROJECT_APPS, *args, **kwargs)
