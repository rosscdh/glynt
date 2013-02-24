from django.conf import settings

import os
import logging
logger = logging.getLogger('django.request')


class UnsupportedMediaPathException(Exception):
    pass


def fetch_resources(uri):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        filename = uri.replace(settings.STATIC_URL, "")
        path = os.path.join(settings.STATIC_ROOT, filename)
        if not os.path.exists(path):
            for d in settings.STATICFILES_DIRS:
                path = os.path.join(d, filename)
                if os.path.exists(path):
                    break
    else:
        raise UnsupportedMediaPathException(
                                'media urls must start with %s or %s' % (
                                settings.MEDIA_URL, settings.STATIC_URL))
    return path

