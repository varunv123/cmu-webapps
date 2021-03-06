# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('slobbbyApp', '0021_auto_20141202_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endTime',
            field=models.TimeField(default=datetime.time(0, 17, 40, 990876)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='startTime',
            field=models.TimeField(default=datetime.time(0, 17, 40, 990831)),
            preserve_default=True,
        ),
    ]
