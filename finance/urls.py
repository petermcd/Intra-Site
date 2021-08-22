from django.urls import path

from . import views

app_name = 'finance'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('debt/<int:pk>/', views.DetailView.as_view(), name='debt_detail'),
]
