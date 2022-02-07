from django.urls import path

from networkv2 import views

app_name = 'networkv2'
urlpatterns = [
    path('', views.index, name="index"),
    path('inventory.ini', views.inventory, name="inventory"),
    path('network.json', views.network, name="network"),
    path('rack', views.rack, name="rack"),
    path('rack.json', views.rack_json, name="rack.json"),
]
