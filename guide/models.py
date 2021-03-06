import uuid

from django.db import models
from django.db.models import QuerySet


class GuideManager(models.Manager):
    def filter_date(self, date: str) -> 'QuerySet[Guide]':
        """
        Фильтрация справочника по дате, получение актуальной версии
        на заданную дату
        :param date: дата в формате YYYY-MM-DD
        """
        return self.get_queryset().filter(guide_version__date_created__gte=date).distinct('name')

    def get_current_version(self, pk: str) -> 'GuideVersion':
        """
        Получение последней версии справочника
        :param pk индефикатор справочника
        """
        return self.get_queryset().get(pk=pk).guide_version.all().order_by('date_created').last()


class Guide(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Наименование', max_length=1000, unique=True)
    short_name = models.CharField('Короткое наименование', max_length=300, unique=True)
    description = models.TextField('Описание', blank=True, null=True)

    objects = GuideManager()

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'
        db_table = 'guide'


class GuideVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guide_id = models.ForeignKey('Guide', on_delete=models.CASCADE, related_name='guide_version',
                                 verbose_name='Справочник')
    title = models.CharField('Название версии', max_length=500)
    date_created = models.DateField('Время начала действия')

    def __str__(self):
        return f'{self.guide_id.name} версия {self.title}'

    class Meta:
        verbose_name = 'Верисия справочника'
        verbose_name_plural = 'Версии справочников'
        db_table = 'guide_version'


class GuideItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_id = models.ForeignKey('GuideVersion', related_name='guide_item',  on_delete=models.CASCADE,
                                  verbose_name='Версия справочника')
    code_item = models.CharField('Код элемента', max_length=500)
    value_item = models.CharField('Значение элемента', max_length=1000)

    def __str__(self):
        return f'Элемент {self.code_item} {self.parent_id}'

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочника'
        db_table = 'guide_item'
