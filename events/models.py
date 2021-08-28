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

    def print(self):
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
