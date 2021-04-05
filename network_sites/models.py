from django.db import models

from network_topology.models import IP


class Site(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    ip = models.ForeignKey(IP, on_delete=models.DO_NOTHING)
    url = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def corrected_url(self) -> str:
        url = self.url
        if self.url and 'IP-ADDRESS.com' in self.url:
            url = url.replace('IP-ADDRESS.com', self.ip.__str__())
        return url
