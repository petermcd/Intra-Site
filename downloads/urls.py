"""URLs for Downloads."""
from django.urls import path

from downloads import views

app_name = "downloads"
urlpatterns = [
    path("books/<str:book>", views.book_download, name="book-download"),
    path("documents/<str:document>", views.document_download, name="event-ticket"),
    path(
        "event-tickets/<str:event_ticket>",
        views.event_ticket_download,
        name="event-ticket",
    ),
    path(
        "travel-tickets/<str:travel_ticket>",
        views.travel_ticket_download,
        name="travel-ticket",
    ),
]
