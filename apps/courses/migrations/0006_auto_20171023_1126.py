# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-23 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_categort'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(default='', max_length=100, verbose_name='章节链接'),
        ),
        migrations.AlterField(
            model_name='course',
            name='categort',
            field=models.CharField(default='后端', max_length=20, verbose_name='课程类别'),
        ),
    ]