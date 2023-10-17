"""Bulk Edit used by the Plugin Forms."""

from django import forms
from django.utils.translation import gettext_lazy as _

from dcim.models import Site
from netbox.forms import NetBoxModelBulkEditForm
from tenancy.models import Tenant
from utilities.forms import add_blank_choice
from utilities.forms.fields import DynamicModelChoiceField

from netbox_physical_clusters.choices import PhysicalClusterStatusChoices
from netbox_physical_clusters.models import PhysicalCluster, PhysicalClusterType

__all__ = (
    "PhysicalClusterBulkEditForm",
    "PhysicalClusterTypeBulkEditForm",
)


class PhysicalClusterTypeBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit for Type."""

    description = forms.CharField(label=_("Description"), max_length=200, required=False)
    model = PhysicalClusterType
    fieldsets = ((None, ("description",)),)
    nullable_fields = ("description",)


class PhysicalClusterBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit for Cluster."""

    cluster_type = DynamicModelChoiceField(queryset=PhysicalClusterType.objects.all(), required=False)
    status = forms.ChoiceField(choices=add_blank_choice(PhysicalClusterStatusChoices), required=False, initial="")
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

    model = PhysicalCluster
    fieldsets = (
        (None, ("cluster_type", "status", "tenant", "description")),
        ("Site", ("site")),
    )
    nullable_fields = (
        "site",
        "tenant",
        "description",
    )
