"""Models for the Finance application."""
from django.db import models

from intranet.helpers import OverwriteStorageName

TRAVEL_DIRECTION_CHOICES = [
    ("To", "To"),
    ("During", "During"),
    ("From", "From"),
]


def ticket_file_name(instance, filename: str) -> str:
    """
    Create filename for event ticket.

    Args:
        instance: Model class uploading the file
        filename: The name of the file uploaded

    Returns: String containing the new filename
    """
    path: str = "SiteDocuments/event-tickets/"
    ext: str = filename.split(".")[-1]
    return f"{path}{instance.name}-{instance.venue.name}-{instance.start}.{ext}"


def travel_file_name(instance, filename) -> str:
    """
    Create filename for travel ticket.

    Args:
        instance: Model class uploading the file
        filename: The name of the file uploaded

    Returns: String containing the new filename
    """
    path: str = "SiteDocuments/travel-tickets/"
    ext: str = filename.split(".")[-1]
    return f"{path}{instance.departing_station.name}-{instance.departure}.{ext}"


class Venue(models.Model):
    """Model for Venue."""

    name: models.CharField = models.CharField(max_length=255)
    street_address: models.CharField = models.CharField(max_length=255)
    city: models.CharField = models.CharField(max_length=255)
    country: models.CharField = models.CharField(max_length=255)
    postcode: models.CharField = models.CharField(max_length=255)

    class Meta:
        """Meta class."""

        verbose_name = "Venue"
        verbose_name_plural = "Venues"

    def __str__(self) -> str:
        """
        To string for Venue.

        Returns:
            The name and city of the venue
        """
        return f"{self.name} - {self.city}"

    @property
    def printable(self) -> str:
        """
        Printable representation of the model.

        Returns:
            Printable version of the venue as a string
        """
        return f"{self.name}\n{self.street_address}\n{self.city}\n{self.country}\n{self.postcode}"

    @property
    def csv(self) -> str:
        """
        Printable representation of the model.

        Returns:
            Printable version of the venue as a string
        """
        return f"{self.name},{self.street_address},{self.city},{self.country},{self.postcode}"


class Station(models.Model):
    """Model for Station."""

    name: models.CharField = models.CharField(max_length=255)
    street_address: models.CharField = models.CharField(max_length=255)
    city: models.CharField = models.CharField(max_length=255)
    country: models.CharField = models.CharField(max_length=255)
    postcode: models.CharField = models.CharField(max_length=255)

    class Meta:
        """Meta class."""

        verbose_name = "Station"
        verbose_name_plural = "Stations"

    def __str__(self) -> str:
        """
        To string for Station.

        Returns:
            The name and cite of the Station
        """
        return f"{self.name} - {self.city}"


class Event(models.Model):
    """Model for an event."""

    name: models.CharField = models.CharField(max_length=255)
    description: models.TextField = models.TextField(max_length=1000)
    venue: models.ForeignKey = models.ForeignKey(
        Venue, on_delete=models.RESTRICT, null=True
    )
    start: models.DateTimeField = models.DateTimeField()
    ends: models.DateTimeField = models.DateTimeField()
    ticket_file: models.FileField = models.FileField(
        storage=OverwriteStorageName, null=True, blank=True, upload_to=ticket_file_name
    )

    class Meta:
        """Meta class."""

        verbose_name = "Event"
        verbose_name_plural = "Events"

        constraints = [
            models.CheckConstraint(
                check=models.Q(models.Q(ends__gte=models.F("start"))),
                name="event_ends_after_start",
            ),
        ]

    def __str__(self) -> str:
        """
        To string for Event.

        Returns:
            The name of the Event
        """
        return str(self.name)

    @property
    def accommodation_arranged(self) -> str:
        """
        Property to identify if accommodation has been arranged.

        Returns:
            Yes or no
        """
        accommodation = Accommodation.objects.filter(for_event__exact=self)
        return "Yes" if accommodation else "No"

    @property
    def travel_arranged(self) -> str:
        """
        Property to identify if travel has been arranged.

        Returns:
            Yes, partial or no
        """
        arranged = "No"
        t_to = Travel.objects.filter(for_event__exact=self, direction__exact="To")
        t_from = Travel.objects.filter(for_event__exact=self, direction__exact="From")
        if all([t_to, t_from]):
            arranged = "Yes"
        elif any([t_to, t_from]):
            arranged = "Partial"
        return arranged


class TravelType(models.Model):
    """Model for travel type."""

    name: models.CharField = models.CharField(max_length=255)

    class Meta:
        """Meta class."""

        verbose_name = "Travel type"
        verbose_name_plural = "Travel types"

    def __str__(self) -> str:
        """
        To string for TravelType.

        Returns:
            Travel type name as a string
        """
        return str(self.name)


class Travel(models.Model):
    """Model for Travel."""

    travel_type: models.ForeignKey = models.ForeignKey(
        TravelType,
        null=False,
        on_delete=models.RESTRICT,
        related_name="travel_type",
    )
    departing_station: models.ForeignKey = models.ForeignKey(
        Station,
        null=False,
        on_delete=models.RESTRICT,
        related_name="departing_station",
    )
    departure: models.DateTimeField = models.DateTimeField()
    arrival_station: models.ForeignKey = models.ForeignKey(
        Station,
        null=False,
        on_delete=models.RESTRICT,
        related_name="arrival_station",
    )
    arrival: models.DateTimeField = models.DateTimeField()
    direction: models.CharField = models.CharField(
        max_length=6, choices=TRAVEL_DIRECTION_CHOICES
    )
    for_event: models.ForeignKey = models.ForeignKey(
        Event,
        null=False,
        on_delete=models.CASCADE,
        related_name="event",
    )
    ticket_file = models.FileField(
        storage=OverwriteStorageName, null=True, blank=True, upload_to=travel_file_name
    )
    notes: models.TextField = models.TextField(max_length=500)

    class Meta:
        """Meta class."""

        verbose_name = "Travel"
        verbose_name_plural = "Travel"

    def __str__(self) -> str:
        """
        To string for Travel.

        Returns:
            The event name, departing station and arrival station for the Travel
        """
        return f"{self.for_event.name}: {self.departing_station.name} -> {self.arrival_station.name}"


class Hotel(models.Model):
    """Model for Hotels."""

    name: models.CharField = models.CharField(max_length=255)
    street_address: models.CharField = models.CharField(max_length=255)
    city: models.CharField = models.CharField(max_length=255)
    country: models.CharField = models.CharField(max_length=255)
    postcode: models.CharField = models.CharField(max_length=255)

    class Meta:
        """Meta class."""

        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"

    def __str__(self) -> str:
        """
        To string for Venue.

        Returns:
            The name and city of the venue
        """
        return f"{self.name} - {self.city}"


class Accommodation(models.Model):
    """Model for accommodation."""

    hotel: models.ForeignKey = models.ForeignKey(
        Hotel,
        null=False,
        on_delete=models.RESTRICT,
        related_name="event_hotel",
    )
    for_event: models.ForeignKey = models.ForeignKey(
        Event,
        null=False,
        on_delete=models.CASCADE,
        related_name="event_accommodation",
    )
    check_in: models.DateTimeField = models.DateTimeField(verbose_name="Check In")
    check_out: models.DateTimeField = models.DateTimeField(verbose_name="Check Out")

    class Meta:
        """Meta class."""

        verbose_name = "Accommodation"
        verbose_name_plural = "Accommodation"

        constraints = [
            models.CheckConstraint(
                check=models.Q(check_out__gt=models.F("check_in")),
                name="accommodation_check_in_before_checkout",
            ),
        ]

    def __str__(self) -> str:
        """
        To string for accommodation.

        Returns:
            The name of the accommodation and event
        """
        return f"{self.for_event.name} - {self.hotel.name}"
