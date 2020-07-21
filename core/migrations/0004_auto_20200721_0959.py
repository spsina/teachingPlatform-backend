# Generated by Django 3.0.8 on 2020-07-21 05:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200721_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 21, 5, 29, 9, 20753, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 21, 5, 29, 12, 796735, tzinfo=utc)),
            preserve_default=False,
        ),
    ]