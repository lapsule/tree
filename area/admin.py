from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Area


class AreaAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'name', 'parent_area', 'level')


admin.site.register(Area, AreaAdmin)
