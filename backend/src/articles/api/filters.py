from django_filters import rest_framework as filters, BaseInFilter, NumberFilter
from django_filters import Filter
from django_filters.fields import Lookup
from rest_framework import filters as drf_filters
from articles.models import Article


class NumberInFilter(BaseInFilter, NumberFilter):
    pass

class ArticleFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter("date_published", label="date")
    sources = NumberInFilter(field_name="source_internal__pk", lookup_expr="in")

    class Meta:
        model = Article
        fields = ["sources", "date"]


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