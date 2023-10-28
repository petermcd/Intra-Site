"""Views for the API app."""
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response as response

from books.models import Author, Book
from finance.models import Bill, BillHistory, Investments, InvestmentValue
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


class BillSerializer(serializers.ModelSerializer):
    """Serializer to represent the Bill model."""

    bill_type = serializers.ReadOnlyField(source="bill_type.name")
    organisation = serializers.ReadOnlyField(source="organisation.name")
    paid_from = serializers.ReadOnlyField(source="paid_from.name")

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = Bill
        fields = [
            "url",
            "name",
            "description",
            "organisation",
            "bill_type",
            "due_day",
            "monthly_payments",
            "current_balance",
            "apr",
            "start_date",
            "last_payment",
            "paid_from",
        ]


class BillHistorySerializer(serializers.ModelSerializer):
    """Serializer to represent the BillHistory model."""

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = BillHistory
        fields = [
            "url",
            "bill",
            "current_balance",
            "date",
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


class InvestmentSerializer(serializers.ModelSerializer):
    """Serializer to represent the Investment model."""

    organisation = serializers.ReadOnlyField(source="organisation.name")

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = Investments
        fields = [
            "description",
            "organisation",
            "current_value",
            "date_purchased",
        ]


class InvestmentHistorySerializer(serializers.ModelSerializer):
    """Serializer to represent the InvestmentValue model."""

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""

        model = InvestmentValue
        fields = [
            "value",
            "date",
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


class BillViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to represent the Bill model."""

    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    @action(detail=False)
    def bills_for_month(self, request):
        """Return the bills for the given month and year."""
        month = (
            int(request.query_params.get("month", datetime.now().month))
            or datetime.now().month
        )
        year = (
            int(request.query_params.get("year", datetime.now().year))
            or datetime.now().year
        )
        search_date = timezone.make_aware(datetime(year=year, month=month, day=1))
        queryset = Bill.objects.all().order_by("name")
        bills = queryset.filter(
            Q(start_date__lte=search_date)
            & Q(Q(last_payment__isnull=True) | Q(last_payment__gte=search_date)),
        )
        serializer = BillSerializer(bills, many=True)
        return response(serializer.data)

    @action(detail=True)
    def history(self, request, pk=None) -> response:
        """Return the history for the given bill."""
        filter_args = {}
        queryset = BillHistory.objects.all().order_by("date")
        if pk:
            filter_args["pk"] = pk
        if "year" in request.query_params:
            year: int = (
                int(request.query_params.get("year", datetime.now().year))
                or datetime.now().year
            )
            start_date: datetime = timezone.make_aware(
                datetime(year=year, month=1, day=1)
            )
            end_date: datetime = timezone.make_aware(
                datetime(year=year + 1, month=1, day=1)
            )
            filter_args = {
                "date__gte": start_date,
                "date__lte": end_date,
            }
        bill_history = queryset.filter(**filter_args)
        serializer = BillHistorySerializer(bill_history, many=True)
        return response(serializer.data)


class InvestmentViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to represent the Investment model."""

    queryset = Investments.objects.all()
    serializer_class = InvestmentSerializer

    @action(detail=True)
    def history(self, request, pk=None):
        """Return the history for the given investment."""
        filter_args = {}
        queryset = InvestmentValue.objects.all().order_by("date")
        if pk:
            filter_args["pk"] = pk
        if "year" in request.query_params:
            year = (
                int(request.query_params.get("year", datetime.now().year))
                or datetime.now().year
            )
            start_date = timezone.make_aware(datetime(year=year, month=1, day=1))
            end_date = timezone.make_aware(datetime(year=year + 1, month=1, day=1))
            filter_args = {
                "date__gte": start_date,
                "date__lte": end_date,
            }
        investment_history = queryset.filter(**filter_args)
        serializer = InvestmentHistorySerializer(investment_history, many=True)
        return response(serializer.data)
