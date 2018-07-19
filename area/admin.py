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


class CommonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'alias',
        'parent_area',
        'level',
        'area_code',
        'postcode',
    )


admin.site.register(Area, AreaAdmin)
admin.site.register(Province, CommonAdmin)
admin.site.register(City, CommonAdmin)
admin.site.register(District, CommonAdmin)
admin.site.register(AdministrativeLevel)
