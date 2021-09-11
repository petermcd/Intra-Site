from django.contrib import admin

from books.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    ordering = ['name', ]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'publisher', 'isbn10', 'read')
    ordering = ('title',)

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'books/js/books.js',
        )
