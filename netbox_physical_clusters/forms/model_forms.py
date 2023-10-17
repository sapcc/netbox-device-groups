"""Define the form for this Plugin."""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


from dcim.models import Device, Site
from netbox.forms import NetBoxModelForm
from tenancy.forms import TenancyForm
from utilities.forms import BootstrapMixin, ConfirmationForm
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)

from netbox_physical_clusters.choices import PhysicalClusterStatusChoices
from netbox_physical_clusters.models import PhysicalCluster, PhysicalClusterType

__all__ = (
    "PhysicalClusterForm",
    "PhysicalClusterTypeForm",
    "PhysicalClusterAddDevicesForm",
    "PhysicalClusterRemoveDevicesForm",
)


class PhysicalClusterTypeForm(NetBoxModelForm):
    """Define the django models for this Physical Cluster Types."""

    fieldsets = (
        (
            _("Cluster Type"),
            (
                "name",
                "description",
                "tags",
            ),
        ),
    )

    class Meta:
        model = PhysicalClusterType
        fields = (
            "name",
            "description",
            "tags",
        )


class PhysicalClusterForm(TenancyForm, NetBoxModelForm):
    """The form definition for adding physical clusters to the database."""

    cluster_type = DynamicModelChoiceField(queryset=PhysicalClusterType.objects.all(), selector=True)

    site = DynamicModelChoiceField(queryset=Site.objects.all(), selector=True)
    status = forms.ChoiceField(
        label=_("Status"),
        choices=PhysicalClusterStatusChoices,
        required=True,
        initial=PhysicalClusterStatusChoices.STATUS_PLANNED,
    )
    fieldsets = (
        (_("Physical Cluster"), ("name", "cluster_type", "site", "status", "description", "tags")),
        (_("Tenancy"), ("tenant_group", "tenant")),
    )

    class Meta:
        model = PhysicalCluster
        fields = (
            "name",
            "cluster_type",
            "status",
            "tenant",
            "site",
            "description",
            "tags",
        )


class PhysicalClusterAddDevicesForm(BootstrapMixin, forms.Form):
    """The form definition for adding devices to physical clusters in the database."""

    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
    )
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        query_params={
            "site_id": "$site",
        },
    )

    class Meta:
        fields = [
            "site",
            "devices",
        ]

    def __init__(self, cluster, *args, **kwargs):
        """On creation initialise an empty set for devices."""
        self.cluster = cluster

        super().__init__(*args, **kwargs)

        self.fields["devices"].choices = []

    def clean(self):
        """If the Cluster is assigned to a Site, all Devices must be assigned to that Site.."""
        super().clean()

        if self.cluster.site is not None:
            for device in self.cleaned_data.get("devices", []):
                if device.site != self.cluster.site:
                    raise ValidationError(
                        {
                            "devices": "{} belongs to a different site ({}) than the cluster ({})".format(
                                device, device.site, self.cluster.site
                            )
                        }
                    )


class PhysicalClusterRemoveDevicesForm(ConfirmationForm):
    """A confirmation dialog asking for confirmation to remove the listed devices from the cluster."""

    pk = forms.ModelMultipleChoiceField(queryset=Device.objects.all(), widget=forms.MultipleHiddenInput())
