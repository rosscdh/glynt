from django.conf import settings

PROJECT_NAME = getattr(settings, 'PROJECT_NAME', 'LawPal')

def project_info(request):
    return {
      'PROJECT_NAME': PROJECT_NAME
    }