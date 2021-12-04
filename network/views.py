from typing import Any, Dict, List

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Device, Website


def index(request) -> HttpResponse:
    """
    Handle the Network topology index

    Return:
        HttpResponse for the index page
    """
    return render(request, 'network/index.html', {})


def network(request) -> JsonResponse:
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
            "name": device.hostname,
            "ip": str(device.ip),
            "description": device.notes,
            "type": 'device'
        }
        data['nodes'].append(device_data)
        if device.connected_too:
            link = {
                "source": f"d{device.pk}",
                "target": f"d{device.connected_too.pk}"
            }
            data['links'].append(link)

    websites = Website.objects.all()
    for website in websites:
        website_data = {
            "id": f"s{website.pk}",
            "name": website.name,
            "ip": str(website.subdomain.device.ip),
            "url": website.full_url,
            "description": website.description,
            "type": 'site'
        }
        data['nodes'].append(website_data)
        try:
            hosting_device = Device.objects.get(ip__exact=website.subdomain.device.ip.pk)
            link = {
                "source": f"s{website.pk}",
                "target": f"d{hosting_device.pk}"
            }
            data['links'].append(link)
        except Device.DoesNotExist:
            pass
    return JsonResponse(data)
