"""API Viewsets for the plugin."""

from rest_framework.routers import APIRootView

from dcim.models import Device
from netbox.api.viewsets import NetBoxModelViewSet
from utilities.utils import count_related

from netbox_physical_clusters import filtersets
from netbox_physical_clusters.models import PhysicalCluster, PhysicalClusterType
from . import serializers


class PhysicalClusterRootView(APIRootView):
    """Physical Clusters API root view."""

    def get_view_name(self):
        """Return the Root View Name."""
        return " Physical Clusters"


class PhysicalClusterTypeViewSet(NetBoxModelViewSet):
    """A Viewset for the PhysicalClusterType."""

    queryset = PhysicalClusterType.objects.all().prefetch_related("tags")
    serializer_class = serializers.PhysicalClusterTypeSerializer
    filterset_class = filtersets.PhysicalClusterTypeFilterSet


class PhysicalClusterViewSet(NetBoxModelViewSet):
    """A Viewset for the PhysicalCluster."""

    queryset = PhysicalCluster.objects.prefetch_related("cluster_type", "tenant", "site", "tags", "devices").annotate(
        device_count=count_related(Device, "cluster"),
    )
    serializer_class = serializers.PhysicalClusterSerializer
    filterset_class = filtersets.PhysicalClusterFilterSet
