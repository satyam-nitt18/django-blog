# Generated by Django 2.2.17 on 2021-01-18 18:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20210118_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='profile',
            name='mobile',
            field=models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
