"""Primary URL configuration for the Intranet site."""
from django.contrib import admin
from django.urls import include, path

from intranet.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("books/", include("books.urls")),
    path("documents/", include("documents.urls")),
    path("downloads/", include("downloads.urls")),
    path("finance/", include("finance.urls")),
    path("tasks/", include("tasks.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
