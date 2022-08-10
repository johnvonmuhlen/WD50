from django.shortcuts import render
from django.http import HttpResponse
import markdown2
import random

from . import util

entries = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, name):

    bruh = markdown2.markdown(util.get_entry(name))

    return render(request, "encyclopedia/entry.html", {
        "name": bruh,
        "title": name
    })

def random(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    entry_content = markdown2.markdown(util.get_entry(random_entry))

    return render(request, "encyclopedia/random.html", {
        "title": random_entry,
        "content": entry_content
    })
