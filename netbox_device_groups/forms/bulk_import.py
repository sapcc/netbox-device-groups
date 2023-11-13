"""Bulk Import used by the Plugin Forms."""

from django.utils.translation import gettext as _

from dcim.models import Site
from netbox.forms import NetBoxModelImportForm
from tenancy.models import Tenant
from utilities.forms.fields import CSVChoiceField, CSVModelChoiceField

from netbox_device_groups.choices import DeviceGroupStatusChoices
from netbox_device_groups.models import DeviceGroup, DeviceGroupType

__all__ = (
    "DeviceGroupImportForm",
    "DeviceGroupTypeImportForm",
)


class DeviceGroupTypeImportForm(NetBoxModelImportForm):
    """Bulk Import for type."""

    class Meta:
        model = DeviceGroupType
        fields = ("name", "description", "tags")


class DeviceGroupImportForm(NetBoxModelImportForm):
    """Bulk Import for Cluster."""

    cluster_type = CSVModelChoiceField(
        queryset=DeviceGroupType.objects.all(), to_field_name="name", help_text=_("Type of cluster")
    )
    status = CSVChoiceField(choices=DeviceGroupStatusChoices, help_text=_("Operational status"))
    site = CSVModelChoiceField(
        queryset=Site.objects.all(), to_field_name="name", required=False, help_text=_("Assigned site")
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(), to_field_name="name", required=False, help_text=_("Assigned tenant")
    )

    class Meta:
        model = DeviceGroup
        fields = ("name", "cluster_type", "status", "site", "tenant", "description", "tags")
