from django.contrib import admin
from django.urls import include, path

from finance.views import MonzoAuthView
from Intranet.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('admin/finance/monzo.html', MonzoAuthView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('books/', include('books.urls')),
    path('documents/', include('documents.urls')),
    path('downloads/', include('downloads.urls')),
    path('events/', include('events.urls')),
    path('finance/', include('finance.urls')),
    path('networkv2/', include('networkv2.urls')),
    path('todo/', include('todo.urls')),
]
