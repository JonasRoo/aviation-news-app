import dateutil.parser
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as df_filters
from rest_framework import filters as rest_filters
from articles.api.pagination import ArticlePagination
from articles.api.serializers import ArticleSerializer, SourceSerializer
from articles.api.filters import ArticleFilter, FieldsOnlySearchFilter
from articles.models import Article, Source


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


class SourceListView(generics.ListAPIView):
    queryset = Source.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SourceSerializer