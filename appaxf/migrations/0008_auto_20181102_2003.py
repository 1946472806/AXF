# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-02 12:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appaxf', '0007_auto_20181102_1137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='account',
            new_name='userid',
        ),
    ]
