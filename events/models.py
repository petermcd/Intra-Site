from django.db import models

from Intranet.misc import OverwriteStorage

TRAVEL_DIRECTION_CHOICES = [
    ('To', 'To'),
    ('From', 'From'),
]


def ticket_file_name(instance, filename) -> str:
    """
    Create filename for event ticket.

    Args:
        instance: Model class uploading the file
        filename: The name of the file uploaded

    Returns: String containing the new filename
    """
    path = 'downloads/event-tickets/'
    ext = filename.split('.')[-1]
    filename = f'{path}{instance.name}-{instance.venue.name}-{instance.start}.{ext}'
    return filename


def travel_file_name(instance, filename) -> str:
    """
    Create filename for travel ticket.

    Args:
        instance: Model class uploading the file
        filename: The name of the file uploaded

    Returns: String containing the new filename
    """
    path = 'downloads/travel-tickets/'
    ext = filename.split('.')[-1]
    filename = f'{path}{instance.departing_station.name}-{instance.departure}.{ext}'
    return filename


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

    @property
    def printable(self) -> str:
        """
        Printable representation of the model.

        Returns:
            Printable version of the venue as a string
        """
        return f'{self.name}\n{self.street_address}\n{self.city}\n{self.country}\n{self.postcode}'


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
    ticket_file = models.FileField(storage=OverwriteStorage, null=True, blank=True, upload_to=ticket_file_name)
    notes = models.TextField(max_length=500)

    def __str__(self) -> str:
        """
        To string for Event.

        Returns:
            The name of the Event
        """
        return self.name

    @property
    def accommodation_arranged(self) -> str:
        """
        Property to identify if accommodation has been arranged.

        Returns:
            Yes or no
        """
        arranged = 'No'
        accommodation = Accommodation.objects.filter(for_event__exact=self)
        if accommodation:
            arranged = 'Yes'
        return arranged

    @property
    def travel_arranged(self) -> str:
        """
        Property to identify if travel has been arranged.

        Returns:
            Yes, partial or no
        """
        arranged = 'No'
        t_to = Travel.objects.filter(for_event__exact=self, direction__exact='To')
        t_from = Travel.objects.filter(for_event__exact=self, direction__exact='From')
        if all([t_to, t_from]):
            arranged = 'Yes'
        elif any([t_to, t_from]):
            arranged = 'Partial'
        return arranged


class TravelType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')

    def __str__(self) -> str:
        """
        To string for TravelType.

        Returns:
            Travel type name as a string
        """
        return self.name


class Travel(models.Model):
    """
    Model for Travel
    """
    travel_type = models.ForeignKey(
        TravelType,
        verbose_name='Travel Type',
        null=False,
        on_delete=models.RESTRICT,
        related_name='travel_type'
    )
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
    ticket_file = models.FileField(storage=OverwriteStorage, null=True, blank=True, upload_to=travel_file_name)
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


class Hotel(models.Model):
    """
    Model for Hotels.
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


class Accommodation(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        verbose_name='Hotel',
        null=False,
        on_delete=models.RESTRICT,
        related_name='event_hotel'
    )
    for_event = models.ForeignKey(
        Event,
        verbose_name='Event',
        null=False,
        on_delete=models.RESTRICT,
        related_name='event_accommodation'
    )
    check_in = models.DateTimeField(verbose_name='Check In')
    check_out = models.DateTimeField(verbose_name='Check Out')
