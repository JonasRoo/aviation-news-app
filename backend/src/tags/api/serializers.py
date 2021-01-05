from rest_framework import serializers
from tags.models import EntityType, Entity, Tag, Alias

# V ---------------- ENTITY TYPES ---------------- V
class EntityTypeSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = EntityType
        fields = ["pk", "owner_name", "name", "color", "date_created", "date_updated"]


class CreateEntityTypeSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EntityType
        fields = ["owner", "name", "color"]

    def validate_name(self, value):
        return value.upper()


# V ---------------- ALIASES ---------------- V
class AliasOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        fields = ["pattern", "is_abbreviation"]


# V ---------------- ENTITIES ---------------- V
class EntitySerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username", read_only=True)
    aliases = AliasOnlySerializer

    class Meta:
        model = Entity
        fields = [
            "pk",
            "owner",
            "entity_type",
            "pattern",
            "name",
            "is_regex",
            "ignore_case",
            "date_created",
            "date_updated",
            "aliases",
        ]

    def validate_pattern(self, value):
        return value.strip()

    def validate_name(self, value):
        return value.strip()


class CreateEntitySerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Entity
        fields = [
            "pk",
            "owner",
            "entity_type",
            "pattern",
            "name",
            "is_regex",
            "ignore_case",
            "date_created",
            "date_updated",
        ]


# V ---------------- TAGS ---------------- V
class TagSerializer(serializers.ModelSerializer):
    entity_pattern = serializers.CharField(source="entity.pattern", read_only=True)
    entity_type_name = serializers.CharField(source="entity.entity_type.name", read_only=True)

    class Meta:
        model = Tag
        fields = [
            "entity_pattern",
            "entity_type_name",
            "text_field_in_article",
            "match_from_index",
            "match_to_index",
        ]
