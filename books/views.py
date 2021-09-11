from django.views import generic

from books.models import Book


class IndexView(generic.ListView):
    paginate_by = 10
    template_name = 'books/index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        """
        Get book objects to display in index view matching the optional get query.

        Return:
            List of book objects
        """
        term = self.request.GET.get('q')
        objects = Book.objects.all().order_by('title')
        if term:
            objects = Book.objects.filter(title__icontains=term).order_by('title')
        return objects

    def get_context_data(self, **kwargs):
        """
        Retrieve context data ready for output

        Return:
            Context data ready for output in a template
        """
        term = ''
        if 'q' in self.request.GET:
            term = f'&q={self.request.GET["q"]}'
        context = super().get_context_data(**kwargs)
        context['search_term'] = term
        return context


class DetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail.html'

    def get_queryset(self):
        """
        Get book objects to display in detail view.

        Return:
            List of book objects
        """
        return Book.objects.all()
