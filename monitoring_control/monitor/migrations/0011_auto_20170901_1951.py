# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-01 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0010_auto_20170831_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='services',
            field=models.ManyToManyField(blank=True, to='monitor.Service', verbose_name='服务列表'),
        ),
        migrations.AlterField(
            model_name='template',
            name='triggers',
            field=models.ManyToManyField(blank=True, to='monitor.Trigger', verbose_name='触发器列表'),
        ),
    ]
