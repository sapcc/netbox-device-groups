"""Define the django models for this Device Group Types."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from dcim.models import Device
from netbox_device_groups.choices import DeviceGroupStatusChoices
from netbox_device_groups.core.models import PluginBaseModel
from netbox_device_groups.models import DeviceGroupType

__all__ = ("DeviceGroup",)


class DeviceGroup(PluginBaseModel):
    """A cluster of physical devices. Each Cluster may optionally be associated with one or more Devices."""

    cluster_type = models.ForeignKey(to=DeviceGroupType, on_delete=models.PROTECT, related_name="device_groups")
    status = models.CharField(
        max_length=50, choices=DeviceGroupStatusChoices, default=DeviceGroupStatusChoices.STATUS_PLANNED
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant", on_delete=models.PROTECT, related_name="device_groups", blank=True, null=True
    )
    site = models.ForeignKey(
        to="dcim.Site", on_delete=models.PROTECT, related_name="device_groups", blank=True, null=True
    )
    devices = models.ManyToManyField(Device)
    primary_ip4 = models.OneToOneField(
        to="ipam.IPAddress",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
        verbose_name=_("primary IPv4"),
    )
    clone_fields = (
        "cluster_type",
        "status",
        "tenant",
        "site",
    )
    prerequisite_models = ("netbox_device_groups.DeviceGroupType",)

    class Meta:
        ordering = ["name"]
        constraints = (
            models.UniqueConstraint(fields=("site", "name"), name="%(app_label)s_%(class)s_unique_site_name"),
        )

    def __str__(self):
        """Returns the object representation in a string format."""
        return self.name

    def get_absolute_url(self):
        """Returns the objects absolute url. i.e. clusters/cluster-type/2."""
        return reverse("plugins:netbox_device_groups:devicegroup", args=[self.pk])
