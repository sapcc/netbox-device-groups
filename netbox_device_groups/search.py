"""Define the search for this plugin."""

from netbox.search import SearchIndex, register_search
from netbox_device_groups import models


@register_search
class DeviceGroupIndex(SearchIndex):
    """Define the Cluster search."""

    model = models.DeviceGroup
    fields = (
        ("name", 100),
        ("description", 500),
    )


@register_search
class DeviceGroupTypeIndex(SearchIndex):
    """Define the Device Group Type search."""

    model = models.DeviceGroupType
    fields = (
        ("name", 100),
        ("description", 500),
    )
