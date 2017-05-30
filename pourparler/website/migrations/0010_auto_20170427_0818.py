# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-27 08:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20170427_0814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='speaker',
        ),
        migrations.AddField(
            model_name='speech',
            name='speaker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='speaker', to='website.Locutor'),
        ),
    ]
