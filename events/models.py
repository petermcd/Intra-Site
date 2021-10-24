from django.core.files.storage import FileSystemStorage
from django.db import models

from Intranet.settings import (BASE_EXTERNAL_STORAGE_URL,
                               BASE_LOCAL_PATH_FOR_EXTERNAL)

TRAVEL_DIRECTION_CHOICES = [
    ('To', 'To'),
    ('From', 'From'),
]

event_fs = FileSystemStorage(
    location=f'{BASE_LOCAL_PATH_FOR_EXTERNAL}/events', base_url=f'{BASE_EXTERNAL_STORAGE_URL}/events'
)
travel_fs = FileSystemStorage(
    location=f'{BASE_LOCAL_PATH_FOR_EXTERNAL}/travel', base_url=f'{BASE_EXTERNAL_STORAGE_URL}/travel'
)


class Venue(models.Model):
    """
    Model for Venue.
    """
    name = models.CharField(max_length=255, verbose_name='Name')
    street_address = models.CharField(max_length=255, verbose_name='Street Address')
    city = models.CharField(max_length=255, verbose_name='City')
    country = models.CharField(max_length=255, verbose_name='Country')
    postcode = models.CharField(max_length=255, verbose_name='Postcode')

    def __str__(self) -> str:
        """
        To string for Venue.

        Returns:
            The name and city of the venue
        """
        return f'{self.name} - {self.city}'


class Station(models.Model):
    """
    Model for Station.
    """
    name = models.CharField(max_length=255, verbose_name='Name')
    street_address = models.CharField(max_length=255, verbose_name='Street Address')
    city = models.CharField(max_length=255, verbose_name='City')
    country = models.CharField(max_length=255, verbose_name='Country')
    postcode = models.CharField(max_length=255, verbose_name='Postcode')

    def __str__(self) -> str:
        """
        To string for Station.

        Returns:
            The name and cite of the Station
        """
        return f'{self.name} - {self.city}'


class Event(models.Model):
    """
    Model for an event
    """
    name = models.CharField(max_length=255, verbose_name='Name')
    description = models.CharField(max_length=1000, verbose_name='Description')
    venue = models.ForeignKey(Venue, on_delete=models.RESTRICT)
    start = models.DateTimeField(verbose_name='Starts')
    ends = models.DateTimeField(verbose_name='Ends')
    ticket_file = models.FileField(storage=event_fs, null=True, blank=True)
    notes = models.TextField(max_length=500)

    def __str__(self) -> str:
        """
        To string for Event.

        Returns:
            The name of the Event
        """
        return self.name


class Travel(models.Model):
    """
    Model for Travel
    """
    departing_station = models.ForeignKey(
        Station,
        verbose_name='Departing Station',
        null=False,
        on_delete=models.RESTRICT,
        related_name='departing_station'
    )
    departure = models.DateTimeField(verbose_name='Departure')
    arrival_station = models.ForeignKey(
        Station, verbose_name='Arrival Station', null=False, on_delete=models.RESTRICT, related_name='arrival_station'
    )
    arrival = models.DateTimeField(verbose_name='Arrival')
    direction = models.CharField(max_length=4, choices=TRAVEL_DIRECTION_CHOICES)
    for_event = models.ForeignKey(
        Event, verbose_name='For Event', null=False, on_delete=models.RESTRICT, related_name='event'
    )
    ticket_file = models.FileField(storage=travel_fs, null=True, blank=True)
    notes = models.TextField(max_length=500)

    def __str__(self) -> str:
        """
        To string for Travel.

        Returns:
            The event name, departing station and arrival station for the Travel
        """
        return f'{self.for_event.name}: {self.departing_station.name} -> {self.arrival_station.name}'

    class Meta:
        """
        Meta class to set the menu name for the object.
        """
        verbose_name = 'Travel'
        verbose_name_plural = 'Travel'
