# Generated by Django 5.0.4 on 2024-10-30 09:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BC', '0007_profile_is_creator_profile_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 29, 9, 43, 51, 3057, tzinfo=datetime.timezone.utc)),
        ),
    ]
