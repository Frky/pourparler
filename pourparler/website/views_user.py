
from PIL import Image
import os
import string
from random import choice

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.files.base import File
from django.conf import settings

from models import Locutor, Event, Subject, Speech
from forms import ImageUploadForm

def register(req):
    tpl = "website/register.html"
    ctxt = dict()
    form = UserCreationForm(req.POST or None)
    if form.is_valid():
        usr = form.save()
        Locutor(user=usr).save()
        usr = authenticate(
                                username=usr.username, 
                                password=req.POST["password1"],
                            )
        # Log the new user in
        login(req, usr)
        return redirect("index")
    else:
        ctxt["form"] = form
    return render(req, tpl, ctxt)

def p_login(req):
    tpl = "website/login.html"
    ctxt = dict()
    username = req.POST.get("username", None)
    password = req.POST.get("password", None)
    if username is not None and password is not None:
        print "yolo"
        try:
            usr = User.objects.get(username=req.POST["username"])
            authenticate(
                            username=usr.username,
                            password=req.POST["password"],
                        )
            login(req, usr)
            return redirect("index")
        except Exception:
            print "oho"
    ctxt["form"] = AuthenticationForm(req.POST or None)
    return render(req, tpl, ctxt)

def p_logout(req):
    logout(req)
    return redirect("index")

def profile(req, uid):
    tpl = "website/profile.html"
    ctxt = dict()
    locutor = get_object_or_404(Locutor, id=uid)
    ctxt["locutor"] = locutor
    ctxt["events"] = sorted(Event.objects.filter(creator=locutor), key=lambda e: e.event_date)
    ctxt["subjects"] = sorted([s.subject for s in Speech.objects.filter(speaker=locutor)], key=lambda s: s.event.event_date)
    return render(req, tpl, ctxt)

def user_settings(req):
    if not req.user.is_authenticated() or req.user.is_anonymous():
        return redirect("index")
    tpl = "website/settings.html"
    ctxt = dict()

    loc = req.user.locutor
    if req.method == "POST":
        random_pic_name = "".join([choice(string.ascii_letters) for i in xrange(32)])
        if 'img' in req.FILES.keys():
            req.FILES['img'].name = random_pic_name
        picform = ImageUploadForm(req.POST, req.FILES)
        if picform.is_valid():
            # TODO delete old file
#             with open(settings.MEDIA_ROOT + 'pic/' + loc.pic.name, 'wb+') as destination:
#                 for chunk in loc.pic.chunks():
#                    destination.write(chunk)
            loc.pic.delete()
            loc.pic = picform.cleaned_data["img"]
            # File(random_pic_name, req.FILES['files[]'])
            loc.save()
            req.user.save()
        else: 
            print picform.errors
    return render(req, tpl, ctxt)
