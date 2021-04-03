from django.shortcuts import render
from django.views import generic

from .models import Device


class IndexView(generic.ListView):
    template_name = 'finance/index.html'
    context_object_name = 'finance_payments_list'

    def get_queryset(self):
        return Device().objects.all()

class DetailView(generic.DetailView):
    model = Device
    template_name = 'finance/detail.html'

    def get_queryset(self):
        return Device.objects.all()
