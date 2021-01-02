from rest_framework import serializers
from articles.models import Article, Source


class ArticleSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source="source_internal.name", read_only=True)
    source_icon = serializers.CharField(source="source_internal.icon_url", read_only=True)

    class Meta:
        model = Article
        fields = [
            "source",
            "title",
            "link",
            "date_published",
            "description",
            "image",
            "author",
            "source_name",
            "source_icon",
        ]


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["pk", "name", "base_url", "icon_url"]