from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import *


class AreaAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'name', 'parent_area', 'level')


admin.site.register(Area, AreaAdmin)
admin.site.register(Province)
admin.site.register(City)
