"""Views for Networkv2."""
from typing import Any, Dict, List, Set

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from networkv2.models import Application, Device, OperatingSystem, Website


def index(request) -> HttpResponse:
    """
    Handle the Network topology index.

    Return:
        HttpResponse for the index page
    """
    return render(request, "networkv2/index.html", {})


def inventory(request) -> HttpResponse:
    """
    Create and output the inventory list for Ansible.

    Return:
        Inventory list in ini format
    """
    groups: Dict[str, Dict[str, Set[str]]] = {}

    operating_systems = OperatingSystem.objects.all()
    applications = Application.objects.all()

    for operating_system in operating_systems:
        if operating_system.name_clean not in groups:
            groups[str(operating_system.name_clean)] = {
                "devices": set(),
                "children": set(),
            }
        if operating_system.parent and operating_system.parent.name_clean not in groups:
            groups[operating_system.parent.name_clean] = {
                "devices": set(),
                "children": {operating_system.name},
            }
        elif operating_system.parent:
            groups[operating_system.parent.name_clean]["children"].add(
                operating_system.name_clean
            )

    for application in applications:
        if application.name_clean not in groups:
            groups[str(application.name_clean)] = {
                "devices": set(),
                "children": set(),
            }
        if application.parent and application.parent.name_clean not in groups:
            groups[application.parent.name_clean] = {
                "devices": set(),
                "children": {application.name_clean},
            }
        elif application.parent:
            groups[application.parent.name_clean]["children"].add(
                application.name_clean
            )

    devices = Device.objects.all()

    for device in devices:
        groups[device.operating_system.name_clean]["devices"].add(device)
        for application in device.installed_applications.all():
            groups[application.name_clean]["devices"].add(device)

    output = ""
    for group, value in groups.items():
        output += f"[{group}]\n"
        for device in value["devices"]:
            extra_output = ""
            if device.operating_system.username:
                extra_output += f"\tansible_user={device.operating_system.username}"
            if device.operating_system.password:
                extra_output += f"\tansible_ssh_pass={device.operating_system.password}"
            output += f"{device.hostname}\tansible_host={device.ip}{extra_output}\n"
        output += "\n"

    for group, value in groups.items():
        if len(value["children"]):
            output += f"[{group}:children]\n"
            for child in value["children"]:
                output += f"{child}\n"
        output += "\n"

    output += "\n"

    return HttpResponse(content_type="text/plain", content=output)


def network(request) -> JsonResponse:
    """
    Create and output the node map as a JSON response.

    Return:
        JsonResponse containing node map of the network
    """
    data: Dict[str, List[Any]] = {
        "nodes": [],
        "links": [],
    }
    devices = Device.objects.all()
    for device in devices:
        device_data = {
            "id": f"d{device.pk}",
            "name": device.hostname,
            "ip": str(device.ip),
            "description": device.notes,
            "type": "device",
        }
        data["nodes"].append(device_data)
        if device.connected_too:
            link = {"source": f"d{device.pk}", "target": f"d{device.connected_too.pk}"}
            data["links"].append(link)

    websites = Website.objects.all()
    for website in websites:
        website_data = {
            "id": f"s{website.pk}",
            "name": website.name,
            "ip": str(website.subdomain.hosted_on.ip),
            "url": website.full_url,
            "description": website.description,
            "type": "site",
        }
        data["nodes"].append(website_data)
        try:
            link = {
                "source": f"s{website.pk}",
                "target": f"d{website.subdomain.hosted_on.pk}",
            }
            data["links"].append(link)
        except Device.DoesNotExist:
            pass
    return JsonResponse(data)


def rack(request) -> HttpResponse:
    """
    Handle the Rack page.

    Return:
        HttpResponse for the rack page
    """
    return render(request, "networkv2/rack.html", {})


def rack_json(request) -> JsonResponse:
    """
    Handle the Rack json.

    Return:
        JsonResponse for the rack json
    """
    rack_json_res: Dict[str, Any] = {}
    devices = (
        Device.objects.all()
        .filter(rack_shelf__isnull=False, rack_shelf_position__isnull=False)
        .order_by("rack_shelf", "rack_shelf_position")
    )
    for device in devices:
        if device.rack_shelf not in rack_json_res:
            rack_json_res[device.rack_shelf] = {
                "width": 1,
                "devices": {},
            }
        device_details = {
            "hostname": device.hostname,
            "image": "/static/networkv2/img/unknown.png",
            "ip": device.ip,
            "description": device.notes,
        }
        if device.device_type:
            device_details["image"] = device.device_type.image
        rack_json_res[device.rack_shelf]["devices"][
            device.rack_shelf_position
        ] = device_details
        if device.rack_shelf_position > rack_json_res[device.rack_shelf]["width"]:
            rack_json_res[device.rack_shelf]["width"] = device.rack_shelf_position
    return JsonResponse(rack_json_res)
