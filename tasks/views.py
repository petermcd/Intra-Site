"""Views for the Task application."""
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from tasks.models import Task, TaskFrequency


class TaskView(generic.ListView):
    """View to see a list of tasks."""

    template_name = "tasks/index.html"
    context_object_name = "task_list"

    def get_queryset(self):
        """
        Get event objects to display in index view.

        Return:
            List of Task objects
        """
        tasks = Task.objects.all().filter(completed=False).order_by("due_by")
        return list(tasks)


def task_add(request):
    """
    Handle adding a new task item.

    Args:
        request: Request object

    Returns:
        Rendered form
    """
    task_item = Task()
    task_item.title = request.POST["task-title"]
    due_by = datetime.strptime(request.POST["task-due-by"], "%d-%m-%Y %H:%M")
    task_item.due_by = due_by
    if len(request.POST["task-frequency"]) == 1:
        task_frequency = TaskFrequency.objects.filter(
            pk=request.POST["task-frequency"][0]
        )
        if len(task_frequency) == 1:
            task_item.frequency = task_frequency[0]
    task_item.save()
    context = {"task": task_item}
    return render(request, "tasks/partials/task_item.html", context)


def task_complete(request, pk: int):
    """
    View to handle completing a task item.

    Args:
        request: Request object
        pk: primary key for the task item being marked as complete

    Returns:
        Empty response with a 200 code
    """
    task_item = Task.objects.filter(pk=pk)
    if len(task_item) == 1:
        task_frequency = task_item[0].frequency
        if not task_frequency or (
            task_frequency.days_to_add == 0
            and task_frequency.months_to_add == 0
            and task_frequency.years_to_add == 0
        ):
            task_item[0].completed = True
        else:
            dt = relativedelta(
                days=task_frequency.days_to_add,
                months=task_frequency.months_to_add,
                years=task_frequency.years_to_add,
            )
            task_item[0].due_by += dt
        task_item[0].save()
    return HttpResponse(status=200)


def task_output_form(request):
    """
    Handle outputting the form for adding a new task item.

    Args:
        request: Request object

    Returns:
        Rendered form
    """
    context = {"task_frequencies": list(TaskFrequency.objects.all())}
    print(context)
    return render(request, "tasks/partials/task_add_form.html", context)
