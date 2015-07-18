# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('slobbbyApp', '0032_auto_20141202_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endTime',
            field=models.TimeField(default=datetime.time(3, 46, 38, 522613)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='startTime',
            field=models.TimeField(default=datetime.time(3, 46, 38, 522559)),
            preserve_default=True,
        ),
    ]
