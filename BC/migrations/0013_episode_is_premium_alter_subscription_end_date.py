# Generated by Django 5.1.2 on 2024-12-02 21:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BC', '0012_player_alter_subscription_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 1, 21, 21, 19, 303044, tzinfo=datetime.timezone.utc)),
        ),
    ]
