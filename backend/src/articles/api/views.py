from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as df_filters
from rest_framework import filters as rest_filters
from articles.api.pagination import ArticlePagination
from articles.api.serializers import ArticleSerializer, SourceSerializer, ArticleWithTagsSerializer
from articles.api.filters import ArticleFilter, FieldsOnlySearchFilter
from articles.models import Article, Source
from tags.models import ArticleTaggedByUser


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filter_backends = (df_filters.DjangoFilterBackend, FieldsOnlySearchFilter)
    filter_class = ArticleFilter
    # "By default, searches will use case-insensitive partial matches."
    search_class = FieldsOnlySearchFilter
    search_fields = ["title", "description"]


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