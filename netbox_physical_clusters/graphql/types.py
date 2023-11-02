"""Define GraphQL type for the Plugin."""

from netbox.graphql.types import NetBoxObjectType
from netbox_physical_clusters import filtersets, models

__all__ = (
    "PhysicalClusterType",
    "PhysicalClusterTypeType",
)


class PhysicalClusterTypeType(NetBoxObjectType):
    """Define GraphQL type for the PhysicalClusterType."""

    class Meta:
        model = models.PhysicalClusterType
        fields = "__all__"
        filterset_class = filtersets.PhysicalClusterTypeFilterSet


class PhysicalClusterType(NetBoxObjectType):
    """Define GraphQL type for the PhysicalCluster."""

    class Meta:
        model = models.PhysicalCluster
        fields = "__all__"
        filterset_class = filtersets.PhysicalClusterFilterSet
