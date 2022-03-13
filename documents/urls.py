"""URLs for Documents."""
from django.urls import path

from documents import views

app_name = "documents"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
