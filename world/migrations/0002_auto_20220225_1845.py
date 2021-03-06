# Generated by Django 3.2.7 on 2022-02-25 18:45

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirbnbListings',
            fields=[
                ('listing_number', models.IntegerField()),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('listing_url', models.CharField(max_length=1000)),
                ('name', models.CharField(max_length=1000)),
                ('host_id', models.IntegerField()),
                ('host_name', models.CharField(max_length=1000)),
                ('host_since', models.CharField(max_length=100)),
                ('host_location', models.CharField(max_length=100)),
                ('host_total_listings_count', models.IntegerField()),
                ('neighbourhood_cleansed', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('room_type', models.CharField(max_length=100)),
                ('accommodates', models.IntegerField()),
                ('bedrooms', models.IntegerField()),
                ('price', models.FloatField()),
                ('availability_30', models.IntegerField()),
                ('availability_60', models.IntegerField()),
                ('availability_90', models.IntegerField()),
                ('availability_365', models.IntegerField()),
                ('number_of_reviews_ltm', models.IntegerField()),
                ('number_of_reviews_l30d', models.IntegerField()),
                ('license', models.CharField(max_length=100)),
                ('instant_bookable', models.CharField(max_length=10)),
                ('calculated_host_listings_count', models.IntegerField()),
                ('reviews_per_month', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.DeleteModel(
            name='WorldBorder',
        ),
    ]
