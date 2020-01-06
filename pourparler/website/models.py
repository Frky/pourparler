#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from website.random_primary import RandomPrimaryIdModel


class Locutor(RandomPrimaryIdModel):
    user = models.OneToOneField(User, related_name="locutor")
    friends = models.ManyToManyField("Locutor")
    pic = models.ImageField(upload_to='pic', null=True, blank=True)
    ## Préférences de l'utilisateur (todo)


class Event(RandomPrimaryIdModel):
    # Creator of the event
    creator = models.ForeignKey(Locutor)
    # Maximum number of participants that can register
    nb_max = models.IntegerField(default=6)
    # Duration of speech
    duration = models.IntegerField(default=5)
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

    # Registrations are closed?
    reg_closed = models.BooleanField(default=False)
    # Registrations are open until N days before the event
    registration_until = models.IntegerField(default=8)
    # Subjects will be delivered to participants N days before the event
    subjects_distribution_date = models.IntegerField(default=7)

    # Can a person be assigned is own subject?
    collide = models.BooleanField(default=False)

    def is_booked(self):
        subjects = Subject.objects.filter(event=self).count()
        return subjects >= self.nb_max

class Subject(models.Model):
    # Who has proposed this subject?
    author = models.ForeignKey(Locutor, related_name="author")
    # To what event this subject is relative to?
    event = models.ForeignKey(Event)
    # Content of the subject
    text = models.CharField(max_length=512)
    # When the subject has been proposed
    date = models.DateTimeField(auto_now_add=True)


class Speech(RandomPrimaryIdModel):
    # Subject treated by this speech
    subject = models.OneToOneField(Subject, related_name="speech")
    # Who is speaking?
    speaker = models.ForeignKey(Locutor, blank=True, null=True, related_name="speaker")
    # Order of passage
    order = models.IntegerField(blank=False, null=False)
    # Text of the speech
    text = models.TextField(max_length=20000)
    # PDF/File of the speech
    # XXX
    # Audio recording of the speech
    audio = models.FileField(upload_to="audio", blank=True, null=True)
    # When the speech has been added
    date = models.DateTimeField(auto_now_add=True)

