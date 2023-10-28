"""Primary URL configuration for the Intranet site."""
from django.urls import include, path
from rest_framework import routers

from api.views import (
    AuthorViewSet,
    BillViewSet,
    BookViewSet,
    InvestmentViewSet,
    NetworkViewSet,
    WebsiteViewSet,
    WhoAmIViewSet,
    WishlistViewSet,
)

router = routers.DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"books", BookViewSet)
router.register(r"finance/bills", BillViewSet)
router.register(r"finance/investments", InvestmentViewSet)
router.register(r"network", NetworkViewSet)
router.register(r"websites", WebsiteViewSet)
router.register(r"whoami", WhoAmIViewSet)
router.register(r"wishlist", WishlistViewSet)

urlpatterns = [
    path("", include(router.urls), name="api"),
]
