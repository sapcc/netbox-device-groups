
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel

__all__ = (
    'ExtendedClusterType',
)


class ExtendedClusterType(NetBoxModel):
    """
    A type of Cluster.
    """
    name = models.CharField(
        verbose_name='name',
        max_length=100
    )
    slug = models.SlugField(
        verbose_name='name',
        max_length=100
    )

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        """
        The method is a Django convention; although not strictly required,
        it conveniently returns the absolute URL for any particular object.
        """
        return reverse("plugins:netbox_plugin_extended_clusters:extclustertypelist", args=[self.pk])