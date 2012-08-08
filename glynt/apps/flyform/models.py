from django.db import models


class FlyForm(models.Model):
    """ Flyform model used to store teh JSON representation of a form """
    body = models.TextField(blank=False,null=False)


