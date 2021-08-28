from django.utils.timezone import now
from django.views import generic

from events.models import Event


class IndexView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return Event.objects.all().filter(ending__gte=now())

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class DetailView(generic.DetailView):
    model = Event
    template_name = 'events/detail.html'

    def get_queryset(self):
        return Event.objects.all()
