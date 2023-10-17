"""Define the django model for the Physical Cluster Types."""

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox_physical_clusters.core.models import PluginBaseModel

__all__ = ("PhysicalClusterType",)


class PhysicalClusterType(PluginBaseModel):
    """Model definition for Physical Cluster Types."""

    class Meta:
        ordering = ("name",)
        verbose_name = _("physical cluster type")
        verbose_name_plural = _("physical cluster types")

    def __str__(self):
        """Returns the object representation in a string format."""
        return self.name

    def get_absolute_url(self):
        """Returns the objects absolute url. i.e. clusters/cluster-type/2."""
        return reverse("plugins:netbox_physical_clusters:physicalclustertype", args=[self.pk])
