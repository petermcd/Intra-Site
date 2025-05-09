"""URL configuration for the Events application."""

from django.urls import path

from events.views import DetailView, IndexView, event_delete

app_name = "events"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:pk>/", DetailView.as_view(), name="details"),
    path("<int:pk>/delete", event_delete, name="event_delete"),
]
