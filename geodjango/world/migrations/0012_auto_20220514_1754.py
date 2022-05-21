# Generated by Django 3.2.7 on 2022-05-14 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0011_alter_airbnblistings_geom'),
    ]

    operations = [
        migrations.RenameField(
            model_name='airbnblistings',
            old_name='days_rented',
            new_name='days_rented_ltm',
        ),
        migrations.RenameField(
            model_name='airbnblistings',
            old_name='rounded_revenue',
            new_name='rounded_revenue_ltm',
        ),
        migrations.RemoveField(
            model_name='airbnblistings',
            name='global_total_listings',
        ),
        migrations.RemoveField(
            model_name='airbnblistings',
            name='listing_number',
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='commercial',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='effected_by_policy_1',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='effected_by_policy_2',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='effected_by_policy_3',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='is_campo',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='is_centro',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='is_gavinana',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='is_isolotto',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='is_rifredi',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='last_scraped',
            field=models.DateField(default='2000-01-01', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='listing_revenue_exceed_LTR',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='minimum_nights_avg_ntm',
            field=models.FloatField(default=7.7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='number_of_reviews',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airbnblistings',
            name='occupancy_rate_approx',
            field=models.FloatField(default=7.7),
            preserve_default=False,
        ),
    ]
