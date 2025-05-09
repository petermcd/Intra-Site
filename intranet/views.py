"""Views for Intranet."""

from django.views import generic


class IndexView(generic.TemplateView):
    """View implementation for the main index page."""

    template_name = "index.html"
