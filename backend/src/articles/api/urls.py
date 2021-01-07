from django.urls import path
from django.views.decorators.cache import cache_page, cache_control
from articles.api.views import (
    ArticleListView,
    SourceListView,
    ArticleWithTagsListView,
    ArticleForTaggingListView,
    OnlyHeartedArticlesListView,
    HeartView,
)

app_name = "articles-api"


def cache_private(func, *cache_page_args, **cache_kwargs):
    return cache_page(cache_page_args, **cache_kwargs)(cache_control(private=True)(func))


urlpatterns = [
    path(
        "list/",
        # only using 10 seoncs here because of the "heart" endpoint
        ArticleListView.as_view(),
        name="get-list-of-all-articles-without-tags",
    ),
    path(
        "list/hearted/",
        OnlyHeartedArticlesListView.as_view(),
        name="get-list-of-own-hearted-articles",
    ),
    path(
        "list/notTagged/",
        ArticleForTaggingListView.as_view(),
        name="get-list-of-articles-user-has-not-tagged",
    ),
    path(
        "sources/",
        cache_private(SourceListView.as_view(), 60 * 60),
        name="get-list-of-all-possible-sources",
    ),
    path(
        "<int:article_id>/heart/",
        HeartView.as_view(),
        name="get-list-of-all-possible-sources",
    ),
]