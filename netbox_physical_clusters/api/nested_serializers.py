"""
API Nested Serializers for the plugin.

Serializers used by the plugin serializers for parent serializers.

"""

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers


from netbox.api.serializers import WritableNestedSerializer
from netbox_physical_clusters.models import PhysicalCluster, PhysicalClusterType


__all__ = [
    "NestedPhysicalClusterSerializer",
    "NestedPhysicalClusterTypeSerializer",
]

#
# PhysicalClusters
#


@extend_schema_serializer(
    exclude_fields=("cluster_count",),
)
class NestedPhysicalClusterTypeSerializer(WritableNestedSerializer):
    """The Serializer to return a Type for a Cluster."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_physical_clusters-api:physicalclustertype-detail"
    )
    cluster_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = PhysicalClusterType
        fields = ["id", "url", "display", "name", "cluster_count"]


@extend_schema_serializer()
class NestedPhysicalClusterSerializer(WritableNestedSerializer):
    """The Serializer to return a Cluster for a Type."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_physical_clusters-api:physicalcluster-detail"
    )

    class Meta:
        model = PhysicalCluster
        fields = ["id", "url", "display", "name"]
