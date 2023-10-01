"""Primary URL configuration for the Intranet site."""
from django.contrib import admin
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic.base import RedirectView

from intranet.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("books/", include("books.urls")),
    path("documents/", include("documents.urls")),
    path("SiteDocuments/", include("downloads.urls")),
    path("events/", include("events.urls")),
    path("favicon.ico", RedirectView.as_view(url=static("img/favicon.ico"))),
    path("finance/", include("finance.urls")),
    path("network/", include("network.urls")),
    path("tasks/", include("tasks.urls")),
    path("wishlist/", include("wishlist.urls")),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("api/", include("api.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
