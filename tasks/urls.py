"""URL configuration for the Tasks application."""
from django.urls import path

from tasks.views import TaskView, task_add, task_complete, task_output_form

app_name = "tasks"
urlpatterns = [
    path("", TaskView.as_view(), name="task_index"),
    path("form", task_output_form, name="task_add_form"),
    path("add", task_add, name="task_add"),
    path("<int:pk>/complete", task_complete, name="task_complete"),
]
