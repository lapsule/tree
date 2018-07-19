# coding:utf-8
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


def get_text(m, name='', default='', fmt='%s'):
    """

    :param m:
    :param name:
    :param default:
    :param fmt:
    :return:
    """
    result = default
    if hasattr(m, name) and getattr(m, name):
        result = getattr(m, name)
        result = fmt % result

    return result


class DjangoModelBase(models.Model):
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = 'Django基础模型'

    def __str__(self):
        return '%s: %s' % (get_text(self, 'id'), get_text(self, 'name')) + get_text(self, 'label', fmt='(%s)')


class LevelBase(DjangoModelBase):
    """
    级别存储通用: 例如 行政级别(省市区),学科级别(门类,学科,专业,方向),职位分类(行业,分类,职位,技能),公司级别
    """
    name = models.CharField('级别名称', max_length=50)
    description = models.CharField('级别描述', max_length=50, null=True, blank=True)
    alias = models.CharField('别名', max_length=50, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return get_text(self, 'name') + get_text(self, 'alias', fmt='(%s)')


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
    LevelModel = AdministrativeLevel

    name = models.CharField('名称(全称)', max_length=50, unique=True)
    alias = models.CharField('别名/简称', max_length=64, null=True, blank=True)
    parent_area = TreeForeignKey('self', verbose_name='上级区域', null=True, blank=True, related_name='children',
                                 on_delete=models.CASCADE)
    common_level = models.ForeignKey(LevelModel, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name='行政级别')

    area_code = models.CharField('电话区号', max_length=64, null=True, blank=True)
    postcode = models.CharField('邮编', max_length=64, null=True, blank=True)
    is_valid = models.BooleanField('是否有效', default=True)

    class Meta:
        db_table = 'area'
        verbose_name = verbose_name_plural = '省/市/区(县)'

    class MPTTMeta:
        parent_attr = 'parent_area'

    def __unicode__(self):
        return get_text(self, 'name', fmt='%s ') + get_text(self, 'common_level', fmt='行政级别:%s')

    def __str__(self):
        return self.__unicode__()


class AreaManager(models.Manager):

    def get_queryset(self):
        current_level = getattr(self.model, 'current_level', '')
        queryset = super(AreaManager, self).get_queryset()
        if current_level:
            queryset = queryset.filter(common_level__name__contains=self.model.current_level)
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
