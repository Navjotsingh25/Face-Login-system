from django import forms
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.password_validation import password_changed
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)
from .form import signupForm
from .models import Profile
from .facedetection import take_photo, encode_image
import numpy as np
import os
import json


def handle_uploaded_file(f, username):
    dumped = json.dumps(encode_image(f).tolist())

    with open("pages/data/{0}/{1}.json".format(username, f.name[:-4]), "w") as destination:
        json.dump(dumped, destination)


def home(request):
    return render(request, "home.html", {})


def signup_view(request):
    if request.method == "POST":
        fm = signupForm(request.POST, request.FILES)
        if fm.is_valid():
            path = os.path.join(
                "/home/nav/Documents/Django/src/myproject/pages/data",
                request.POST["username"],
            )
            os.mkdir(path)
            handle_uploaded_file(request.FILES["Image1"], request.POST["username"])
            handle_uploaded_file(request.FILES["Image2"], request.POST["username"])
            handle_uploaded_file(request.FILES["Image3"], request.POST["username"])
            handle_uploaded_file(request.FILES["Image4"], request.POST["username"])
            fm.save()
            return redirect("profile")
    else:
        fm = signupForm()
    return render(request, "signup.html", {"form": fm})


def login_view(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data["username"]
            upass = fm.cleaned_data["password"]
            user = authenticate(username=uname, password=upass)

            if user is not None:
                if take_photo(uname):
                    login(request, user)
                    return redirect("profile")
                else:
                    return HttpResponse(
                        "invalid athantication or your photo is not clear"
                    )
    else:
        fm = AuthenticationForm()
    return render(request, "login.html", {"form": fm})


def profile_view(request):
    if request.user.is_authenticated:
        return render(request, "profile.html", {"name": request.user})
    else:
        return redirect("login")


def logout_view(request):
    logout(request)
    return redirect("home")


def about_view(request):
    return render(request,"about.html")