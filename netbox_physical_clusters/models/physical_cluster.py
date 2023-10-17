"""Define the django models for this Physical Cluster Types."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from dcim.models import Device
from netbox_physical_clusters.choices import PhysicalClusterStatusChoices
from netbox_physical_clusters.core.models import PluginBaseModel
from netbox_physical_clusters.models import PhysicalClusterType

__all__ = ("PhysicalCluster",)


class PhysicalCluster(PluginBaseModel):
    """A cluster of physical devices. Each Cluster may optionally be associated with one or more Devices."""

    cluster_type = models.ForeignKey(
        to=PhysicalClusterType, on_delete=models.PROTECT, related_name="physical_clusters"
    )
    status = models.CharField(
        max_length=50, choices=PhysicalClusterStatusChoices, default=PhysicalClusterStatusChoices.STATUS_PLANNED
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant", on_delete=models.PROTECT, related_name="physical_clusters", blank=True, null=True
    )
    site = models.ForeignKey(
        to="dcim.Site", on_delete=models.PROTECT, related_name="physical_clusters", blank=True, null=True
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
    prerequisite_models = ("netbox_physical_clusters.PhysicalClusterType",)

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
        return reverse("plugins:netbox_physical_clusters:physicalcluster", args=[self.pk])
