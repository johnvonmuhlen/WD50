import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    current_user = request.user
    return render(request, "network/index.html", {
        "current_user": current_user
    })

def profile(request, user):
    current_user = request.user
    user_profile = User.objects.get(username = user)
    return render(request, "network/profile.html", {
        "current_user": current_user,
        "user_profile": user_profile
    })

def follow(request, user_id):
    pass


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def new_post(request):

    user = User.objects.get(username=request.user.username)
    # Composing a new email must be via POST
    if request.method == "POST":
            
        # Get contents of post
        body = request.POST["body"]
        #Create post

        if len(body) < 2:
            return render(request, "auctions/index.html", {
                "message": "Post must have at least 2 words"
            })
        
        else:
            post = Post(content=body, likes=0, total_comments=0, user=user)
            post.save()
            return render(request, "network/index.html")

    else:
        return JsonResponse({"error": "Request method must be Post"}, status=201) 


def posts(request):
    posts = Post.objects.all()
    
    #p = Paginator(posts, 10)
    return JsonResponse([posts.serialize() for post in posts], safe=False)