"""Views for Todo."""
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from todo.models import ToDo


class TodoList(generic.ListView):
    """View implementation for todo list."""

    template_name = "todo/index.html"
    context_object_name = "todo_list"

    def get_queryset(self):
        """
        Get event objects to display in index view.

        Return:
            List of todo objects
        """
        todos = ToDo.objects.all().order_by("added")
        return list(todos)


def todo_output_form(request):
    """
    Handle outputting the form for adding a new todo item.

    Args:
        request: Request object

    Returns:
        Rendered form
    """
    context = {}
    return render(request, "todo/partials/todo_add_form.html", context)


def todo_add(request):
    """
    Handle adding a new todo item.

    Args:
        request: Request object

    Returns:
        Rendered form
    """
    todo_item = ToDo()
    todo_item.description = request.POST["todo-text"]
    todo_item.save()
    context = {"todo": todo_item}
    return render(request, "todo/partials/todo_item.html", context)


def todo_delete(request, pk: int):
    """
    View to handle deleting a todo item.

    Args:
        request: Request object
        pk: primary key for the todo item being deleted

    Returns:
        Empty response with a 204 code
    """
    todo_item = ToDo.objects.filter(pk=pk)
    if len(todo_item) == 1:
        todo_item[0].delete()
    return HttpResponse(status=200)
