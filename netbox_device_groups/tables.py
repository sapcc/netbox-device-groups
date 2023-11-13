"""Define the django tables for this plugin."""

from django.utils.translation import gettext_lazy as _
import django_tables2 as tables

from netbox_device_groups.models import DeviceGroup, DeviceGroupType
from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin

__all__ = (
    "DeviceGroupTable",
    "DeviceGroupTypeTable",
)


class DeviceGroupTypeTable(NetBoxTable):
    """Device Group Type django table definition."""

    name = tables.Column(linkify=True)
    cluster_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_device_groups:devicegroup_list",
        url_params={"type_id": "pk"},
        verbose_name=_("Clusters"),
    )
    tags = columns.TagColumn(url_name="plugins:netbox_device_groups:devicegrouptype_list")

    class Meta(NetBoxTable.Meta):
        model = DeviceGroupType
        fields = (
            "pk",
            "id",
            "name",
            "cluster_count",
            "description",
            "created",
            "last_updated",
            "tags",
            "actions",
        )
        default_columns = (
            "pk",
            "name",
            "description",
            "cluster_count",
        )


class DeviceGroupTable(TenancyColumnsMixin, NetBoxTable):
    """Device Group django table definition."""

    name = tables.Column(verbose_name=_("Name"), linkify=True)
    cluster_type = tables.Column(verbose_name=_("Type"), linkify=True)
    status = columns.ChoiceFieldColumn(
        verbose_name=_("Status"),
    )
    site = tables.Column(verbose_name=_("Site"), linkify=True)
    device_count = columns.LinkedCountColumn(
        viewname="dcim:device_list", url_params={"devicegroup_id": "pk"}, verbose_name=_("Devices")
    )

    tags = columns.TagColumn(url_name="plugins:netbox_device_groups:devicegroup_list")

    class Meta(NetBoxTable.Meta):
        model = DeviceGroup
        fields = (
            "pk",
            "id",
            "name",
            "cluster_type",
            "status",
            "tenant",
            "site",
            "description",
            "device_count",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = (
            "pk",
            "name",
            "cluster_type",
            "status",
            "tenant",
            "site",
            "device_count",
        )
