from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# placeholder just to get started
def index(request):
    return HttpResponse("Hello world")