import os
from django.conf import settings

from xhtml2pdf import pisa
import StringIO

import logging
logger = logging.getLogger(__name__)


FORM_GROUPS = {
  'no_steps': [],
}


class UnsupportedMediaPathException(Exception):
    pass


def generate_pdf_template_object(html, link_callback=None):
    """
    Inner function to pass template objects directly instead of passing a filename
    """
    pdf = StringIO.StringIO()
    link_callback = fetch_resources if link_callback is None else link_callback
    pisa.CreatePDF(html.encode("UTF-8"), pdf , encoding='UTF-8',
                   link_callback=link_callback)
    return pdf


def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.
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
                                settings.MEDIA_ROOT, settings.STATIC_ROOT))
    return path

