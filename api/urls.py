"""URLs for API."""
from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("book/<str:search_type>/<str:search>", views.get_book_details),
]
