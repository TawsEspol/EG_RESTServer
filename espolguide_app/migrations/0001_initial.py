# Generated by Django 2.0.1 on 2018-05-10 06:33

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bloques',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=60)),
                ('nombre', models.CharField(max_length=80)),
                ('unidad', models.CharField(max_length=60)),
                ('bloque', models.CharField(max_length=60)),
                ('tipo', models.CharField(max_length=60)),
                ('descripcio', models.CharField(max_length=100)),
                ('area_m2', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
    ]
