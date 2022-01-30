from django.db import models
from datetime import datetime

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length = 1000)
    


class Message(models.Model):
    value = models.CharField(max_length = 10000000)
    date = models.DateTimeField(default = datetime.now, blank = True)
    #where message coming from is the room
    room = models.CharField(max_length = 10000000)
    #this is the user sending  message
    user = models.CharField(max_length = 10000000)

    #could use ForeignKey



