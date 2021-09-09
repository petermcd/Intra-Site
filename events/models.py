from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        """
        Standard to string.

        Return:
            String representation of the object
        """
        tmp_dict = [
            self.name,
            self.street_address,
            self.town,
            self.region or '',
            self.country,
            self.postcode,
        ]
        output = [item for item in tmp_dict if item]
        return ', '.join(output)

    def printable(self) -> str:
        """
        Formatted representation of the address.

        Return:
            Formatted address ready for output
        """
        tmp_dict = [
            self.name,
            self.street_address,
            self.town,
            self.region or '',
            self.country,
            self.postcode,
        ]
        output = [item for item in tmp_dict if item]
        return '\n'.join(output)


class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.RESTRICT)
    starting = models.DateTimeField(blank=True, null=True)
    ending = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255)
    ticket_file = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        """
        Standard to string.

        Return:
            String representation of the object
        """
        return self.name


class TransportMethod(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        """
        Standard to string.

        Return:
            String representation of the object
        """
        return self.name


class EventTravel(models.Model):
    method = models.ForeignKey(TransportMethod, on_delete=models.RESTRICT)
    direction = models.CharField(max_length=4, choices=[('To', 'To'), ('From', 'From')])
    event = models.ForeignKey(Event, on_delete=models.RESTRICT)
    venue = models.ForeignKey(Venue, on_delete=models.RESTRICT)
    starting = models.DateTimeField()
    ending = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    @property
    def event_name(self) -> str:
        """
        Fetch the name of the event associated with the travel entry

        Return:
            Event name
        """
        return self.event.name

    @property
    def venue_name(self) -> str:
        """
        Fetch the name of the venue associated with the travel entry

        Return:
            Venue name
        """
        return self.venue.name

    def __str__(self) -> str:
        """
        Standard to string.

        Return:
            String representation of the object
        """
        return f'{self.direction} {self.event.name} at {self.starting} on a {self.method.name}'
