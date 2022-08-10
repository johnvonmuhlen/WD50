from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Categorie, Bid, Comment


def index(request):
    if request.method == "POST":
        title = request.POST["title"]
        short_des = request.POST["short_des"]
        detailed_des = request.POST["detailed_des"]
        starting_bid = request.POST["starting_bid"]
        category = request.POST["category"]

        user = request.user

        if request.user.is_authenticated:
            l = Listing(title=title, short_description=short_des, detailed_description=detailed_des, 
            starting_bid=starting_bid, owner=user)

            l.save()

            l.category.add(Categorie.objects.get(title=category))

            return render(request, "auctions/index.html", {
                "listings": Listing.objects.all()
            })            
        else:
            return render(request, "auctions/login.html")

    else:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all()
        })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    return render(request, "auctions/create_listing.html", {
       "categories": Categorie.objects.all() 
    })

@login_required
def watchlist(request):
    if request.method == "POST":

        return render(request, "auctions/watchlist.html", {

        })

def categories(request):
    return render(request, "auctions/categories.html", {
       "categories": Categorie.objects.all()
    })

def listing(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)

    if request.method == "POST":
        if 'submit' in request.POST:
            comment = request.POST["comment"]
            comments = Comment.objects.all()

            c = Comment(content=comment, user=request.user)
            c.save()

            return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bid": b,
                    "comments": comments
                    })

        else:

            bid = request.POST["bid"]

            if int(bid) <= int(listing.current_bid.price):
                return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Bid must be higher than current bid"
                })
            else:
                b = Bid(price=bid, bidder=listing.current_bid.bidder)

                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bid": b
                    })

    else:
        return render(request, "auctions/listing.html", {
        "listing": listing,
        })

def filter(request, category_title):
    category = Categorie.objects.get(title=category_title)
    listing = Listing.objects.filter(category=category)
    if listing.exists() == False:
        return render(request, "auctions/empty.html", {
            "category": category
        })

    return render(request, "auctions/filtered_listings.html", {
        "category": category,
        "listings": listing
    })
