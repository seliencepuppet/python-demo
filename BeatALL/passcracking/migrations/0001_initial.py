# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-30 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordCrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ssh_crack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.GenericIPAddressField(verbose_name='目标ip地址')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='目标命名')),
            ],
        ),
        migrations.CreateModel(
            name='ssh_crack_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=50, verbose_name='破解的密码')),
                ('ssh_crack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passcracking.ssh_crack')),
            ],
        ),
    ]
