# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.utils.encoding import smart_unicode
from django.contrib.sites.models import Site

from jsonfield import JSONField

from glynt.apps.utils import get_namedtuple_choices
from glynt.apps.document.managers import DocumentTemplateManager, PublicDocumentTemplateManager, PrivateDocumentTemplateManager
from glynt.apps.document.managers import ClientCreatedDocumentManager, PublicClientCreatedDocumentManager, DeletedClientCreatedDocumentManager

from glynt.apps.smoothe.pybars_smoothe import Smoothe

import qrcode

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
    slug = models.SlugField(db_index=True, blank=False, max_length=255)
    acronym = models.CharField(max_length=64, blank=True)
    summary = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    body = models.TextField(blank=True)
    doc_status = models.IntegerField(choices=DOC_STATUS.get_choices(), blank=False, default=DOC_STATUS.draft)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    doc_category = models.ForeignKey('DocumentTemplateCategory', blank=True, null=True)

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


class DocumentTemplateCategory(models.Model):
    """
    Basic Categories for document Model
    """
    name =  models.CharField(max_length=128)
    slug = models.SlugField(db_index=True, unique=True, max_length=128)
    color = models.CharField(max_length=24, null=True)

    class Meta:
      verbose_name_plural = 'Document Categories'

    def __unicode__(self):
        return u'%s' % self.name


class ClientCreatedDocument(models.Model):
    """ Model to store the user generate document based on a source document 
    but associated with a specific creating user """
    owner = models.ForeignKey(User)
    source_document = models.ForeignKey(DocumentTemplate)
    name = models.CharField(max_length=128, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    doc_data = JSONField(blank=True, db_column='data')
    meta_data = JSONField(blank=True, default='{}') # Stores data on num_signatures vs total signatures
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    objects = ClientCreatedDocumentManager()
    active_objects = PublicClientCreatedDocumentManager()
    deleted_objects = DeletedClientCreatedDocumentManager()

    class Meta:
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

    @property
    def meta(self):
        return self.meta_data if type(self.meta_data) is dict else {}

    def get_absolute_url(self):
        return reverse('doc:update_document', kwargs={'pk': self.pk})

    def get_review_url(self):
        return reverse('document:my_review', kwargs={'pk': self.pk})

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

    @property
    def invitees(self):
        return self.documentsignature_set.all()

    @property
    def invitees_as_json(self):
        invitees = []
        for i in self.documentsignature_set.all():
            i.meta_data['pk'] = i.pk
            i.meta_data['is_signed'] = i.is_signed
            invitees.append(i.meta_data)
        return json.dumps(invitees)

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

    class Meta:
      verbose_name_plural = 'Document HTML'

    def render(self):
        logger.info('DocumentHTML render: %s'%(self.pk,))
        #html = markdown.markdown(smart_unicode(self.html)) if self.html else None
        html = smart_unicode(self.html) if self.html else None

        smoothe = Smoothe(source_html=html)

        return smoothe.render(self.document.doc_data)


# import signals, must be at end of file
from glynt.apps.document.signals import save_document_comment_signal, generate_document_body_signal
