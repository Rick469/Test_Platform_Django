# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-08-13 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0009_runrecord_sequence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='do_times',
            field=models.IntegerField(default=0, verbose_name='执行次数'),
        ),
    ]
