import os

import catboost
import pandas as pd
from django.contrib.auth.models import User
from valuation.models import Profile
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import random
import string
from valuation.datadesc import *

test_api_dict = {
    "cont_features": [[feature_names_dict[c], c] for c in cont_features],
    "cat_features": [[feature_names_dict[c], c, cat_options_dict[c]] for c in cat_features],
    "features_desc": [(feature_names_dict[f], feature_desc_dict[f]) for f in features],
}

model = catboost.CatBoost()
model.load_model("valuation/CatboostModel.cbm", format="cbm")


def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return render(request, "accounts.html")


def validate_features(request):
    for f in features:
        if str(f) not in request.POST:
            return HttpResponse("Invalid Input", status=400)
    for c in cat_features:
        if not request.POST[c].isnumeric():
            return HttpResponse("Non-integer value for feature " + c, status=400)
        if int(request.POST[c]) not in cat_options_dict_raw[c]:
            return HttpResponse("Invalid option for categorical feature " + c, status=400)
    for c in cont_features:
        if not request.POST[c].isnumeric():
            return HttpResponse("Non-integer value for feature " + c, status=400)


def demo_view(request):
    if request.method == "GET":
        return render(request, "demoapi.html", test_api_dict)
    if request.method == "POST":
        if not request.POST.get("api_key", None) or (
            request.POST["api_key"] != "FREE_KEY"
            and not Profile.objects.filter(api_key=request.POST["api_key"])
        ):
            return HttpResponse("API Key is Invalid", status=401)
        vf = validate_features(request)
        if vf is not None:
            return vf
        return render(
            request,
            "demoapi.html",
            {**{"returned_data": get_home_price_json(request)}, **test_api_dict},
        )


def test_api_view(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "GET":
        return render(request, "testapi.html", test_api_dict)
    if request.method == "POST":
        if not request.POST.get("api_key", None) or not Profile.objects.filter(
            api_key=request.POST["api_key"]
        ):
            return HttpResponse("API Key is Invalid", status=401)
        vf = validate_features(request)
        if vf is not None:
            return vf
        return render(
            request,
            "testapi.html",
            {**{"returned_data": get_home_price_json(request)}, **test_api_dict},
        )


def get_home_price(request):
    if not request.POST["api_key"] or not Profile.objects.filter(api_key=request.POST["api_key"]):
        return HttpResponse("API Key is Invalid", status=401)
    if request.method == "POST":
        vf = validate_features(request)
        if vf is not None:
            return vf
        return JsonResponse(get_home_price_json(request))


def get_home_price_json(request):
    df = pd.DataFrame({f: [request.POST[f]] for f in features})
    return {"price": "$" + str("{:0.2f}".format(model.predict(df)[0]))}


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
    return render(request, "accounts.html", {"failed_login": True})


def logout_view(request):
    logout(request)
    return redirect("/")


def delete_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("/")
    logout(request)
    user.delete()
    return redirect("/")


def signup_view(request):
    if User.objects.filter(username=request.POST["username"]):
        return render(request, "accounts.html", {"username_taken": True})
    api_key = "".join(random.choices(string.ascii_letters + string.digits, k=30))
    while User.objects.filter(profile__api_key=api_key):
        api_key = "".join(random.choices(string.ascii_letters + string.digits, k=30))
    user = User.objects.create_user(
        username=request.POST["username"],
        email=request.POST["email"],
        password=request.POST["password"],
    )
    user.save()
    user.profile.email = request.POST["email"]
    user.profile.name = request.POST["name"]
    user.profile.api_key = api_key
    user.profile.save()
    login(request, user)
    return redirect("/")
