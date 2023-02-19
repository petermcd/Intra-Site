"""URL configuration for the network application."""
from django.urls import path

from network import views

app_name = "network"
urlpatterns = [
    path("", views.index, name="index"),
    path("hosts", views.hosts, name="hosts"),
    path("hosts.zip", views.hosts_zip, name="hosts.zip"),
    path("list/", views.ListView.as_view(), name="list"),
    path("network.json", views.network, name="network"),
    path("rack/", views.rack, name="rack"),
    path("rack.json", views.rack_json, name="rack.json"),
    path("wake/<int:pk>/", views.wake_device, name="wake"),
    path("websites/", views.WebsitesView.as_view(), name="websites"),
    path("websites/websites.json", views.websites_json, name="websites_json"),
    path("websites/<int:pk>/delete", views.website_delete, name="website_delete"),
]
