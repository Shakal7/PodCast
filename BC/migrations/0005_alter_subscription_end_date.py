# Generated by Django 5.0.4 on 2024-10-30 05:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BC', '0004_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 29, 5, 40, 13, 729374, tzinfo=datetime.timezone.utc)),
        ),
    ]
