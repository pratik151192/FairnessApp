# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_uservalues_image_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservalues',
            name='firstLogin',
            field=models.BooleanField(default=False),
        ),
    ]
