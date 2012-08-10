from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

from categories.models import CategoryBase
from glynt.apps.flyform.models import FlyForm

from glynt.apps.utils import get_namedtuple_choices



class Document(models.Model):
    """ Base Document Class """
    DOC_STATUS = get_namedtuple_choices('DOC_STATUS', (
        (0,'deleted','Deleted'),
        (1,'active','Active'),
        (2,'draft','Draft'),
        #(3,'in_review','In-Review'),
        
    ))

    owner = models.ForeignKey(User)
    name = models.CharField(max_length=128,blank=False)
    slug = models.SlugField(blank=False)
    summary = models.TextField(blank=True,null=True)
    body = models.TextField(blank=True,null=True)
    flyform = models.OneToOneField(FlyForm)
    doc_status = models.IntegerField(choices=DOC_STATUS.get_choices(),blank=False)
    is_public = models.BooleanField(default=True)

    doc_cats = models.ManyToManyField('DocumentCategory')

    tags = TaggableManager()

    def __unicode__(self):
        return u'%s' %(self.name)



class DocumentCategory(CategoryBase):
    """
    Basic Categories for document Model
    """
    class Meta:
        verbose_name_plural = 'Document Categories'