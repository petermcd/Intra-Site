from django.utils.timezone import now
from django.views import generic

from events.models import Event, EventAccommodation, EventTravel
from network_topology.models import Settings


class IndexView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        """
        Get event objects to display in index view.

        Return:
            List of event objects
        """
        return Event.objects.all().filter(ending__gte=now()).order_by('starting')

    def get_context_data(self, **kwargs):
        """
        Obtain context data ready for output

        Return:
            Context data ready for output in a template
        """
        return super().get_context_data(**kwargs)


class DetailView(generic.DetailView):
    model = Event
    template_name = 'events/detail.html'

    def get_context_data(self, **kwargs):
        """
        Obtain context data ready for output

        Return:
            Context data ready for output in a template
        """
        context = super().get_context_data(**kwargs)
        context['api_key'] = Settings.objects.filter(name__exact='GOOGLE_API_KEY')[0].value
        context['accommodation'] = EventAccommodation.objects.filter(event__exact=context['event'])
        context['to'] = EventTravel.objects.filter(event__exact=context['event'], direction__exact='To')
        context['from'] = EventTravel.objects.filter(event__exact=context['event'], direction__exact='From')
        return context

    def get_queryset(self):
        """
        Get event objects to display in detail view.

        Return:
            List of event objects
        """
        return Event.objects.all()
