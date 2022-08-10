from django.urls import path

from . import views

app_name = "bruh"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.entry, name="entry"),
    path("random", views.random, name="random")
]
