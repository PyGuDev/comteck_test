# Generated by Django 3.2.7 on 2021-09-18 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0002_auto_20210918_1721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guideversion',
            options={'verbose_name': 'Верисия справочника', 'verbose_name_plural': 'Версии справочников'},
        ),
    ]
