#-*- coding: utf-8 -*-

import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render, redirect, HttpResponse

from .views_user import register, p_login, p_logout, profile, user_settings, p_change_pwd 
from .models import Event, Subject, Speech
from .forms import EventForm, SubjectForm
from .draw import random_draw


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
    ctxt["nb_submitted"] = Subject.objects.filter(event=event).count()
    try:
        ctxt["my_subject"] = Subject.objects.get(event=event, author=req.user.locutor)
    except ObjectDoesNotExist:
        ctxt["my_subject"] = None
    except MultipleObjectsReturned:
        ctxt["my_subject"] = None
    except AttributeError:
        ctxt["my_subject"] = None
    if event.reg_closed:
        subjects = Subject.objects.filter(event=event)
        ctxt["speechs"] = sorted([Speech.objects.get(subject=s) for s in subjects], key=lambda a: a.order)
    else:
        # For now, anyone with the link can register
        ctxt["can_participate"] = not event.is_booked() and req.user.is_authenticated() and not req.user.is_anonymous()
        ctxt["subject_form"] = SubjectForm()
    return render(req, tpl, ctxt)

def submit_subject(req):
    form = SubjectForm(req.POST)
    if form.is_valid():
        # Check if there is still available slots
        if Event.objects.get(id=req.POST["event"]).is_booked():
            messages.error(req, "Cet événement est complet.")
            return redirect("event", eid=req.POST["event"]) 
        # Check if user has already proposed a subject
        if Subject.objects.filter(author=req.user.locutor, event=req.POST["event"]).count() > 0:
            messages.error(req, "Vous avez déjà proposé un sujet pour cet événement.")
            return redirect("event", eid=req.POST["event"]) 

        subject = form.save(req=req)
        speech = Speech()
        speech.subject = subject
        speech.order = -1
        speech.save()
    return redirect("event", eid=req.POST["event"]) 

def draw(req, eid):
    event = Event.objects.get(id=eid)
    if req.user != event.creator.user:
        return redirect("event",eid=eid)
    if event.reg_closed:
        return None
    subjects = Subject.objects.filter(event=event)
    attribution = random_draw(subjects)
    for i, (s, p) in enumerate(zip(*attribution)):
        speech = Speech.objects.get(subject=s)
        speech.speaker = p
        speech.order = i + 1
        speech.save()
    event.reg_closed = True
    event.save()
    return redirect("event", eid=eid)

def speech(req, sid):
    tpl = "website/speech.html"
    ctxt = dict()
    speech = Speech.objects.get(id=sid)
    if "speech-text" in req.POST and speech.speaker.user == req.user:
        speech.text = req.POST["speech-text"]
        speech.save()
    ctxt["speech"] = speech 
    return render(req, tpl, ctxt)

def del_speech(req, sid):
    speech = Speech.objects.get(id=sid)
    if speech.speaker.user == req.user:
        speech.text = ""
        speech.save()
    return redirect("speech", sid=sid)

