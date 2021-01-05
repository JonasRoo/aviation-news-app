from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from articles.models import Article

UpperCaseValidator = RegexValidator(
    "^[A-Z\-_]+", "Only upper-case letters, underscores and dashes are allowed!"
)


class EntityType(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=32, validators=(UpperCaseValidator,))
    color = models.CharField(max_length=32, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Entity(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    entity_type = models.ForeignKey(EntityType, related_name="entities", on_delete=models.CASCADE)
    pattern = models.CharField(max_length=200)
    name = models.CharField(max_length=200, blank=True)
    is_regex = models.BooleanField(blank=True, null=True, default=False)
    ignore_case = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "pattern",
            "entity_type",
        )

    def __str__(self):
        return f"{self.name} <{self.pattern}> (regex={self.is_regex})"


class Alias(models.Model):
    entity = models.ForeignKey(Entity, related_name="aliases", on_delete=models.CASCADE)
    pattern = models.CharField(max_length=200)
    is_abbreviation = models.BooleanField(default=False)


class Tag(models.Model):
    ARTICLE_TEXT_FIELD_CHOICES = (
        ("T", "Title"),
        ("D", "Description"),
    )
    article = models.ForeignKey(Article, related_name="tags", on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    text_field_in_article = models.CharField(max_length=1, choices=ARTICLE_TEXT_FIELD_CHOICES)
    match_from_index = models.IntegerField()
    match_to_index = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)