from django.urls import path
from articles.api.views import ArticleListView, SourceListView

app_name = "api-articles"

urlpatterns = [
    path("list/", ArticleListView.as_view(), name="get-list-of-articles"),
    path("sources/", SourceListView.as_view(), name="get-list-of-all-possible-sources"),
]