from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)

    def __str__(self):
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

    def printable(self):
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
        return self.name


class TransportMethod(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class EventTravel(models.Model):
    method = models.ForeignKey(TransportMethod, on_delete=models.RESTRICT)
    direction = models.CharField(max_length=4, choices=[('To', 'To'), ('From', 'From')])
    event = models.ForeignKey(Event, on_delete=models.RESTRICT)
    venue = models.ForeignKey(Venue, on_delete=models.RESTRICT)
    starting = models.DateTimeField()
    notes = models.CharField(max_length=255, blank=True, null=True)

    @property
    def event_name(self) -> str:
        return self.event.name

    @property
    def venue_name(self) -> str:
        return self.venue.name

    def __str__(self) -> str:
        return f'{self.direction} {self.event.name} at {self.starting} on a {self.method.name}'
