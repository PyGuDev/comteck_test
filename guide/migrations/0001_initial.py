# Generated by Django 3.2.7 on 2021-09-18 16:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000, verbose_name='Наименование')),
                ('short_name', models.CharField(max_length=300, verbose_name='Короткое наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('version', models.CharField(max_length=300, verbose_name='Версия')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Время начала действия')),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
                'db_table': 'guide',
            },
        ),
        migrations.CreateModel(
            name='GuideItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code_item', models.CharField(max_length=500, verbose_name='Код элемента')),
                ('value_item', models.CharField(max_length=1000, verbose_name='Значение элемента')),
                ('guide_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guide_item', to='guide.guide')),
            ],
            options={
                'verbose_name': 'Элемент справочника',
                'verbose_name_plural': 'Элементы справочника',
                'db_table': 'guide_item',
            },
        ),
    ]