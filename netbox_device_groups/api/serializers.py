"""API Serializers for the plugin/."""

from rest_framework import serializers

from netbox.api.fields import ChoiceField
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer

from netbox_device_groups.choices import DeviceGroupStatusChoices
from netbox_device_groups.models import DeviceGroup, DeviceGroupType
from netbox_device_groups.api.nested_serializers import NestedDeviceGroupTypeSerializer
from dcim.api.nested_serializers import (
    NestedDeviceSerializer,
    NestedSiteSerializer,
)


class DeviceGroupTypeSerializer(NetBoxModelSerializer):
    """Serializer for the Device Group Type."""

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_device_groups-api:devicegrouptype-detail")
    cluster_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = DeviceGroupType
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


class DeviceGroupSerializer(NetBoxModelSerializer):
    """Serializer for the Device Group."""

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_device_groups-api:devicegroup-detail")
    cluster_type = NestedDeviceGroupTypeSerializer()
    status = ChoiceField(choices=DeviceGroupStatusChoices, required=False)
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    site = NestedSiteSerializer(required=False, allow_null=True, default=None)
    device_count = serializers.IntegerField(read_only=True)
    devices = NestedDeviceSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = DeviceGroup
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
