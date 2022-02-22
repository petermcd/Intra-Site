from django.urls import path

from todo import views

app_name = 'todo'
urlpatterns = [
    path('', views.TodoList.as_view(), name='todo_list'),
    path('form', views.todo_output_form, name='todo_add_form'),
    path('add', views.todo_add, name='todo_add'),
    path('<int:pk>/delete', views.todo_delete, name='todo_delete'),
]
