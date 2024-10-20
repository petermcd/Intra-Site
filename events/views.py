"""Views for the Finance application."""
from django.http import HttpResponse
from django.utils.timezone import now
from django.views import generic
from django.views.decorators.http import require_GET

from events.models import Accommodation, Event, Travel
from settings.models import Setting


class IndexView(generic.ListView):
    """View implementation for events list."""

    template_name = "events/index.html"
    context_object_name = "event_list"

    def get_queryset(self):
        """
        Get event objects to display in index view.

        Return:
            List of event objects
        """
        return Event.objects.all().filter(ends__gte=now()).order_by("start")

    def get_context_data(self, **kwargs):
        """
        Obtain context data ready for output.

        Return:
            Context data ready for output in a template
        """
        return super().get_context_data(**kwargs)


class DetailView(generic.DetailView):
    """View implementation for event details."""

    model = Event
    template_name = "events/event.html"

    def get_context_data(self, **kwargs):
        """
        Obtain context data ready for output.

        Return:
            Context data ready for output in a template
        """
        context = super().get_context_data(**kwargs)
        context["api_key"] = Setting.objects.filter(name__exact="GOOGLE_API_KEY")[
            0
        ].value
        context["accommodation"] = Accommodation.objects.filter(
            for_event__exact=context["event"]
        ).order_by("check_in")
        context["to"] = Travel.objects.filter(
            for_event__exact=context["event"], direction__exact="To"
        ).order_by("departure")
        context["during"] = Travel.objects.filter(
            for_event__exact=context["event"], direction__exact="During"
        ).order_by("departure")
        context["from"] = Travel.objects.filter(
            for_event__exact=context["event"], direction__exact="From"
        ).order_by("departure")
        return context

    def get_queryset(self):
        """
        Get event objects to display in detail view.

        Return:
            List of event objects
        """
        return Event.objects.all()


@require_GET
def event_delete(request, pk: int) -> HttpResponse:
    """
    View to handle deleting and event a task item.

    Args:
        request: Request object
        pk: primary key for the task item being marked as complete

    Returns:
        Empty response with a 200 code
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    event_item = Event.objects.filter(pk=pk)
    if len(event_item) == 1:
        event_item[0].delete()
    return HttpResponse(status=200)
