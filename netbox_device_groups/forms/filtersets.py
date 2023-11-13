"""Filtersets used by the Plugin Forms."""
from django import forms
from django.utils.translation import gettext as _

from dcim.models import Site
from netbox.forms import NetBoxModelFilterSetForm
from tenancy.forms import TenancyFilterForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField

from netbox_device_groups.choices import DeviceGroupStatusChoices
from netbox_device_groups.models import DeviceGroup, DeviceGroupType


__all__ = (
    "DeviceGroupFilterForm",
    "DeviceGroupTypeFilterForm",
)


class DeviceGroupTypeFilterForm(NetBoxModelFilterSetForm):
    """Form Filter for DeviceGroupType."""

    model = DeviceGroupType
    tag = TagFilterField(model)


class DeviceGroupFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    """Form Filter use to limit objects returned for DeviceGroup."""

    model = DeviceGroup
    fieldsets = (
        (None, ("q", "filter_id", "tag")),
        (_("Attributes"), ("cluster_type_id", "status")),
        (_("Site/Tenant"), ("site_id", "tenant_group_id", "tenant_id")),
    )
    cluster_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceGroupType.objects.all(), required=False, label=_("Type")
    )
    status = forms.MultipleChoiceField(choices=DeviceGroupStatusChoices, required=False)
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        null_option="None",
        label=_("Site"),
    )
    tag = TagFilterField(model)
