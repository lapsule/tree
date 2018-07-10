from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import AdministrativeLevel, Area


class AreaAdmin2(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_area', 'level', 'administrative_level')


class AreaAdmin(DjangoMpttAdmin):
    list_display = ('id', 'name', 'parent_area', 'level', 'administrative_level')


admin.site.register(Area, AreaAdmin)
# admin.site.register(Area, AreaAdmin2)

admin.site.register(AdministrativeLevel)
