
from django import forms
from django.forms import widgets 

from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
                    "date", 
                    "time", 
                    "place",
                    "remarks",
                ]
        widgets = {
                    "date": widgets.DateInput(),
                    "time": widgets.TimeInput(),
                }
