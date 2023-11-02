"""Define the search for this plugin."""

from netbox.search import SearchIndex, register_search
from netbox_physical_clusters import models


@register_search
class PhysicalClusterIndex(SearchIndex):
    """Define the Cluster search."""

    model = models.PhysicalCluster
    fields = (
        ("name", 100),
        ("description", 500),
    )


@register_search
class PhysicalClusterTypeIndex(SearchIndex):
    """Define the Cluster Type search."""

    model = models.PhysicalClusterType
    fields = (
        ("name", 100),
        ("description", 500),
    )
