# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('slobbbyApp', '0004_remove_event_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='endDate',
            field=models.DateField(default=datetime.date(2014, 11, 15)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='startDate',
            field=models.DateField(default=datetime.date(2014, 11, 15)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='endTime',
            field=models.TimeField(default=datetime.time(13, 48, 20, 367961)),
        ),
        migrations.AlterField(
            model_name='event',
            name='startTime',
            field=models.TimeField(default=datetime.time(13, 48, 20, 367906)),
        ),
    ]
