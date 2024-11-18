# Generated by Django 5.0.4 on 2024-10-30 09:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BC', '0006_episode_audio_files_episode_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_creator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 29, 9, 40, 18, 32834, tzinfo=datetime.timezone.utc)),
        ),
    ]