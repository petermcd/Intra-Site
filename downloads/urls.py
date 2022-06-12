"""URL configuration for the Tasks application."""
from django.urls import path

from downloads.views import download_view

app_name = "downloads"
urlpatterns = [
    path("<str:directory>/<str:filename>", download_view, name="file-download"),
]
