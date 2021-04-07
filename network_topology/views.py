from django.http import JsonResponse
from django.shortcuts import render

from network_sites.models import Site

from .models import Device


def index(request):
    return render(request, 'network_topology/index.html', {})


def topology(request):
    data = {
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
            "ip": str(site.ip),
            "url": site.corrected_url,
            "description": site.description,
            "type": 'site'
        }
        data['nodes'].append(site_data)
        try:
            hosting_device = Device.objects.get(ip__exact=site.ip.pk)
            link = {
                "source": f"s{site.pk}",
                "target": f"d{hosting_device.pk}"
            }
            data['links'].append(link)
        except Device.DoesNotExist:
            pass
    return JsonResponse(data)
