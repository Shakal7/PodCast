from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Episode(models.Model):
    Title = models.CharField(max_length=200)
    Artist = models.CharField(max_length=200, blank=True, null=True)
    Type = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, default='images/default.jpg')
    audio_files = models.FileField(blank=True, null=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.Title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    is_creator = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



class Player(models.Model):
    volume = models.FloatField(default=0.5)  # Volume level, default to 0.5
    current_audio_index = models.PositiveIntegerField(blank=True,null=True)  # Index of the currently playing audio, can be blank initially
    is_playing = models.BooleanField(default=False)


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    plan = models.CharField(max_length=50, default='Free')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now() + timedelta(days=30))
    is_active = models.BooleanField(default=False) 


    def __str__(self):
        return f"{self.user.username} - {self.plan} Plan"