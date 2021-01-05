from django.urls import path
from articles.api.views import ArticleListView, SourceListView, ArticleWithTagsListView

app_name = "articles-api"

urlpatterns = [
    path("list/", ArticleListView.as_view(), name="get-list-of-articles"),
    path("list/tags/", ArticleWithTagsListView.as_view(), name="get-list-of-articles-with-tags"),
    path("sources/", SourceListView.as_view(), name="get-list-of-all-possible-sources"),
]