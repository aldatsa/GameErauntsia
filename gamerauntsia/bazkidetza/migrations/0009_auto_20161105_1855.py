# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-05 17:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jokoa', '__first__'),
        ('bazkidetza', '0008_auto_20161105_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='OparitzekoJokoak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=250)),
                ('oparituta', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'publikazio data')),
                ('jokoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jokoa.Jokoa')),
                ('plataforma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jokoa.Plataforma')),
            ],
            options={
                'verbose_name': 'Oparitzeko jokoa',
                'verbose_name_plural': 'Oparitzeko jokoak',
            },
        ),
        migrations.AlterField(
            model_name='bazkidea',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 5, 17, 55, 26, 498343, tzinfo=utc)),
        ),
    ]
