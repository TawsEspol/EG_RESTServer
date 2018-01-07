# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bloques',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('codigo', models.CharField(max_length=60)),
                ('nombre', models.CharField(max_length=80)),
                ('unidad', models.CharField(max_length=60)),
                ('bloque', models.CharField(max_length=60)),
                ('tipo', models.CharField(max_length=60)),
                ('descripcio', models.CharField(max_length=100)),
                ('area_m2', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4236)),
            ],
        ),
    ]
