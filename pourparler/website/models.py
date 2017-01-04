from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from website.random_primary import RandomPrimaryIdModel

class Event(RandomPrimaryIdModel):
    owner = models.ForeignKey(User)
    date = models.DateField(default=None, blank=False, null=False)
    time = models.TimeField(default=None, blank=True, null=True)
    place = models.CharField(max_length=512, blank=True, null=True)
    remarks = models.CharField(max_length=1024, blank=True, null=True)

class Subject(models.Model):
    owner = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    text = models.CharField(default="What? So what? Now what?", max_length=512)
