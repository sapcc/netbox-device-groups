from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from netbox.models import NetBoxModel
from dcim.models import Device
from ..choices import ExtendedClusterStatusChoices
from .extended_cluster_types import ExtendedClusterType

__all__ = (
    'ExtendedCluster',
)


class ExtendedCluster(NetBoxModel):
    """
    A cluster of VirtualMachines. Each Cluster may optionally be associated with one or more Devices.
    """
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100
    )
    type = models.ForeignKey(
        verbose_name=_('type'),
        to=ExtendedClusterType,
        on_delete=models.PROTECT,
        related_name='extended_clusters'
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=50,
        choices=ExtendedClusterStatusChoices,
        default=ExtendedClusterStatusChoices.STATUS_ACTIVE
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='extended_clusters',
        blank=True,
        null=True
    )
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.PROTECT,
        related_name='extended_clusters',
        blank=True,
        null=True
    )

    prerequisite_models = (
        'ExtendedClusterType',
    )

    class Meta:
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                fields=('group', 'name'),
                name='%(app_label)s_%(class)s_unique_group_name'
            ),
            models.UniqueConstraint(
                fields=('site', 'name'),
                name='%(app_label)s_%(class)s_unique_site_name'
            ),
        )
        verbose_name = _('cluster')
        verbose_name_plural = _('clusters')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('virtualization:cluster', args=[self.pk])

    def get_status_color(self):
        return ExtendedClusterStatusChoices.colors.get(self.status)

    def clean(self):
        super().clean()

        # If the Cluster is assigned to a Site, verify that all host Devices belong to that Site.
        if self.pk and self.site:
            nonsite_devices = Device.objects.filter(cluster=self).exclude(site=self.site).count()
            if nonsite_devices:
                raise ValidationError({
                    'site': _("{} devices are assigned as hosts for this cluster but are not in site {}").format(
                        nonsite_devices, self.site
                    )
                })
