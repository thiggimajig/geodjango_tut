# Generated by Django 3.2.7 on 2022-05-25 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0014_auto_20220515_1139'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AirbnbListings',
            new_name='AirbnbListingstable',
        ),
    ]