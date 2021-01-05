from django.urls import path
from tags.api.views import (
    EntityTypesListView,
    CreateEntityTypeView,
    UpdateEntityTypeView,
    EntitiesListView,
    OwnEntitiesListView,
    CreateEntityView,
    UpdateEntityView,
)

app_name = "tags-api"

urlpatterns = [
    # entity-types
    path("types/list/", EntityTypesListView.as_view(), name="list-available-entity-types"),
    path("types/create/", CreateEntityTypeView.as_view(), name="create-new-entity-type"),
    path(
        "types/<int:pk>/update/",
        UpdateEntityTypeView.as_view(),
        name="update-or-destroy-entity-type",
    ),
    # entities
    path("entities/list/own/", OwnEntitiesListView.as_view(), name="list-own-entities"),
    path("entities/list/", EntitiesListView.as_view(), name="list-entities"),
    path("entities/create/", CreateEntityView.as_view(), name="create-new-entity"),
    path(
        "entities/<int:pk>/update/",
        UpdateEntityView.as_view(),
        name="update-or-destroy-entity",
    ),
    # tags
]