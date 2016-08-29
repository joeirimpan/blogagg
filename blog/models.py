from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=200, null=True)
    url = models.URLField()
    name = models.CharField(max_length=200)


class Article(models.Model):
    blog = models.ForeignKey(Blog, null=True)
    title = models.CharField(max_length=200, null=True)
    url = models.URLField()
    description = models.TextField()
    # publication_date = models.DateTimeField()
