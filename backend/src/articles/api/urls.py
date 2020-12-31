from django.urls import path
from articles.api.views import ArticleListView, ListAllSourcesView

app_name = "api-articles"

urlpatterns = [
    path("list/", ArticleListView.as_view(), name="get-list-of-articles"),
    path("sources/", ListAllSourcesView.as_view(), name="get-list-of-all-possible-sources"),
]