# Generated by Django 2.2.17 on 2021-01-11 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210111_1408'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile_user',
            new_name='user',
        ),
    ]