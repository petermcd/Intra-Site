"""Models for the Task application."""
from django.db import models


class WishlistItem(models.Model):
    """Model for Wishlist items."""

    name: models.TextField = models.TextField(blank=False)
    quantity: models.IntegerField = models.IntegerField(default=1, blank=False)
    image: models.ImageField = models.ImageField(blank=True)
    price: models.IntegerField = models.IntegerField(default=0, blank=False)
    description: models.TextField = models.TextField(blank=False)
    product_url: models.URLField = models.URLField(blank=False)
    info_url: models.URLField = models.URLField(blank=False)
    in_stock: models.BooleanField = models.BooleanField(default=False, blank=False)

    def __str__(self):
        """Return the name of the product."""
        return self.name
