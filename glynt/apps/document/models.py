from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager
from categories.models import CategoryBase

from glynt.apps.utils import get_namedtuple_choices
from jsonfield import JSONField

from managers import DocumentManager, PublicDocumentManager, PrivateDocumentManager
from managers import ClientCreatedDocumentManager, DeletedClientCreatedDocumentManager

class Document(models.Model):
  """ Base Document Class """
  DOC_STATUS = get_namedtuple_choices('DOC_STATUS', (
      (0,'deleted','Deleted'),
      (1,'active','Active'),
      (2,'draft','Draft'),
      
  ))
  owner = models.ForeignKey(User)
  name = models.CharField(max_length=128,blank=False)
  slug = models.SlugField(blank=False)
  summary = models.TextField(blank=True,null=True)
  body = models.TextField(blank=True,null=True)
  flyform = models.OneToOneField('flyform.FlyForm')
  doc_status = models.IntegerField(choices=DOC_STATUS.get_choices(),blank=False)
  is_public = models.BooleanField(default=True)
  doc_cats = models.ManyToManyField('DocumentCategory')
  tags = TaggableManager()

  objects = DocumentManager()
  public_objects = PublicDocumentManager()
  private_objects = PrivateDocumentManager()

  class Meta:
    ordering = ['name']

  def __unicode__(self):
    return u'%s' %(self.name)


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
  slug = models.SlugField(blank=False, null=True)
  body = models.TextField(blank=True, null=True)
  data = JSONField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
  is_deleted = models.BooleanField(default=False)

  objects = ClientCreatedDocumentManager()
  deleted_objects = DeletedClientCreatedDocumentManager()

  def __unicode__(self):
    return u'%s' % (self.name)

  def get_absolute_url(self):
    return reverse('document:my_view', kwargs={'slug': self.slug})

  def diff_source(self):
    return 'Return a diff against the self.source_document.body value'

