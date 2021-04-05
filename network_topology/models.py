from django.core.exceptions import ValidationError
from django.db import models


class ConnectionMethod(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class IP(models.Model):
    ip = models.GenericIPAddressField(unique=True)

    def __str__(self) -> str:
        return self.ip


class DeviceType(models.Model):
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f"{self.manufacturer} - {self.model}"


class Device(models.Model):
    name = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    ip = models.OneToOneField(IP, on_delete=models.CASCADE)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    connected_to = models.ForeignKey('self', on_delete=models.RESTRICT, blank=True, null=True)
    connection_method = models.ForeignKey(ConnectionMethod, on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self) -> str:
        return self.name
