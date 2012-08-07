from django.conf import settings

PROJECT_NAME = getattr(settings, PROJECT_NAME, 'MyLawyer')

def project_info(request):
    return {
    	'project_name': PROJECT_NAME
    }