from typing import Any, Dict, List

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import generic

from .models import Device, Site


def index(request) -> HttpResponse:
    """
    Handle the Network topology index

    Return:
        HttpResponse for the index page
    """
    return render(request, 'network_topology/index.html', {})


def topology(request) -> JsonResponse:
    """
    Create and output the node map as a JSON response.

    Return:
        JsonResponse containing node map of the network
    """
    data: Dict[str, List[Any]] = {
        'nodes': [],
        'links': [],
    }
    devices = Device.objects.all()
    for device in devices:
        device_data = {
            "id": f"d{device.pk}",
            "name": device.name,
            "ip": str(device.ip),
            "description": device.description,
            "type": 'device'
        }
        data['nodes'].append(device_data)
        if device.connected_to:
            link = {
                "source": f"d{device.pk}",
                "target": f"d{device.connected_to.pk}"
            }
            data['links'].append(link)

    sites = Site.objects.all()
    for site in sites:
        site_data = {
            "id": f"s{site.pk}",
            "name": site.name,
            "ip": str(site.hosted_on.ip),
            "url": site.corrected_url,
            "description": site.description,
            "type": 'site'
        }
        data['nodes'].append(site_data)
        try:
            hosting_device = Device.objects.get(ip__exact=site.hosted_on.ip.pk)
            link = {
                "source": f"s{site.pk}",
                "target": f"d{hosting_device.pk}"
            }
            data['links'].append(link)
        except Device.DoesNotExist:
            pass
    return JsonResponse(data)


class SiteView(generic.ListView):
    template_name = 'templates/network_topology/index2.html'
    context_object_name = 'network_sites_list'

    def get_queryset(self):
        """
        Get site objects to display in site view.

        Return:
            List of site objects
        """
        return Site.objects.all().order_by('name')
