# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policia', '0002_etiqueta_zapatos'),
    ]

    operations = [
        migrations.AddField(
            model_name='etiqueta',
            name='corbata',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='etiqueta',
            name='medias',
            field=models.CharField(default=3, max_length=200),
            preserve_default=False,
        ),
    ]
