from typing import Any, Dict, List

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from networkv2.models import Device, Website


def index(request) -> HttpResponse:
    """
    Handle the Network topology index

    Return:
        HttpResponse for the index page
    """
    return render(request, 'networkv2/index.html', {})


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
            "ip": str(website.subdomain.hosted_on.ip),
            "url": website.full_url,
            "description": website.description,
            "type": 'site'
        }
        data['nodes'].append(website_data)
        try:
            link = {
                "source": f"s{website.pk}",
                "target": f"d{website.subdomain.hosted_on.pk}"
            }
            data['links'].append(link)
        except Device.DoesNotExist:
            pass
    return JsonResponse(data)
