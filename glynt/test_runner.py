# -*- coding: utf-8 -*-
from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner
from django_jenkins.runner import CITestSuiteRunner

class GlyntAppTestRunner(CITestSuiteRunner):
    def build_suite(self, test_labels, *args, **kwargs):
        # not args passed in
        if not test_labels:
            test_labels = []
            # Remove path info and use only the app "label"
            for app in settings.PROJECT_APPS:
                app_name = app.split('.')[-1]
                test_labels.append(app_name)
            test_labels = tuple(test_labels)

        return super(GlyntAppTestRunner, self).build_suite(test_labels, *args, **kwargs)
