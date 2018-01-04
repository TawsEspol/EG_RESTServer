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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('codigo', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=80)),
                ('unidad', models.CharField(max_length=10)),
                ('bloque', models.CharField(max_length=10)),
                ('tipo', models.CharField(max_length=20)),
                ('descripcio', models.CharField(max_length=50)),
                ('area_m2', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4236)),
            ],
        ),
    ]
