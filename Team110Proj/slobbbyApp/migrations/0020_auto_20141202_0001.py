# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('slobbbyApp', '0019_auto_20141201_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endDate',
            field=models.DateField(default=datetime.date(2014, 12, 2)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='endTime',
            field=models.TimeField(default=datetime.time(0, 1, 46, 738988)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='startDate',
            field=models.DateField(default=datetime.date(2014, 12, 2)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='startTime',
            field=models.TimeField(default=datetime.time(0, 1, 46, 738926)),
            preserve_default=True,
        ),
    ]
