"""Views for the Wishlist application."""
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import generic

from wishlist.models import WishlistItem
from wishlist.product_details import ProductDetailsFactory, ProductNotFoundException


class Wishlist(generic.ListView):
    """View to see a list of qishlist items."""

    template_name = "wishlist/index.html"
    context_object_name = "wishlist_list"

    def get_queryset(self) -> list[WishlistItem]:
        """
        Get event objects to display in index view.

        Return:
            List of Wishlist objects
        """
        wishlist = WishlistItem.objects.all().order_by("name")
        return list(wishlist)


class WishlistAdd(generic.ListView):
    """View to add a wishlist item."""

    template_name = "wishlist/partials/wishlist_item.html"
    context_object_name = "wishlist_item"

    def post(self, request, *args, **kwargs):
        """
        Post event to add a wishlist item.

        Args:
            request: HTTP request object.
        """
        product_url = request.POST["product_url"]
        shop = ProductDetailsFactory().shop(url=product_url)
        try:
            product_details = shop.get_product_details(url=product_url)
        except ProductNotFoundException:
            return Http404()
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

    def get(self, request, *args, **kwargs):
        """
        Get request to action an increase in number of items required.

        Args:
            request: HTTP request.
            kwargs: Will contain PK of the item to increase.
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

    def get(self, request, *args, **kwargs):
        """
        Get request to action a decrease in number of items required.

        Args:
            request: HTTP request.
            kwargs: Will contain PK of the item to decrease.
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
