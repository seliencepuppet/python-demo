# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-28 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSpace', '0006_auto_20170828_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='TimeSpace.HostGroup', verbose_name='主机组'),
        ),
        migrations.AlterField(
            model_name='host',
            name='templates',
            field=models.ManyToManyField(blank=True, to='TimeSpace.Template', verbose_name='默认模板'),
        ),
    ]
