"""
WSGI config for glynt project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys, site

# Tell wsgi to add the Python site-packages to its path. 
site.addsitedir('/home/stard0g101/.virtualenvs/cartvine_shoppers/lib/python2.6/site-packages')
site.addsitedir('/home/stard0g101/webapps/cartvine_shoppers/glynt')

os.environ['DJANGO_SETTINGS_MODULE'] = 'glynt.settings'

activate_this = os.path.expanduser("~/.virtualenvs/cartvine_shoppers/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

# Calculate the path based on the location of the WSGI script
project = '/home/stard0g101/webapps/cartvine_shoppers/glynt/glynt/'
workspace = os.path.dirname(project)
sys.path.append(workspace)

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
