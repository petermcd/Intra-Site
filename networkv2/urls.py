from django.urls import path

from networkv2 import views

app_name = 'networkv2'
urlpatterns = [
    path('', views.index, name="index"),
    path('network.json', views.network, name="network"),
    path('rack.html', views.rack, name="rack"),
]
