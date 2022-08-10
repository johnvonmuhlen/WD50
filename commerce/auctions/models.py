from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class Categorie(models.Model):
   title = models.CharField(max_length=30, default="")


   def __str__(self):
        return f"{self.id}: {self.title}"

class User(AbstractUser):
    #comments = models.ManyToManyField(Comment, blank=True, related_name="user", default="")
    #listings_in_watchlist = models.ManyToManyField(Listing, blank=True, related_name="user", default="")
    pass

class Comment(models.Model):
    content = models.CharField(max_length=150, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment", default="comment")

    def __str__(self):
        return f"{self.content} by {self.user}"

class Bid(models.Model):
    price = models.IntegerField(default='')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid", default="current_bidder")

    def __str__(self):
        return f"${self.price}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    short_description = models.CharField(max_length=50, default="", )
    detailed_description = models.CharField(max_length=300, default="")
    image = models.ImageField(default="image")
    category = models.ManyToManyField(Categorie, blank=True, related_name="listings",  default="get_listing_category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", default="owner")
    created_on = models.DateTimeField(auto_now=True)
    current_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="listing", default="bid")
    

    def __str__(self):
        return f"{self.id}: {self.title}, Starting Bid: {self.current_bid}"




