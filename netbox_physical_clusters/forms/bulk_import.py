"""Bulk Import used by the Plugin Forms."""

from django.utils.translation import gettext as _

from dcim.models import Site
from netbox.forms import NetBoxModelImportForm
from tenancy.models import Tenant
from utilities.forms.fields import CSVChoiceField, CSVModelChoiceField

from netbox_physical_clusters.choices import PhysicalClusterStatusChoices
from netbox_physical_clusters.models import PhysicalCluster, PhysicalClusterType

__all__ = (
    "PhysicalClusterImportForm",
    "PhysicalClusterTypeImportForm",
)


class PhysicalClusterTypeImportForm(NetBoxModelImportForm):
    """Bulk Import for type."""

    class Meta:
        model = PhysicalClusterType
        fields = ("name", "description", "tags")


class PhysicalClusterImportForm(NetBoxModelImportForm):
    """Bulk Import for Cluster."""

    cluster_type = CSVModelChoiceField(
        queryset=PhysicalClusterType.objects.all(), to_field_name="name", help_text=_("Type of cluster")
    )
    status = CSVChoiceField(choices=PhysicalClusterStatusChoices, help_text=_("Operational status"))
    site = CSVModelChoiceField(
        queryset=Site.objects.all(), to_field_name="name", required=False, help_text=_("Assigned site")
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(), to_field_name="name", required=False, help_text=_("Assigned tenant")
    )

    class Meta:
        model = PhysicalCluster
        fields = ("name", "cluster_type", "status", "site", "tenant", "description", "tags")
