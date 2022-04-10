"""URL configuration for the Tasks application."""
from django.urls import path

from downloads.views import DownloadView

app_name = "downloads"
urlpatterns = [
    path("<str:directory>/<str:filename>", DownloadView, name="file-download"),
]
