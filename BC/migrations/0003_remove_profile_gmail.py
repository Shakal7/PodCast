# Generated by Django 5.1.2 on 2024-10-14 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BC', '0002_rename_name_profile_gmail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='Gmail',
        ),
    ]