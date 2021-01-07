from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as df_filters
from rest_framework import filters as rest_filters
from rest_framework.response import Response
from articles.api.pagination import ArticlePagination
from articles.api.serializers import (
    ArticleSerializer,
    SourceSerializer,
    ArticleWithTagsSerializer,
    ArticleExperimentalSerializer,
)
from articles.api.filters import ArticleFilter, FieldsOnlySearchFilter
from articles.models import Article, Source, Heart
from tags.models import ArticleTaggedByUser


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleExperimentalSerializer
    pagination_class = ArticlePagination
    filter_backends = (df_filters.DjangoFilterBackend, FieldsOnlySearchFilter)
    filter_class = ArticleFilter
    # "By default, searches will use case-insensitive partial matches."
    search_class = FieldsOnlySearchFilter
    search_fields = ["title", "description"]


class OnlyHeartedArticlesListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleExperimentalSerializer
    pagination_class = ArticlePagination
    filter_backends = (df_filters.DjangoFilterBackend, FieldsOnlySearchFilter)
    filter_class = ArticleFilter
    # "By default, searches will use case-insensitive partial matches."
    search_class = FieldsOnlySearchFilter
    search_fields = ["title", "description"]

    def get_queryset(self):
        user_hearts = Heart.objects.filter(user=self.request.user).values("article")
        return Article.objects.filter(pk__in=user_hearts)


class ArticleWithTagsListView(generics.ListAPIView):
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleWithTagsSerializer
    pagination_class = ArticlePagination
    filter_backends = (df_filters.DjangoFilterBackend, FieldsOnlySearchFilter)
    filter_class = ArticleFilter
    # "By default, searches will use case-insensitive partial matches."
    search_class = FieldsOnlySearchFilter
    search_fields = ["title", "description"]


class ArticleForTaggingListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleWithTagsSerializer
    pagination_class = ArticlePagination
    filter_backends = (df_filters.DjangoFilterBackend, FieldsOnlySearchFilter)
    filter_class = ArticleFilter
    # "By default, searches will use case-insensitive partial matches."
    search_class = FieldsOnlySearchFilter
    search_fields = ["title", "description"]

    def get_queryset(self):
        user = self.request.user
        user_has_already_tagged = ArticleTaggedByUser.objects.filter(user=user)
        return Article.objects.exclude(pk__in=user_has_already_tagged)


class SourceListView(generics.ListAPIView):
    queryset = Source.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SourceSerializer


class HeartView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, article_id, format=None):
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return Response({"error": f"Article with ID {article_id} does not exist!"})
        user = self.request.user
        try:
            heart = Heart.objects.get(user=user, article=article)
            heart.delete()
            return Response({"message": f"Successfully unhearted article!"})
        except Heart.DoesNotExist:
            heart = Heart.objects.create(user=user, article=article)
            return Response({"message": f"Successfully hearted article!"})