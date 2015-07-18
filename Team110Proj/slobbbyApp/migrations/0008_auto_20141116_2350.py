# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('slobbbyApp', '0007_auto_20141116_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='invitedUsers',
            field=models.ManyToManyField(related_name=b'invitedUsers', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='endTime',
            field=models.TimeField(default=datetime.time(23, 50, 22, 817050)),
        ),
        migrations.AlterField(
            model_name='event',
            name='startTime',
            field=models.TimeField(default=datetime.time(23, 50, 22, 817008)),
        ),
    ]
