from django.shortcuts import render
from django.views import generic

from .models import Device


def index(request):
    return render(request, 'network_topology/index.html', {})

