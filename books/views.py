from django.views import generic

from books.models import Book


class IndexView(generic.ListView):
    paginate_by = 10
    template_name = 'books/index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        term = self.request.GET.get('q')
        objects = Book.objects.all().order_by('title')
        if term:
            objects = Book.objects.filter(title__icontains=term).order_by('title')
        return objects

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class DetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail.html'

    def get_queryset(self):
        return Book.objects.all()
