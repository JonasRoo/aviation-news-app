import dateutil.parser
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from articles.api.pagination import ArticlePagination
from articles.api.serializers import ArticleSerializer
from articles.models import Article


class ArticleListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    def get_queryset(self):
        qs = Article.objects.all()

        # filtering by url params
        source_param = self.request.query_params.get("source")
        if source_param:
            qs = qs.filter(source__icontains=source_param)

        title_param = self.request.query_params.get("title")
        if title_param:
            qs = qs.filter(title__icontains=title_param)

        date_from, date_to = (
            self.request.query_params.get("from"),
            self.request.query_params.get("to"),
        )
        if date_from:
            date_from = dateutil.parser.parse(date_from)
            qs = qs.filter(date_published__gte=date_from)
        if date_to:
            date_to = dateutil.parser.parse(date_to)
            qs = qs.filter(date_published__lte=date_to)

        return qs


class ListAllSourcesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        sources = set([s["source"] for s in Article.objects.values("source").distinct()])
        return Response(sources)