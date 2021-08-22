from django.urls import path

from books import views

app_name = 'books'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('<int:pk>/', views.DetailView.as_view(), name="index"),
]