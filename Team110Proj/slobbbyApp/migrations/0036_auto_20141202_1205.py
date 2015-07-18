# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('slobbbyApp', '0035_auto_20141202_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endTime',
            field=models.TimeField(default=datetime.time(12, 5, 44, 934954)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='startTime',
            field=models.TimeField(default=datetime.time(12, 5, 44, 934910)),
            preserve_default=True,
        ),
    ]
