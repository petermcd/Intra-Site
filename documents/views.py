from django.views import generic

from documents.models import Document


class IndexView(generic.ListView):
    paginate_by = 10
    template_name = "documents/index.html"
    context_object_name = "document_list"

    def get_queryset(self):
        """
        Get document objects to display in index view matching the optional get query.

        Return:
            List of document objects
        """
        term = self.request.GET.get("q")
        objects = Document.objects.all().order_by("name")
        if term:
            objects = Document.objects.filter(name__icontains=term).order_by("name")
        return objects

    def get_context_data(self, **kwargs):
        """
        Retrieve context data ready for output

        Return:
            Context data ready for output in a template
        """
        term = ""
        if "q" in self.request.GET:
            term = f'&q={self.request.GET["q"]}'
        context = super().get_context_data(**kwargs)
        context["search_term"] = term
        return context
