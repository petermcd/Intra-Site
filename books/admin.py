from django.contrib import admin

from books.models import Author, Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'isbn10', 'read')
    ordering = ('title',)

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'books/js/books.js',
        )


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
