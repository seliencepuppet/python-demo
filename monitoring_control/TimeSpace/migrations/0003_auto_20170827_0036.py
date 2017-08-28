# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-27 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSpace', '0002_actionoperation_notifiers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='services',
            field=models.ManyToManyField(blank=True, to='TimeSpace.Service', verbose_name='服务列表'),
        ),
    ]