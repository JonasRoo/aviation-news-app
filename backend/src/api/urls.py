from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("articles/", include("articles.api.urls", namespace="articles-api")),
    path("auth/", include("users.api.urls", namespace="auth-api")),
]