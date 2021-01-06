from django.urls import path
from articles.api.views import (
    ArticleListView,
    SourceListView,
    ArticleWithTagsListView,
    ArticleForTaggingListView,
    OnlyHeartedArticlesListView,
    HeartView,
)

app_name = "articles-api"

urlpatterns = [
    path("list/", ArticleListView.as_view(), name="get-list-of-articles"),
    path("list/", ArticleListView.as_view(), name="get-list-of-articles"),
    path(
        "list/hearted/",
        OnlyHeartedArticlesListView.as_view(),
        name="get-list-of-own-hearted-articles",
    ),
    path(
        "list/notTagged/",
        ArticleForTaggingListView.as_view(),
        name="get-list-of-articles-user-has-not-tagget",
    ),
    path("sources/", SourceListView.as_view(), name="get-list-of-all-possible-sources"),
    path("<int:article_id>/heart/", HeartView.as_view(), name="get-list-of-all-possible-sources"),
]