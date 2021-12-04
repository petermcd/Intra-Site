from django.contrib import admin
from django.urls import include, path

from Intranet.views import IndexView
from finance.views import MonzoAuthView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('admin/finance/monzo.html', MonzoAuthView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('books/', include('books.urls')),
    path('events/', include('events.urls')),
    path('network/', include('network.urls')),
]
