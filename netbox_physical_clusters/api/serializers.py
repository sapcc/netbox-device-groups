"""API Serializers for the plugin/."""

from rest_framework import serializers

from netbox.api.fields import ChoiceField
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer

from netbox_physical_clusters.choices import PhysicalClusterStatusChoices
from netbox_physical_clusters.models import PhysicalCluster, PhysicalClusterType
from netbox_physical_clusters.api.nested_serializers import NestedPhysicalClusterTypeSerializer
from dcim.api.nested_serializers import (
    NestedDeviceSerializer,
    NestedSiteSerializer,
)


class PhysicalClusterTypeSerializer(NetBoxModelSerializer):
    """Serializer for the Physical Cluster Type."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_physical_clusters-api:physicalclustertype-detail"
    )
    cluster_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = PhysicalClusterType
        fields = [
            "id",
            "url",
            "name",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "cluster_count",
        ]


class PhysicalClusterSerializer(NetBoxModelSerializer):
    """Serializer for the Physical Cluster."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_physical_clusters-api:physicalcluster-detail"
    )
    cluster_type = NestedPhysicalClusterTypeSerializer()
    status = ChoiceField(choices=PhysicalClusterStatusChoices, required=False)
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    site = NestedSiteSerializer(required=False, allow_null=True, default=None)
    device_count = serializers.IntegerField(read_only=True)
    devices = NestedDeviceSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = PhysicalCluster
        fields = [
            "id",
            "url",
            "name",
            "cluster_type",
            "status",
            "tenant",
            "site",
            "description",
            "tags",
            "created",
            "last_updated",
            "device_count",
            "devices",
        ]
