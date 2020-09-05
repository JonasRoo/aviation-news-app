from django.db import models


class Article(models.Model):
    # REQUIRED FIELDS
    source = models.CharField(max_length=32)
    title = models.CharField(max_length=256)
    link = models.URLField()
    date_published = models.DateTimeField()
    # META DATA
    description = models.CharField(max_length=1024, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=64, blank=True, null=True)
    # INTERNAL
    date_added = models.DateTimeField(auto_now_add=True)
