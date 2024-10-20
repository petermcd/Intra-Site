"""Views for the Task application."""
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.http import require_GET

from documents.models import Document


class DocumentView(generic.ListView):
    """View to see a list of documents."""

    template_name = "documents/index.html"
    context_object_name = "document_list"

    def get_queryset(self):
        """
        Get document objects to display in index view.

        Return:
            List of Document objects
        """
        documents = Document.objects.all().order_by("title")
        return list(documents)


@require_GET
def document_delete(request, pk: int) -> HttpResponse:
    """
    View to handle deleting a document item.

    Args:
        request: Request object
        pk: primary key for the document item being deleted

    Returns:
        Empty response with a 200 code
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    document_item = Document.objects.filter(pk=pk)
    if len(document_item) == 1:
        document_item.delete()
    return HttpResponse(status=200)
