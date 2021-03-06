# Generated by Django 2.2.7 on 2020-01-13 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_auto_20200113_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoinfo',
            name='pv',
            field=models.PositiveIntegerField(default=1, verbose_name='页面访问量'),
        ),
        migrations.AlterField(
            model_name='videoinfo',
            name='uv',
            field=models.PositiveIntegerField(default=1, verbose_name='独立访客数'),
        ),
    ]
