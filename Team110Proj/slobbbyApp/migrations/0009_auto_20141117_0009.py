# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('slobbbyApp', '0008_auto_20141116_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endDate',
            field=models.DateField(default=datetime.date(2014, 11, 17)),
        ),
        migrations.AlterField(
            model_name='event',
            name='endTime',
            field=models.TimeField(default=datetime.time(0, 9, 37, 11670)),
        ),
        migrations.AlterField(
            model_name='event',
            name='startDate',
            field=models.DateField(default=datetime.date(2014, 11, 17)),
        ),
        migrations.AlterField(
            model_name='event',
            name='startTime',
            field=models.TimeField(default=datetime.time(0, 9, 37, 11622)),
        ),
    ]
