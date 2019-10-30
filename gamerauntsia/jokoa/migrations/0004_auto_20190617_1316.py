# Generated by Django 2.2.2 on 2019-06-17 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jokoa', '0003_auto_20170606_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jokoa',
            name='logoa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='photologue.Photo'),
        ),
        migrations.AlterField(
            model_name='plataforma',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='photologue.Photo'),
        ),
    ]