"""Views for the Network application."""

from typing import Any

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import generic

from network.models import (
    AdditionalAnsibleGroup,
    AnsibleDeviceConfiguration,
    Application,
    Device,
    OperatingSystem,
    Website,
)
from network.wake import Wake


class ListView(generic.ListView):
    """View to see a list of devices."""

    template_name = "network/device_list.html/"
    context_object_name = "device_list"

    def get_queryset(self):
        """
        Get device objects to display in list view.

        Return:
            List of Device objects
        """
        devices = Device.objects.all().order_by("hostname")
        return list(devices)


class WebsitesView(generic.ListView):
    """View to see a list of websites."""

    template_name = "network/websites.html"
    context_object_name = "website_list"

    def get_queryset(self):
        """
        Get investment objects to display in index view.

        Return:
            List of Investment objects
        """
        websites = Website.objects.all().order_by("name")
        return list(websites)


def wake_device(request, pk: int):
    """
    View to handle deleting a website.

    Args:
        request: Request object
        pk: primary key for the website to delete

    Returns:
        Empty response with a 200 code
    """
    if device := Device.objects.filter(pk=pk):
        return (
            HttpResponse(status=200)
            if Wake(device=device[0]).wake()
            else HttpResponse(status=400)
        )
    else:
        return HttpResponse(status=400)


def website_delete(request, pk: int):
    """
    View to handle deleting a website.

    Args:
        request: Request object
        pk: primary key for the website to delete

    Returns:
        Empty response with a 200 code
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    website_item = Website.objects.filter(pk=pk)
    if len(website_item) == 1:
        website_item.delete()
    return HttpResponse(status=200)


def index(request) -> HttpResponse:
    """
    Handle the Network topology index.

    Return:
        HttpResponse for the index page
    """
    return render(request, "network/index.html", {})


def hosts(request) -> HttpResponse:
    """
    Create and output the inventory list for Ansible.

    Args:
        request: HttpRequest object

    Return:
        Inventory list in ini format
    """
    groups: dict[str, dict[str, set[Device]]] = {}

    additional_groups = AdditionalAnsibleGroup.objects.all().order_by("name")

    for additional_group in additional_groups:
        if additional_group.alias not in groups:
            groups[str(additional_group.alias)] = {
                "devices": set(),
                "children": set(),
            }
        if additional_group.parent:
            if additional_group.parent.alias not in groups:
                groups[additional_group.parent.alias] = {
                    "devices": set(),
                    "children": set(additional_group.parent.alias),
                }
            else:
                groups[additional_group.parent.alias]["children"].add(
                    additional_group.alias
                )

    operating_systems = OperatingSystem.objects.all().order_by("name")

    for operating_system in operating_systems:
        if operating_system.alias not in groups:
            groups[str(operating_system.alias)] = {
                "devices": set(),
                "children": set(),
            }
        if operating_system.parent:
            if operating_system.parent.alias not in groups:
                groups[operating_system.parent.alias] = {
                    "devices": set(),
                    "children": {operating_system.alias},
                }
            else:
                groups[operating_system.parent.alias]["children"].add(
                    operating_system.alias
                )

    devices = (
        Device.objects.all()
        .filter(ansible_managed=True, ip_address__isnull=False)
        .order_by("hostname")
    )

    for device in devices:
        groups[device.operating_system.alias]["devices"].add(device)
        for additional_group in device.additional_ansible_groups.all().order_by("name"):
            groups[additional_group.alias]["devices"].add(device)

    output = ""
    for group, value in groups.items():
        output += f"[{group}]\n"
        for device in value["devices"]:
            ansible_config = AnsibleDeviceConfiguration.objects.all().filter(
                for_device=device
            )
            output += f"{device.hostname}\tansible_host={device.ip_address}"
            for config in ansible_config:
                output += f"\t{config.name}={config.value}"
            output += "\n"
        output += "\n"

    for group, value in groups.items():
        if len(value["children"]):
            output += f"[{group}:children]\n"
            for child in value["children"]:
                output += f"{child}\n"
        output += "\n"

    output += "\n"

    return HttpResponse(content_type="text/plain", content=output)


def hosts_zip(request) -> HttpResponse:
    """
    Create and output the inventory list for Ansible.

    Args:
        request: HttpRequest object

    Return:
        Inventory list in ini format
    """
    groups: dict[str, dict[str, set[Device]]] = {}

    operating_systems = OperatingSystem.objects.all()
    applications = Application.objects.all()

    for operating_system in operating_systems:
        if operating_system.name not in groups:
            groups[str(operating_system.name)] = {
                "devices": set(),
                "children": set(),
            }
        if operating_system.parent and operating_system.parent.name not in groups:
            groups[operating_system.parent.name] = {
                "devices": set(),
                "children": {operating_system.name},
            }
        elif operating_system.parent:
            groups[operating_system.parent.name]["children"].add(operating_system.name)

    for application in applications:
        if application not in groups:
            groups[str(application.name)] = {
                "devices": set(),
                "children": set(),
            }

    devices = Device.objects.all().filter(ansible_managed=True)

    for device in devices:
        groups[device.operating_system.name]["devices"].add(device)
        for application in device.applications.all():
            groups[application.name]["devices"].add(device)

    output = ""
    for group, value in groups.items():
        output += f"[{group}]\n"
        for device in value["devices"]:
            output += f"{device.hostname}\tansible_host={device.ip_address}\n"
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

    Args:
        request: HttpRequest object

    Return:
        JsonResponse containing node map of the network
    """
    data: dict[str, list[Any]] = {
        "nodes": [],
        "links": [],
    }
    devices = Device.objects.all()
    for device in devices:
        device_data = {
            "id": f"d{device.pk}",
            "name": device.hostname,
            "ip": str(device.ip_address),
            "description": device.description,
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
            "ip": str(website.hosted_on.ip_address),
            "url": website.full_url,
            "description": website.description,
            "type": "site",
        }
        data["nodes"].append(website_data)
        try:
            link = {
                "source": f"s{website.pk}",
                "target": f"d{website.hosted_on.pk}",
            }
            data["links"].append(link)
        except Device.DoesNotExist:
            pass

    return JsonResponse(data)


def rack(request) -> HttpResponse:
    """
    Handle the Rack page.

    Args:
        request: HttpRequest object

    Return:
        HttpResponse for the rack page
    """
    return render(request, "network/rack.html", {})


def rack_json(request) -> JsonResponse:
    """
    Handle the Rack json.

    Args:
        request: HttpRequest object

    Return:
        JsonResponse for the rack json
    """
    rack_json_res: dict[str, Any] = {}
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
            "image": "/static/img/unknown.png",
            "ip": device.ip_address,
            "description": device.description,
        }
        if device.device_type:
            device_details["image"] = f"/static/img/{device.device_type.image}"
        rack_json_res[device.rack_shelf]["devices"][
            device.rack_shelf_position
        ] = device_details
        if device.rack_shelf_position > rack_json_res[device.rack_shelf]["width"]:
            rack_json_res[device.rack_shelf]["width"] = device.rack_shelf_position
    return JsonResponse(rack_json_res)
