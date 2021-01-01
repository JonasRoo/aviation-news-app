from django.db import models


class Source(models.Model):
    base_url = models.URLField(max_length=128)
    icon_url = models.URLField(max_length=512, blank=True, null=True)


class Article(models.Model):
    # REQUIRED FIELDS
    source_internal = models.ForeignKey(to="Source", on_delete=models.SET_NULL, null=True)
    source = models.URLField()
    title = models.CharField(max_length=256)
    link = models.URLField(max_length=512)
    date_published = models.DateTimeField()
    # META DATA
    description = models.CharField(max_length=1024, blank=True, null=True)
    image = models.URLField(blank=True, null=True, max_length=512)
    author = models.CharField(max_length=64, blank=True, null=True)
    # INTERNAL
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("source", "title", "link")
        ordering = ("-date_published",)

    def __str__(self):
        return f"{self.source} published {{{self.title}}} on {self.date_published.date()}"
