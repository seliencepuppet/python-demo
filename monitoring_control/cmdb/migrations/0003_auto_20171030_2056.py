# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-30 20:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0002_auto_20171030_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='contract',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='contract',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='contract',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='disk',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='disk',
            name='update_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='事件时间'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
