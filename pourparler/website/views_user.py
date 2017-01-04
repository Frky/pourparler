from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

def register(req):
    tpl = "website/register.html"
    ctxt = dict()
    form = UserCreationForm(req.POST or None)
    if form.is_valid():
        usr = form.save()
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

