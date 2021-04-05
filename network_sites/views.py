from django.views import generic

from .models import Site


class IndexView(generic.ListView):
    template_name = 'network_sites/index.html'
    context_object_name = 'network_sites_list'

    def get_queryset(self):
        return Site.objects.all().order_by('name')
