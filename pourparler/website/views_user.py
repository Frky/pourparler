from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from models import Locutor, Event, Subject

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
    ctxt["events"] = Event.objects.filter(creator=locutor)
    ctxt["subjects"] = Subject.objects.filter(author=locutor)

    return render(req, tpl, ctxt)

