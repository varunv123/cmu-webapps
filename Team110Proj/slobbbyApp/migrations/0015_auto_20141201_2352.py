# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('slobbbyApp', '0014_auto_20141201_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endTime',
            field=models.TimeField(default=datetime.time(23, 52, 32, 850608)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='startTime',
            field=models.TimeField(default=datetime.time(23, 52, 32, 850555)),
            preserve_default=True,
        ),
    ]
