from django.shortcuts import render, redirect
import json


def index(request):
    context = {"movies": {}}
    response = render(request, "movies/index.html", context)
    return response
