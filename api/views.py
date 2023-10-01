"""Views for the API app."""
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets

from books.models import Author, Book
from network.models import Device, DeviceType, Model, OperatingSystem, Website
from wishlist.models import WishlistItem


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer to represent the Author model."""

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = Author
        fields = [
            "url",
            "name",
        ]


class BookSerializer(serializers.ModelSerializer):
    """Serializer to represent the Book model."""

    authors = AuthorSerializer(many=True)

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = Book
        fields = [
            "authors",
            "description",
            "isbn10",
            "isbn13",
            "published",
            "publisher",
            "subtitle",
            "thumbnail",
            "title",
            "url",
        ]
        depth = 1


class DeviceTypeSerializer(serializers.ModelSerializer):
    """Serializer to represent the DeviceType model."""

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = DeviceType
        fields = [
            "name",
            "image",
        ]


class ModelSerializer(serializers.ModelSerializer):
    """Serializer to represent the Model model."""

    vendor = serializers.ReadOnlyField(source="vendor.name")

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = Model
        fields = [
            "name",
            "vendor",
        ]


class OSSerializer(serializers.ModelSerializer):
    """Serializer to represent the OperatingSystem model."""

    vendor = serializers.ReadOnlyField(source="vendor.name")

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = OperatingSystem
        fields = [
            "name",
            "vendor",
        ]


class WebsiteSerializer(serializers.ModelSerializer):
    """Serializer to represent the Website model."""

    hosted_on = serializers.ReadOnlyField(source="hosted_on.hostname")

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = Website
        fields = [
            "name",
            "full_url",
            "description",
            "hosted_on",
        ]


class WhoAmISerializer(serializers.ModelSerializer):
    """Serializer to represent the current user."""

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = User
        fields = ["url", "username", "email", "is_staff"]


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer to represent the WishlistItem model."""

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = WishlistItem
        fields = [
            "url",
            "name",
            "quantity",
            "image",
            "price",
            "description",
            "product_url",
            "info_url",
            "in_stock",
            "last_updated",
        ]


class NetworkSerializer(serializers.ModelSerializer):
    """Serializer to represent the Device model."""

    operating_system = OSSerializer()
    model = ModelSerializer()
    device_type = DeviceTypeSerializer()
    connected_too = serializers.ReadOnlyField(source="connected_too.hostname")

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = Device
        fields = [
            "url",
            "hostname",
            "ip_address",
            "mac_address",
            "operating_system",
            "model",
            "device_type",
            "connected_too",
            "description",
        ]


class AuthorViewSet(viewsets.ModelViewSet):
    """Viewset to represent the Author model."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """Viewset to represent the Book model."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    """Viewset to represent the Device model."""

    queryset = Device.objects.all()
    serializer_class = NetworkSerializer


class WebsiteViewSet(viewsets.ModelViewSet):
    """Viewset to represent the Website model."""

    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    """Viewset to represent the WishlistItem model."""

    queryset = WishlistItem.objects.all()
    serializer_class = WishlistSerializer


class WhoAmIViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to represent the current user."""

    queryset = User.objects.all()
    serializer_class = WhoAmISerializer

    def get_object(self):
        """Return the current user."""
        pk = self.kwargs.get("pk")
        return self.request.user if pk == "current" else super().get_object()
