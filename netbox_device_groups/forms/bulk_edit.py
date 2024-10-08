"""Bulk Edit used by the Plugin Forms."""

from django import forms
from django.utils.translation import gettext_lazy as _

from dcim.models import Site
from netbox.forms import NetBoxModelBulkEditForm
from tenancy.models import Tenant
from utilities.forms import add_blank_choice
from utilities.forms.fields import DynamicModelChoiceField

from netbox_device_groups.choices import DeviceGroupStatusChoices
from netbox_device_groups.models import DeviceGroup, DeviceGroupType

__all__ = (
    "DeviceGroupBulkEditForm",
    "DeviceGroupTypeBulkEditForm",
)


class DeviceGroupTypeBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit for Type."""

    description = forms.CharField(label=_("Description"), max_length=200, required=False)
    model = DeviceGroupType
    fieldsets = ((None, ("description",)),)
    nullable_fields = ("description",)


class DeviceGroupBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit for Device Group."""

    device_group_type = DynamicModelChoiceField(queryset=DeviceGroupType.objects.all(), required=False)
    status = forms.ChoiceField(choices=add_blank_choice(DeviceGroupStatusChoices), required=False, initial="")
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            "region_id": "$region",
            "group_id": "$site_group",
        },
    )
    description = forms.CharField(max_length=200, required=False)

    model = DeviceGroup
    fieldsets = (
        (None, ("device_group_type", "status", "tenant", "description")),
        ("Site", ("site")),
    )
    nullable_fields = (
        "site",
        "tenant",
        "description",
    )
