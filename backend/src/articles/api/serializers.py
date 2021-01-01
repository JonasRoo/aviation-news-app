from rest_framework import serializers
from articles.models import Article, Source


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["source", "title", "link", "date_published", "description", "image", "author"]


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["pk", "name", "base_url", "icon_url"]