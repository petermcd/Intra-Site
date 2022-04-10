"""URL configuration for the Tasks application."""
from django.urls import path

from documents.views import DocumentView, document_delete

app_name = "documents"
urlpatterns = [
    path("", DocumentView.as_view(), name="document_index"),
    path("<int:pk>/delete", document_delete, name="document_delete"),
]
