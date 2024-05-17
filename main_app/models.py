from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
# the tube model
class Tube(models.Model):
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=250)
  url = models.CharField(max_length=250)
  
  def __str__(self):
    return self.title 

# the playlist model
class Playlist(models.Model):
  title = models.CharField(max_length=100)
  tubes = models.ManyToManyField(Tube) 
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # colabs = models.ManyToManyField(User)

  def __str__(self):
    return self.title 

