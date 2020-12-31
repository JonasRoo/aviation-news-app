from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from articles.api.serializers import ArticleSerializer
from articles.models import Article
from rest_framework.permissions import IsAuthenticated


class ArticleListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        source_param = self.request.query_params.get("source")
        if source_param:
            return Article.objects.filter(source__icontains=source_param)

        return Article.objects.all()


class ListAllSourcesView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get(self, request, format=None):
        sources = set([s["source"] for s in Article.objects.values("source").distinct()])
        return Response(sources)