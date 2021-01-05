from django.urls import path
from articles.api.views import (
    ArticleListView,
    SourceListView,
    ArticleWithTagsListView,
    ArticleForTaggingListView,
)

app_name = "articles-api"

urlpatterns = [
    path("list/", ArticleListView.as_view(), name="get-list-of-articles"),
    path("list/tags/", ArticleWithTagsListView.as_view(), name="get-list-of-articles-with-tags"),
    path(
        "list/notTagged/",
        ArticleForTaggingListView.as_view(),
        name="get-list-of-articles-user-has-not-tagget",
    ),
    path("sources/", SourceListView.as_view(), name="get-list-of-all-possible-sources"),
]