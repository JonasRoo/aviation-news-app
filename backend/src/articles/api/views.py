import dateutil.parser
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as df_filters
from rest_framework import filters as rest_filters
from articles.api.pagination import ArticlePagination
from articles.api.serializers import ArticleSerializer
from articles.api.filters import ArticleFilter, FieldsOnlySearchFilter
from articles.models import Article


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


class ListAllSourcesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        # for some reason, .values("source").distinct() returns ~10k values,
        # even though there's only 3 sources (at time of writing).
        # (I assume this has to do with "source" being a `models.URLField`)
        # Hence the "ugly" set-casting
        sources = set([s["source"] for s in Article.objects.values("source").distinct()])
        return Response(sources)