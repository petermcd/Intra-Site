"""URL configuration for the Books application."""
from django.urls import path

from books.views import AuthorIndexView, DetailView, IndexView, get_book_details

app_name = "books"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("authors/", AuthorIndexView.as_view(), name="authors"),
    path("<int:pk>/", DetailView.as_view(), name="details"),
    path("<str:search_type>/<str:search>", get_book_details, name="book_search"),
]
