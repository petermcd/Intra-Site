"""Admin configuration for the Books application."""
from django.contrib import admin

from books.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "title",
        "subtitle",
        "publisher",
        "read",
    )
    ordering = ("title",)
    search_fields = (
        "description",
        "title",
    )

    class Media:
        """Class to add relevant javascript to the admin page."""

        js = (
            "/static/js/books.js",
            "https://unpkg.com/html5-qrcode@2.0.9/dist/html5-qrcode.min.js",
        )
