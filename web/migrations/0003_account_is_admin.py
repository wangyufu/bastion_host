# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-10 03:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_remove_account_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]