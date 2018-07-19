from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import *


class AreaAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'id',
        'name',
        'alias',
        'parent_area',
        'level',
        'area_code',
        'postcode',
    )


admin.site.register(Area, AreaAdmin)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(District)
admin.site.register(AdministrativeLevel)
