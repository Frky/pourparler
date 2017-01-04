
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from .views_user import register, p_login, p_logout 
from .models import Event
from .forms import EventForm


def index(req):
    tpl = "website/index.html"
    ctxt = dict()
    return render(req, tpl, ctxt)

def create_event(req):
    tpl = "website/create.html"
    ctxt = dict()
    form = EventForm()
    if form.is_valid():
        event = form.save()
        print event.id
        return redirect("event", event.id)
    else:
        print form.errors
    ctxt["form"] = form
    return render(req, tpl, ctxt)

def event(req, eid):
    tpl = "website/event.html"
    try:
        event = Event.objects.get(id=eid)
    except ObjectDoesNotExist:
        return redirect("index")
    ctxt["e"] = event
    return render(req, tpl, ctxt)
