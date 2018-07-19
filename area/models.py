# coding:utf-8
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from data_layer.mysql.base.models import LevelBase, get_text


class AdministrativeLevel(LevelBase, models.Model):
    """
    行政级别: 省(直辖市,自治区,州??)/市/区(县)/镇(乡)/村
    """

    class Meta:
        db_table = 'administrative_level'
        verbose_name = verbose_name_plural = "行政级别"
        app_label = 'area'


class Area(MPTTModel):
    """
    地区级联存储

    current_level 默认为空,当为: 省,时,区,县筛选出名字对应的地区,更好的方式是特定字段存储,用特定进行筛选
    """
    current_level = ''

    name = models.CharField('名称(全称)', max_length=50, unique=True)
    alias = models.CharField('别名/简称', max_length=64, null=True, blank=True)
    area_code = models.CharField('电话区号', max_length=64, null=True, blank=True)
    postcode = models.CharField('邮编', max_length=64, null=True, blank=True)
    is_valid = models.BooleanField('是否有效', default=True)
    parent_area = TreeForeignKey('self', verbose_name='上级区域', null=True, blank=True, related_name='children',
                                 on_delete=models.CASCADE)
    administrative_level = models.ForeignKey(AdministrativeLevel, on_delete=models.CASCADE, null=True, blank=True,
                                             verbose_name='行政级别')

    class Meta:
        db_table = 'area'
        verbose_name = verbose_name_plural = '省/市/区(县)'

    class MPTTMeta:
        parent_attr = 'parent_area'

    def __unicode__(self):
        return get_text(self, 'name', fmt='%s ') + get_text(self, 'administrative_level', fmt='行政级别:%s')

    def __str__(self):
        return self.__unicode__()


class AreaManager(models.Manager):

    def get_queryset(self):
        current_level = getattr(self.model, 'current_level', '')
        queryset = super(AreaManager, self).get_queryset()
        if current_level:
            queryset = queryset.filter(administrative_level__name__contains=self.model.current_level)
        return queryset


class Province(Area):
    current_level = '省'

    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = '省'

    objects = AreaManager()


class City(Area):
    current_level = '市'

    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = '市'

    objects = AreaManager()


class District(Area):
    current_level = '县'

    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = '区/县'

    objects = AreaManager()

# provinces = Province.objects.all()
# print(provinces, provinces.count())
