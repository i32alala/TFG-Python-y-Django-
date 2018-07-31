# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policia', '0003_auto_20180712_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='etiqueta',
            name='bolso',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='etiqueta',
            name='chaqueta',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='etiqueta',
            name='cinturon',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='etiqueta',
            name='falda',
            field=models.CharField(default=3, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='etiqueta',
            name='jersey',
            field=models.CharField(default=4, max_length=200),
            preserve_default=False,
        ),
    ]
