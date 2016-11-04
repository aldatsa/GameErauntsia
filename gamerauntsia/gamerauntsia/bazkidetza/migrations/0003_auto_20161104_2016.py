# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-04 19:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0010_auto_20160105_1307'),
        ('bazkidetza', '0002_auto_20161104_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eskaintza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('izena', models.CharField(max_length=150)),
                ('deskribapena', models.TextField()),
                ('activate_date', models.DateTimeField(auto_now_add=True)),
                ('expire_date', models.DateTimeField(blank=True, null=True)),
                ('irudia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photologue.Photo')),
            ],
            options={
                'verbose_name': 'Eskaintza',
                'verbose_name_plural': 'Eskaintza',
            },
        ),
        migrations.AlterField(
            model_name='bazkidea',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 4, 19, 16, 23, 91006, tzinfo=utc)),
        ),
    ]
