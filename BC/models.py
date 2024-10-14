from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Episode(models.Model):
    Title = models.CharField(max_length=200)
    Artist = models.CharField(max_length=200, blank=True, null=True)
    Type = models.CharField(max_length=200, blank=True, null=True)

    # image = models.ImageField(blank=True, null=True)
    # audio_files = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.Title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
