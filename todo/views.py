from django.views import generic
from todo.models import ToDo


class IndexView(generic.ListView):
    template_name = 'todo/index.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        """
        Get event objects to display in index view.

        Return:
            List of todo objects
        """
        todos = ToDo.objects.all().order_by('added')
        return list(todos)
