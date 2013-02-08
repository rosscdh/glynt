# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.utils.encoding import smart_unicode
from django.contrib.sites.models import Site

from categories.models import CategoryBase
from jsonfield import JSONField

from glynt.apps.utils import get_namedtuple_choices
from glynt.apps.document.managers import DocumentTemplateManager, PublicDocumentTemplateManager, PrivateDocumentTemplateManager
from glynt.apps.document.managers import ClientCreatedDocumentManager, PublicClientCreatedDocumentManager, DeletedClientCreatedDocumentManager

from glynt.apps.smoothe.pybars_smoothe import Smoothe

import qrcode
import markdown


import logging
logger = logging.getLogger('django.request')


class DocumentTemplate(models.Model):
    """ Base Document Class """
    DOC_STATUS = get_namedtuple_choices('DOC_STATUS', (
        (0,'deleted','Deleted'),
        (1,'active','Active'),
        (2,'draft','Draft'),
      
    ))
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=128, blank=False)
    slug = models.SlugField(blank=False, max_length=255)
    acronym = models.CharField(max_length=64, blank=True)
    summary = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    body = models.TextField(blank=True)
    doc_status = models.IntegerField(choices=DOC_STATUS.get_choices(), blank=False, default=DOC_STATUS.draft)
    is_public = models.BooleanField(default=True)
    doc_cats = models.ManyToManyField('DocumentTemplateCategory')

    objects = DocumentTemplateManager()
    public_objects = PublicDocumentTemplateManager()
    private_objects = PrivateDocumentTemplateManager()

    class Meta:
      ordering = ['name']

    def __unicode__(self):
      return u'%s' % (self.name, )

    def get_absolute_url(self):
        return reverse('doc:update_template', kwargs={'pk': self.pk})

    
    @property
    def is_v1_doc(self):
        return True if self.flyform is not None else False

    def default_data_as_json(self):
        return json.dumps({})


class DocumentTemplateCategory(CategoryBase):
    """
    Basic Categories for document Model
    """
    class Meta:
      verbose_name_plural = 'Document Categories'


class ClientCreatedDocument(models.Model):
    """ Model to store the user generate document based on a source document 
    but associated with a specific creating user """
    owner = models.ForeignKey(User)
    source_document = models.ForeignKey(DocumentTemplate)
    name = models.CharField(max_length=128, blank=True, null=True)
    slug = models.SlugField(unique=False, blank=False, null=True, max_length=255)
    body = models.TextField(blank=True, null=True)
    doc_data = JSONField(blank=True, null=True, db_column='data')
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

    @property
    def num_invited(self):
        if self.meta_data and 'num_invited' in self.meta_data:
            return int(self.meta_data['num_invited'])
        return 0

    @property
    def cookie_name(self):
        return 'glynt-%s' % (self.pk, )

    def get_absolute_url(self):
        return reverse('doc:update_document', kwargs={'pk': self.pk})

    def get_review_url(self):
        return reverse('document:my_review', kwargs={'slug': self.slug})

    def qr_code_image(self):
        site = Site.objects.get_current()
        url = '%s%s' % (site.domain, self.get_review_url(),)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=7,
            border=2,
        )

        qr.add_data(url)
        qr.make(fit=True)
        return qr.make_image()

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

    def data_as_json(self):
      return json.dumps(self.doc_data)


class DocumentHTML(models.Model):
    """ 
        The Storage of rendered HTML is managed by this model
        @TODO: Versioning
    """
    document = models.ForeignKey(ClientCreatedDocument)
    html = models.TextField(blank=True)

    def render(self):
        logger.info('DocumentHTML render: %s'%(self.pk,))
        html = markdown.markdown(smart_unicode(self.html)) if self.html else None
        smoothe = Smoothe(source_html=html)

        return smoothe.render(self.document.doc_data)


# import signals, must be at end of file
from glynt.apps.document.signals import save_document_comment_signal, generate_document_body_signal
