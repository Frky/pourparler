#-*- coding: utf-8 -*-

import datetime

from django import forms
from django.forms import widgets 
from django.forms.extras.widgets import SelectDateWidget

from .models import Event, Subject
from .widgets.select_time_widget import SelectTimeWidget

months = {
            1: 'janvier', 
            2: 'fevrier', 
            3: 'mars', 
            4: 'avril',
            5: 'mai', 
            6: 'juin', 
            7: 'juillet', 
            8: 'août',
            9: 'septembre', 
            10: 'octobre', 
            11: 'novembre', 
            12: 'décembre',
        }

class EventForm(forms.ModelForm):

    initials = {
                "event_date": datetime.date.today(), 
				"nb_max": "",
                "duration": "",
				"event_time": datetime.time(20,00),
            }

    class Meta:
        model = Event
        fields = [
                    "event_date", 
                    "event_time", 
                    "event_place",
                    "duration", 
                    "nb_max",
                    "description", 

                    # Additional fields
                    # "participation",
                    # "diffusion",
                ]
        widgets = {
                    "duration": widgets.NumberInput(attrs={"class": "uk-input", "placeholder": "cinq minutes, c'est pas mal"}),
                    "nb_max": widgets.NumberInput(attrs={"class": "uk-input", "placeholder": "conseil : entre six et huit"}),
                    "event_date": SelectDateWidget(months=months, attrs={"class": "uk-select event-date-select"}), 
                    "event_time": SelectTimeWidget(twelve_hr=True, minute_step=5, attrs={"class": "uk-input event-time-select"}),
                    "event_place": widgets.TextInput(attrs={"class": "uk-input", "placeholder": "une place publique, une agora, un charmant salon"}),
                    "description": widgets.Textarea(attrs={"class": "uk-textarea"}),
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
                    "duration": "Quelle durée de discours (en minutes) ?",
                    "nb_max": "Combien de locuteurs au maximum ?",
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

class SubjectForm(forms.ModelForm):

    class Meta:

        model = Subject
        fields = [
                    "text", 
                ]
        widgets = {
                    "text": forms.TextInput(attrs={
                                "placeholder": "Proposition de sujet",
                                "class": "uk-input",
                                                    }),
                }
        labels = {
                    "text": "",
                }

    def save(self, req=None, commit=True):
        subject = super(SubjectForm, self).save(False)
        if req is None:
            return None
        subject.author = req.user.locutor
        subject.event = Event.objects.get(id=req.POST["event"])
        if commit:
            subject.save()
        return subject


class ImageUploadForm(forms.Form):
    img = forms.ImageField()


class AudioUploadForm(forms.Form):
    audio = forms.FileField()
