from django.urls import path

from network import views

app_name = 'network'
urlpatterns = [
    path('', views.index, name="index"),
    path('network.json', views.network, name="network"),
]
