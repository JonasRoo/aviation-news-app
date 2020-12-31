from rest_framework import serializers
from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["source", "title", "link", "date_published", "description", "image", "author"]


class ArticleSourceOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["source"]