# Generated by Django 2.2.26 on 2022-02-16 19:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bazkidetza', '0009_auto_20220216_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bazkidea',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 16, 19, 34, 36, 77181, tzinfo=utc)),
        ),
    ]
