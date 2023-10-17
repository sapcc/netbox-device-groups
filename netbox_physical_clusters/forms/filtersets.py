"""Filtersets used by the Plugin Forms."""
from django import forms
from django.utils.translation import gettext as _

from dcim.models import Site
from netbox.forms import NetBoxModelFilterSetForm
from tenancy.forms import TenancyFilterForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField

from netbox_physical_clusters.choices import PhysicalClusterStatusChoices
from netbox_physical_clusters.models import PhysicalCluster, PhysicalClusterType


__all__ = (
    "PhysicalClusterFilterForm",
    "PhysicalClusterTypeFilterForm",
)


class PhysicalClusterTypeFilterForm(NetBoxModelFilterSetForm):
    """Form Filter for PhysicalClusterType."""

    model = PhysicalClusterType
    tag = TagFilterField(model)


class PhysicalClusterFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    """Form Filter use to limit objects returned for PhysicalCluster."""

    model = PhysicalCluster
    fieldsets = (
        (None, ("q", "filter_id", "tag")),
        (_("Attributes"), ("cluster_type_id", "status")),
        (_("Site/Tenant"), ("site_id", "tenant_group_id", "tenant_id")),
    )
    cluster_type_id = DynamicModelMultipleChoiceField(
        queryset=PhysicalClusterType.objects.all(), required=False, label=_("Type")
    )
    status = forms.MultipleChoiceField(choices=PhysicalClusterStatusChoices, required=False)
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        null_option="None",
        label=_("Site"),
    )
    tag = TagFilterField(model)
