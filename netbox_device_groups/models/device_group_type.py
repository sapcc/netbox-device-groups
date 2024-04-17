"""Define the django model for the Device Group Types."""

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox_device_groups.core.models import PluginBaseModel

__all__ = ("DeviceGroupType",)


class DeviceGroupType(PluginBaseModel):
    """Model definition for Device Group Types."""

    class Meta:
        ordering = ("name",)
        verbose_name = _("device group type")
        verbose_name_plural = _("device group types")

    def __str__(self):
        """Returns the object representation in a string format."""
        return self.name

    def get_absolute_url(self):
        """Returns the objects absolute url. i.e. clusters/cluster-type/2."""
        return reverse("plugins:netbox_device_groups:devicegrouptype", args=[self.pk])
