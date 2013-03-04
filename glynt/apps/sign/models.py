from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from jsonfield import JSONField

from glynt.apps.document.models import ClientCreatedDocument

from signpad2image.signpad2image import s2ib


class DocumentSignature(models.Model):
    """ Model to store a users signature of a document
    signatures are stored as JSON value
    http://thomasjbradley.ca/lab/signature-pad/#database
    """
    document = models.ForeignKey(ClientCreatedDocument)
    key_hash = models.CharField(blank=False, max_length=32, unique=True)
    hash_data = models.CharField(blank=False, max_length=255)
    user = models.ForeignKey(User, blank=True, null=True)
    signature = JSONField(blank=True, null=True)
    meta_data = JSONField(blank=True, null=True, default={})
    is_signed = models.BooleanField(default=False)
    date_invited = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_signed = models.DateTimeField(blank=True, null=True, auto_now=False, auto_now_add=False)

    class Meta:
        ordering = ['-date_invited', '-date_signed']

    def __unicode__(self):
        return u'%s' % (self.key_hash,)

    def get_absolute_url(self):
        return reverse('sign:default', kwargs={'pk': self.document.pk, 'hash': self.key_hash})

    @property
    def signature_pic_url(self):
        return reverse('sign:signature_pic', kwargs={'pk': self.document.pk, 'hash': self.key_hash})

    def signature_as_string(self):
        return json.dumps(self.signature)

    def signature_as_image(self):
        try:
            return s2ib(self.signature_as_string(), wh=(198,120), pincolor=(0,0,0))
        except:
            return s2ib(False, wh=(198,120), pincolor=(0,0,0))

    @property
    def signee_name(self):
        return u'%s' % self.meta_data.get('to_name', None)

    @property
    def signee_email(self):
        return u'%s' % self.meta_data.get('to_email', None)

    @property
    def signee_ip_address(self):
        return u'%s' % self.meta_data.get('signee_ip', None)


# import signals, must be at end of file
from glynt.apps.sign.signals import save_document_signature_signal
