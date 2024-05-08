"""
API Nested Serializers for the plugin.

Serializers used by the plugin serializers for parent serializers.

"""

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers


from netbox.api.serializers import WritableNestedSerializer
from netbox_device_groups.models import DeviceGroup, DeviceGroupType


__all__ = [
    "NestedDeviceGroupSerializer",
    "NestedDeviceGroupTypeSerializer",
]

#
# DeviceGroups
#


@extend_schema_serializer(
    exclude_fields=("device_group_count",),
)
class NestedDeviceGroupTypeSerializer(WritableNestedSerializer):
    """The Serializer to return a Type for a device group."""

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_device_groups-api:devicegrouptype-detail")
    device_group_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = DeviceGroupType
        fields = ["id", "url", "display", "name", "device_group_count"]


@extend_schema_serializer()
class NestedDeviceGroupSerializer(WritableNestedSerializer):
    """The Serializer to return a device group for a Type."""

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_device_groups-api:devicegroup-detail")

    class Meta:
        model = DeviceGroup
        fields = ["id", "url", "display", "name"]
