from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from articles.models import Article


class ArticleFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter("date_published")
    source = filters.CharFilter("source", lookup_expr="icontains")

    class Meta:
        model = Article
        fields = ["source"]


class FieldsOnlySearchFilter(drf_filters.SearchFilter):
    def get_search_fields(self, view, request):
        fields = []
        if request.query_params.get("title_only"):
            fields.append("title")
        elif request.query_params.get("description_only"):
            fields.append("description")
        else:
            fields = super().get_search_fields(view, request)

        if request.query_params.get("regex"):
            fields = [f"${field}" for field in fields]
            print(fields)

        return fields