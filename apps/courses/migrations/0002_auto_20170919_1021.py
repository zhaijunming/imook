# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-19 10:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': ('课程',), 'verbose_name_plural': ('课程',)},
        ),
        migrations.AlterModelOptions(
            name='courseresource',
            options={'verbose_name': ('课程资源',), 'verbose_name_plural': ('课程资源',)},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': ('章节',), 'verbose_name_plural': ('章节',)},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': ('视频',), 'verbose_name_plural': ('视频',)},
        ),
    ]
