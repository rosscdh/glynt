# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.utils.safestring import mark_safe

from taggit.managers import TaggableManager
from categories.models import CategoryBase
from jsonfield import JSONField

from glynt.apps.utils import get_namedtuple_choices
from glynt.apps.document.managers import DocumentManager, PublicDocumentManager, PrivateDocumentManager
from glynt.apps.document.managers import ClientCreatedDocumentManager, PublicClientCreatedDocumentManager, DeletedClientCreatedDocumentManager

from glynt.pybars_plus import PybarsPlus
import markdown
import qrcode


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
    flyform = models.OneToOneField('flyform.FlyForm', blank=True, null=True, db_index=True)
    doc_status = models.IntegerField(choices=DOC_STATUS.get_choices(), blank=False, db_index=True)
    is_public = models.BooleanField(default=True, db_index=True)
    doc_cats = models.ManyToManyField('DocumentCategory')
    tags = TaggableManager()

    objects = DocumentManager()
    public_objects = PublicDocumentManager()
    private_objects = PrivateDocumentManager()

    class Meta:
      ordering = ['name']

    def __unicode__(self):
      return u'%s' % (self.name, )

    @property
    def is_v1_doc(self):
        return True if self.flyform is not None else False

    def default_data_as_json(self):
      return json.dumps(self.flyform.defaults) if self.is_v1_doc is True else json.dumps({'document_name': self.name, 'document_summary': self.summary})


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
    slug = models.SlugField(unique=False, blank=False, null=True, max_length=255)
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
      ordering = ['-created_at', 'name']

    def __unicode__(self):
      return u'%s' % (self.name)

    @property
    def num_signed(self):
      if self.meta_data and 'num_signed' in self.meta_data:
        return int(self.meta_data['num_signed'])
      return 0

    def get_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.get_absolute_url())
        qr.make(fit=True)
        return qr.make_image()

    def rendered_body(self):
        """ Merge with the base set of fields"""
        data = [(k, '') for k in self.source_document.flyform.flyform_fields]
        if type(self.data) is dict:
            data = dict(data + [(k, v) for k, v in self.data.iteritems()])
        data['document_title'] = self.name if 'document_title' in data else ''

        pybars_plus = PybarsPlus(self.body)
        #return mark_safe(markdown.markdown(pybars_plus.render(data)))
        return mark_safe(pybars_plus.render(data))

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
      if self.meta_data and 'num_invited' in self.meta_data:
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
        if self.source_document.is_v1_doc is True:
            return reverse('document:my_view', kwargs={'slug': self.slug})
        else:
            return reverse('doc:my_view', kwargs={'slug': self.slug})

    @property
    def cookie_name(self):
      return 'glynt-%s' % (self.pk, )

    def diff_source(self):
      return 'Return a diff against the self.source_document.body value'

    def data_as_json(self):
      return json.dumps(self.data)

# import signals
from glynt.apps.document.signals import *
