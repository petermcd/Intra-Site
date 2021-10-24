from django.contrib import admin

from books.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('title', 'subtitle', 'publisher', 'read',)
    ordering = ('title',)

    class Media:
        js = (
            'books/js/books.js',
        )

