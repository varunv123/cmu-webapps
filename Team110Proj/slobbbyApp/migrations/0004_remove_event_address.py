# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slobbbyApp', '0003_event_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='address',
        ),
    ]