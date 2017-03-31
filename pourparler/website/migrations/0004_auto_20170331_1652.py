# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-31 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20170331_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='locutor',
            name='friends',
            field=models.ManyToManyField(to='website.Locutor'),
        ),
        migrations.AlterField(
            model_name='locutor',
            name='id',
            field=models.CharField(db_index=True, max_length=14, primary_key=True, serialize=False, unique=True),
        ),
    ]
