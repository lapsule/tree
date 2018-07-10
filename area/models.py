# coding:utf-8
from django.db import models
from mptt.models import MPTTModel


class AdministrativeLevel(models.Model):
    name = models.CharField('行政级别', max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class Area(MPTTModel):
    name = models.CharField('名称', max_length=50, unique=True)
    parent_area = models.ForeignKey('self', verbose_name='上级区域', null=True, blank=True, related_name='children',
                                    on_delete=models.PROTECT)
    administrative_level = models.ForeignKey(AdministrativeLevel, on_delete=models.PROTECT, null=True,
                                             verbose_name='行政级别')

    class Meta:
        db_table = 'area'
        verbose_name = verbose_name_plural = '省/市/地区(县)'

    class MPTTMeta:
        parent_attr = 'parent_area'

    def __unicode__(self):
        return "{} ({})".format(self.name, self.administrative_level.name if self.administrative_level else '')

    def __str__(self):
        return self.__unicode__()
