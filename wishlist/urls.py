"""URL configuration for the Tasks application."""
from django.urls import path

from wishlist.views import (
    Wishlist,
    WishlistAdd,
    WishlistDecrease,
    WishlistIncrease,
    WishlistUpdateNext,
    all_wishlist_json,
)

app_name = "wishlist"
urlpatterns = [
    path("", Wishlist.as_view(), name="task_index"),
    path("additem", WishlistAdd.as_view(), name="wishlist_add"),
    path("<int:pk>/increase", WishlistIncrease.as_view(), name="wishlist_increase"),
    path("<int:pk>/decrease", WishlistDecrease.as_view(), name="wishlist_decrease"),
    path("update_next", WishlistUpdateNext.as_view(), name="wishlist_decrease"),
    path("wishlist.json", all_wishlist_json, name="wishlist_jsone"),
]
