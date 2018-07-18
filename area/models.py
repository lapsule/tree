# coding:utf-8
from django.db import models
from mptt.models import MPTTModel


class AreaManager(models.Manager):

    def get_queryset(self):
        current_level = getattr(self.model, 'current_level', '')
        queryset = super(AreaManager, self).get_queryset()
        if current_level:
            queryset = queryset.filter(name__contains=current_level)
        return queryset


class Area(MPTTModel):
    """
    地区级联存储

    current_level 默认为空,当为: 省,时,区,县筛选出名字对应的地区,更好的方式是特定字段存储,用特定进行筛选
    """
    current_level = ''

    name = models.CharField('名称', max_length=50, unique=True)
    parent_area = models.ForeignKey('self', verbose_name='上级区域', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='children')

    class Meta:
        db_table = 'area'
        verbose_name = verbose_name_plural = '省/市/地区(县)'

    class MPTTMeta:
        parent_attr = 'parent_area'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


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


# provinces = Province.objects.all()
# print(provinces, provinces.count())
