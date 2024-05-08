"""Filters sets for the plugin."""

import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from dcim.models import Device, Site
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet

from .choices import DeviceGroupStatusChoices
from .models import DeviceGroup, DeviceGroupType

__all__ = (
    "DeviceGroupFilterSet",
    "DeviceGroupTypeFilterSet",
)


class DeviceGroupTypeFilterSet(NetBoxModelFilterSet):
    """FilterSet for the device group type."""

    class Meta:
        model = DeviceGroupType
        fields = ["id", "name", "description"]


class DeviceGroupFilterSet(NetBoxModelFilterSet, TenancyFilterSet):
    """FilterSet for the device group."""

    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        label=_("Site (ID)"),
    )
    site = django_filters.ModelMultipleChoiceFilter(
        field_name="site__name",
        queryset=Site.objects.all(),
        to_field_name="name",
        label=_("Site (name)"),
    )
    status = django_filters.MultipleChoiceFilter(choices=DeviceGroupStatusChoices, null_value=None)
    device_group_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=DeviceGroupType.objects.all(),
        label=_("Device Type (ID)"),
    )
    device_group_type = django_filters.ModelMultipleChoiceFilter(
        field_name="device_group_type__name",
        queryset=DeviceGroupType.objects.all(),
        to_field_name="name",
        label=_("Device Type"),
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name="devices",
        queryset=Device.objects.all(),
        label=_("Device"),
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name="devices__name",
        queryset=Device.objects.all(),
        to_field_name="name",
        label=_("Device (name)"),
    )

    class Meta:
        model = DeviceGroup
        fields = ["id", "name"]

    def search(self, queryset, name, value):
        """Search Definition for the Device Group."""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    def _has_primary_ip(self, queryset, name, value):
        """Does the Device Group have a primary IP Address."""
        params = Q(primary_ip4__isnull=False)
        if value:
            return queryset.filter(params)
        return queryset.exclude(params)
