#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from website.random_primary import RandomPrimaryIdModel


class Locutor(RandomPrimaryIdModel):
    user = models.OneToOneField(User, related_name="locutor")
    friends = models.ManyToManyField("Locutor")
    ## Préférences de l'utilisateur (todo)


class Event(RandomPrimaryIdModel):
    # Creator of the event
    creator = models.ForeignKey(Locutor)
    # Maximum number of participants that can register
    nb_max = models.IntegerField(default=6)
    # Can anyone attend, or is it a private event?
    participation = models.IntegerField(default=0)
    # Can anyone access the subjects/speeches, or is it a restricted diffusion?
    diffusion = models.IntegerField(default=0)

    # When the eloquence takes place
    event_date = models.DateField(default=None, blank=False, null=False)
    event_time = models.TimeField(default=None, blank=True, null=True)
    # Where the eloquence takes place
    event_place = models.CharField(max_length=512, blank=True, null=True)

    # Additional information for the participants
    description = models.TextField(max_length=1024, blank=True, null=True)

    # Registrations are open until N days before the event
    registration_until = models.IntegerField(default=8)
    # Subjects will be delivered to participants N days before the event
    subjects_distribution_date = models.IntegerField(default=7)

    # Can a person be assigned is own subject?
    collide = models.BooleanField(default=False)


class Subject(models.Model):
    # Who is assigned this subject?
    author = models.ForeignKey(Locutor)
    # To what event this subject is relative to?
    event = models.ForeignKey(Event)
    # Content of the subject
    text = models.CharField(default="What? So what? Now what?", max_length=512)
    # When the subject has been proposed
    date = models.DateTimeField(auto_now_add=True)


class Speech(models.Model):
    # Subject treated by this speech
    subject = models.ForeignKey(Subject)
    # Order of passage
    order = models.IntegerField(blank=False, null=False)
    # Text of the speech
    text = models.TextField(max_length=20000)
    # Audio recording of the speech
    audio = models.FileField(blank=True, null=True)
    # When the speech has been added
    date = models.DateTimeField(auto_now_add=True)
