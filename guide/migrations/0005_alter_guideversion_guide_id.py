# Generated by Django 3.2.7 on 2021-09-18 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0004_auto_20210918_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guideversion',
            name='guide_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guide_version', to='guide.guide', verbose_name='Справочник'),
        ),
    ]
