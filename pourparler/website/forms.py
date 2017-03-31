#-*- coding: utf-8 -*-

import datetime

from django import forms
from django.forms import widgets 
from django.forms.extras.widgets import SelectDateWidget

from .models import Event

months = {
            1: 'jan.', 
            2: 'fev.', 
            3: 'mars', 
            4: 'avr.',
            5: 'mai', 
            6: 'juin', 
            7: 'jui.', 
            8: 'août',
            9: 'sep.', 
            10: 'oct.', 
            11: 'nov.', 
            12: 'dec.',
        }

class EventForm(forms.ModelForm):

    initials = {
                "event_date": datetime.date.today(), 
                "nb_max": 7
            }

    class Meta:
        model = Event
        fields = [
                    "nb_max",
                    "event_date", 
                    "event_time", 
                    "event_place",
                    "description", 

                    # Additional fields
                    "participation",
                    "diffusion",
                ]
        widgets = {
                    "event_date": SelectDateWidget(months=months), 
                    "event_time": widgets.TimeInput(),
                    "participation": widgets.Select(choices=(
                            (1, "Quiconque peut participer"), 
                            (2, "Sur invitation du créateur seulement"),
                            (3, "Sur invitation d'un participant"), 
                        )),
                    "diffusion": widgets.Select(choices=(
                            (1, "Quiconque peut accéder aux discours"), 
                            (2, "Seuls les participants peuvent accéder au discours"),
                            (3, "Seul l'auteur peut accéder à son discours"), 
                        ))

                }
        labels = {
                    "nb_max": "Combien de locuteurs (au plus) ?",
                    "event_date": "Quand ça ?",
                    "event_time": "À quelle heure ?",
                    "event_place": "Où donc ?",
                    "description": "Quelque chose à ajouter ?",

                    "participation": "Participation",
                    "diffusion": "Diffusion",
                }

    def save(self, req=None, commit=True):
        event = super(EventForm, self).save(False)
        if req is None:
            return None
        event.creator = req.user.locutor
        if commit:
            event.save()
        return event

