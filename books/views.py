from django.views import generic

from books.models import Book


class IndexView(generic.ListView):
    template_name = 'books/index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class DetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail.html'

    def get_queryset(self):
        return Book.objects.all()
