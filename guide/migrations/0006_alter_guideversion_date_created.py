# Generated by Django 3.2.7 on 2021-09-19 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0005_alter_guideversion_guide_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guideversion',
            name='date_created',
            field=models.DateField(verbose_name='Время начала действия'),
        ),
    ]
