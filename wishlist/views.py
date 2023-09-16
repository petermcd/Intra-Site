"""Views for the Wishlist application."""
from datetime import datetime
from typing import Any

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import generic

from wishlist.models import WishlistItem
from wishlist.product_details import ProductDetailsFactory, ProductNotFoundException


class Wishlist(generic.ListView):
    """View to see a list of wishlist items."""

    template_name = "wishlist/index.html"
    context_object_name = "wishlist_list"

    def get_queryset(self) -> list[WishlistItem]:
        """
        Get event objects to display in index view.

        Return:
            List of Wishlist objects
        """
        return list(WishlistItem.objects.all().order_by("name"))


class WishlistAdd(generic.ListView):
    """View to add a wishlist item."""

    template_name = "wishlist/partials/wishlist_item.html"
    context_object_name = "wishlist_item"

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        Post event to add a wishlist item.

        Args:
            request: HTTP request object.

        Raises:
            Http404: On inability to locate the product on the shop.

        Returns:
            HttpResponse: Rendered template containing the product details
        """
        product_url = request.POST["product_url"]
        shop = ProductDetailsFactory().shop(url=product_url)
        try:
            product_details = shop.get_product_details()
        except ProductNotFoundException:
            raise Http404()
        item = WishlistItem()
        item.name = product_details.name
        item.image = product_details.product_image
        item.price = product_details.price
        item.description = product_details.description
        item.product_url = product_details.product_url
        item.info_url = product_details.info_url
        item.in_stock = product_details.in_stock
        item.save()
        context = {self.context_object_name: item}
        return render(
            request=request, template_name=self.template_name, context=context
        )


class WishlistIncrease(generic.TemplateView):
    """View to increase the number of an item required."""

    template_name = "wishlist/partials/wishlist_item.html"
    context_object_name = "wishlist_item"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Get request to action an increase in number of items required.

        Args:
            request: HTTP request.
            kwargs: Will contain PK of the item to increase.

        Raises:
            Http404: On inability to locate the product.

        Returns:
            HttpResponse: Rendered template containing the product details.
        """
        try:
            product = WishlistItem.objects.get(pk=kwargs["pk"])
        except WishlistItem.DoesNotExist:
            raise Http404("No such product")
        product.quantity += 1
        product.save()
        context = {self.context_object_name: product}
        return render(
            request=request, template_name=self.template_name, context=context
        )


class WishlistDecrease(generic.ListView):
    """View to decrease the number of an item required."""

    template_name = "wishlist/partials/wishlist_item.html"
    context_object_name = "wishlist_item"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Get request to action a decrease in number of items required.

        Args:
            request: HTTP request.
            kwargs: Will contain PK of the item to decrease.

        Raises:
            Http404: On inability to locate the product.

        Returns:
            HttpResponse: Rendered template containing the product details.
        """
        try:
            product = WishlistItem.objects.get(pk=kwargs["pk"])
        except WishlistItem.DoesNotExist:
            raise Http404("No such product")
        if product.quantity == 1:
            product.delete()
            return HttpResponse("")
        product.quantity -= 1
        product.save()
        context = {self.context_object_name: product}
        return render(
            request=request, template_name=self.template_name, context=context
        )


class WishlistUpdateNext(generic.TemplateView):
    """View to update details of the oldest wishlist item."""

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Update a wishlist item with the oldest last updated date.

        Args:
            request: HTTP request object.

        Return:
            JsonResponse: Wishlist item as JSON.
        """
        item: WishlistItem = WishlistItem.objects.all().order_by("last_updated")[:1][0]
        try:
            shop = ProductDetailsFactory().shop(url=str(item.product_url))
            product_details = shop.get_product_details()
        except ProductNotFoundException:
            return JsonResponse(
                {
                    "result": "failure",
                    "message": "Unable to locate product",
                }
            )
        item.name = product_details.name
        item.image = product_details.product_image
        item.description = product_details.description
        item.price = product_details.price
        item.in_stock = product_details.in_stock
        item.last_updated = datetime.now()
        item.save()
        return JsonResponse(
            {
                "result": "success",
                "item": {
                    "name": item.name,
                    "quantity": item.quantity,
                    "image": item.image,
                    "price": item.price,
                    "description": item.description,
                    "product_url": item.product_url,
                    "info_url": item.info_url,
                    "in_stock": item.in_stock,
                    "last_updated": item.last_updated,
                },
            }
        )


def all_wishlist_json(request) -> JsonResponse:
    """
    View to output wishlist as json.

    Args:
        request: API Request

    Returns:
         HttpResponse
    """
    response: dict[str, list[dict[str, Any]]] = {"wishlist": []}
    wishlist_res = WishlistItem.objects.all()
    for wishlist in wishlist_res:
        wishlist_details = {
            "name": wishlist.name,
            "quantity": wishlist.quantity,
            "price": wishlist.price,
            "url": wishlist.product_url,
            "description": wishlist.description,
        }
        response["wishlist"].append(wishlist_details)
    return JsonResponse(response)
