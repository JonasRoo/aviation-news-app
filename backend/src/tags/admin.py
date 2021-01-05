from django.contrib import admin
from tags.models import EntityType, Entity, Tag, Alias, ArticleTaggedByUser

admin.site.register(EntityType)
admin.site.register(Entity)
admin.site.register(Tag)
admin.site.register(Alias)
admin.site.register(ArticleTaggedByUser)