from django.db import models


class IP(models.Model):
    ip = models.GenericIPAddressField(unique=True)


class DeviceType(models.Model):
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.CharField(max_length=500)


class Device(models.Model):
    name = models.CharField(max_length=255)
    ip = models.OneToOneField(IP, on_delete=models.CASCADE)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    connected_to = models.ForeignKey('self', on_delete=models.RESTRICT, blank=True, null=True)
