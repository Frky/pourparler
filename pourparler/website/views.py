#-*- coding: utf-8 -*-

import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from .views_user import register, p_login, p_logout, profile 
from .models import Event
from .forms import EventForm


def index(req):
    tpl = "website/index.html"
    ctxt = dict()
    return render(req, tpl, ctxt)

@login_required(login_url="login")
def create_event(req):
    tpl = "website/create.html"
    ctxt = dict()
    form = EventForm(req.POST)
    if form.is_valid():
        event = form.save(req=req)
        return redirect("event", event.id)
    else:
        print form.errors
    ctxt["form"] = EventForm(initial=EventForm.initials)

    return render(req, tpl, ctxt)

def event(req, eid):
    tpl = "website/event.html"
    ctxt = dict()
    try:
        event = Event.objects.get(id=eid)
    except ObjectDoesNotExist:
        return redirect("index")
    ctxt["e"] = event
    return render(req, tpl, ctxt)
