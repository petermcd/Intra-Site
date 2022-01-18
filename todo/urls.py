from django.urls import path

from todo import views

app_name = 'todo'
urlpatterns = [
    path('', views.IndexView.as_view(), name='todo'),
    path('add', views.IndexView.as_view(), name='todo'),
    path('delete', views.IndexView.as_view(), name='todo'),
]
