# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='etiqueta',
            name='zapatos',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
