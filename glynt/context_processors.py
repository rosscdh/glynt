from django.conf import settings

PROJECT_NAME = getattr(settings, 'PROJECT_NAME', 'LawPal')
PROJECT_ENVIRONMENT = getattr(settings, 'PROJECT_ENVIRONMENT', 'prod')

def project_info(request):
    return {
      'PROJECT_NAME': PROJECT_NAME
    }


def project_environment(request):
    return {
      'PROJECT_ENVIRONMENT': PROJECT_ENVIRONMENT
    }