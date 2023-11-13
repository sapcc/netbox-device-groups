"""Define GraphQL type for the Plugin."""

from netbox.graphql.types import NetBoxObjectType
from netbox_device_groups import filtersets, models

__all__ = (
    "DeviceGroupType",
    "DeviceGroupTypeType",
)


class DeviceGroupTypeType(NetBoxObjectType):
    """Define GraphQL type for the DeviceGroupType."""

    class Meta:
        model = models.DeviceGroupType
        fields = "__all__"
        filterset_class = filtersets.DeviceGroupTypeFilterSet


class DeviceGroupType(NetBoxObjectType):
    """Define GraphQL type for the DeviceGroup."""

    class Meta:
        model = models.DeviceGroup
        fields = "__all__"
        filterset_class = filtersets.DeviceGroupFilterSet
