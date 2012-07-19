from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Document(models.Model):
    DOC_STATUS = (
        (0,'Deleted'),
        (1,'Draft'),
        (2,'In-Review'),
        (3,'Active'),
    )

    owner = models.ForeignKey(User)
    name = models.CharField(max_length=128,blank=False)
    slug = models.SlugField(blank=False)
    summary = models.TextField(blank=True,null=True)
    body = models.TextField(blank=True,null=True)
    doc_status = models.IntegerField(choices=DOC_STATUS,blank=False)
    is_public = models.BooleanField(default=True)

    tags = TaggableManager()

    def __unicode__(self):
        return u'%s' %(self.name)