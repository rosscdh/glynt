from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from taggit.managers import TaggableManager
from categories.models import CategoryBase

from glynt.apps.utils import get_namedtuple_choices
from jsonfield import JSONField

from glynt.apps.document.managers import DocumentManager, PublicDocumentManager, PrivateDocumentManager
from glynt.apps.document.managers import ClientCreatedDocumentManager, PublicClientCreatedDocumentManager, DeletedClientCreatedDocumentManager

class Document(models.Model):
    """ Base Document Class """
    DOC_STATUS = get_namedtuple_choices('DOC_STATUS', (
        (0,'deleted','Deleted'),
        (1,'active','Active'),
        (2,'draft','Draft'),
      
    ))
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=128, blank=False)
    slug = models.SlugField(blank=False, max_length=255)
    summary = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    flyform = models.OneToOneField('flyform.FlyForm')
    doc_status = models.IntegerField(choices=DOC_STATUS.get_choices(), blank=False)
    is_public = models.BooleanField(default=True)
    doc_cats = models.ManyToManyField('DocumentCategory')
    tags = TaggableManager()

    objects = DocumentManager()
    public_objects = PublicDocumentManager()
    private_objects = PrivateDocumentManager()

    class Meta:
      ordering = ['name']

    def __unicode__(self):
      return u'%s' % (self.name, )

    def default_data_as_json(self):
      return json.dumps(self.flyform.defaults)


class DocumentCategory(CategoryBase):
    """
    Basic Categories for document Model
    """
    class Meta:
      verbose_name_plural = 'Document Categories'


class ClientCreatedDocument(models.Model):
    """ Model to store the user generate document based on a source document 
    but associated with a specific creating user """
    owner = models.ForeignKey(User)
    source_document = models.ForeignKey(Document)
    name = models.CharField(max_length=128, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=False, null=True, max_length=255)
    body = models.TextField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    meta_data = JSONField(blank=True, null=True, default={}) # Stores data on num_signatures vs total signatures
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    objects = ClientCreatedDocumentManager()
    active_objects = PublicClientCreatedDocumentManager()
    deleted_objects = DeletedClientCreatedDocumentManager()

    class Meta:
      unique_together = ('slug', 'owner',)

    def __unicode__(self):
      return u'%s' % (self.name)

    @property
    def num_signed(self):
      if 'num_signed' in self.meta_data:
        return int(self.meta_data['num_signed'])
      return 0

    def increment_num_signed(self, signature_id):
      """ Save the number of signers, save the signature_id for uniqueness """
      if 'signers' not in self.meta_data:
        self.meta_data['signers'] = []
      if signature_id not in self.meta_data['signers']:
        self.meta_data['signers'].append(signature_id)
      if 'num_signed' not in self.meta_data:
        self.meta_data['num_signed'] = 0
      self.meta_data['num_signed'] = len(self.meta_data['signers'])
      self.save()

    @property
    def num_invited(self):
      if 'num_invited' in self.meta_data:
        return int(self.meta_data['num_invited'])
      return 0

    def increment_num_invited(self, signature_id):
      """ Save the number of invitees, save the signature_id for uniqueness """
      if 'invitees' not in self.meta_data:
        self.meta_data['invitees'] = []
      if signature_id not in self.meta_data['invitees']:
        self.meta_data['invitees'].append(signature_id)
      if 'num_invited' not in self.meta_data:
        self.meta_data['num_invited'] = 0
      self.meta_data['num_invited'] = len(self.meta_data['invitees'])
      self.save()

    def signatories(self):
      """ Get list of people invited to sign """
      return self.documentsignature_set.all()

    def signed_signatories(self):
      """ Get list of people who have signed """
      return self.documentsignature_set.filter(is_signed=True)

    def get_absolute_url(self):
      return reverse('document:my_view', kwargs={'slug': self.slug})

    @property
    def cookie_name(self):
      return 'glynt-%s' % (self.pk, )

    def diff_source(self):
      return 'Return a diff against the self.source_document.body value'

    def data_as_json(self):
      return json.dumps(self.data)


from glynt.apps.document.signals import *