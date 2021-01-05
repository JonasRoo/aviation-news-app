from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from tags.api.serializers import (
    EntityTypeSerializer,
    EntitySerializer,
    CreateEntityTypeSerializer,
    CreateEntitySerializer,
)
from tags.models import EntityType, Entity, Tag

# V----------------- TYPES -----------------V
class EntityTypesListView(generics.ListAPIView):
    queryset = EntityType.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EntityTypeSerializer


class CreateEntityTypeView(generics.CreateAPIView):
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    serializer_class = CreateEntityTypeSerializer


class UpdateEntityTypeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EntityType.objects.all()
    lookup_field = "pk"
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    serializer_class = EntityTypeSerializer


# V----------------- ENTITIES -----------------V
class EntitiesListView(generics.ListAPIView):
    queryset = Entity.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EntitySerializer


class OwnEntitiesListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EntitySerializer

    def get_queryset(self):
        return Entity.objects.filter(owner=self.request.user)


class CreateEntityView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateEntitySerializer


class UpdateEntityView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    permission_classes = (IsAuthenticated,)
    serializer_class = EntitySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Entity.objects.all()
        return Entity.objects.filter(owner=self.request.user)


# V----------------- TAGS -----------------V