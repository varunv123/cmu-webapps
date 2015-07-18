# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('slobbbyApp', '0010_auto_20141117_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endDate',
            field=models.DateField(default=datetime.date(2014, 12, 1)),
        ),
        migrations.AlterField(
            model_name='event',
            name='endTime',
            field=models.TimeField(default=datetime.time(21, 55, 25, 259933)),
        ),
        migrations.AlterField(
            model_name='event',
            name='startDate',
            field=models.DateField(default=datetime.date(2014, 12, 1)),
        ),
        migrations.AlterField(
            model_name='event',
            name='startTime',
            field=models.TimeField(default=datetime.time(21, 55, 25, 259886)),
        ),
    ]
