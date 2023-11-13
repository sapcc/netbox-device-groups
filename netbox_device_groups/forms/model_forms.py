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

from netbox_device_groups.choices import DeviceGroupStatusChoices
from netbox_device_groups.models import DeviceGroup, DeviceGroupType

__all__ = (
    "DeviceGroupForm",
    "DeviceGroupTypeForm",
    "DeviceGroupAddDevicesForm",
    "DeviceGroupRemoveDevicesForm",
)


class DeviceGroupTypeForm(NetBoxModelForm):
    """Define the django models for this Device Group Types."""

    fieldsets = (
        (
            _("Device Group Type"),
            (
                "name",
                "description",
                "tags",
            ),
        ),
    )

    class Meta:
        model = DeviceGroupType
        fields = (
            "name",
            "description",
            "tags",
        )


class DeviceGroupForm(TenancyForm, NetBoxModelForm):
    """The form definition for adding device groups to the database."""

    cluster_type = DynamicModelChoiceField(queryset=DeviceGroupType.objects.all(), selector=True)

    site = DynamicModelChoiceField(queryset=Site.objects.all(), selector=True)
    status = forms.ChoiceField(
        label=_("Status"),
        choices=DeviceGroupStatusChoices,
        required=True,
        initial=DeviceGroupStatusChoices.STATUS_PLANNED,
    )
    fieldsets = (
        (_("Device Group"), ("name", "cluster_type", "site", "status", "description", "tags")),
        (_("Tenancy"), ("tenant_group", "tenant")),
    )

    class Meta:
        model = DeviceGroup
        fields = (
            "name",
            "cluster_type",
            "status",
            "tenant",
            "site",
            "description",
            "tags",
        )


class DeviceGroupAddDevicesForm(BootstrapMixin, forms.Form):
    """The form definition for adding devices to device groups in the database."""

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


class DeviceGroupRemoveDevicesForm(ConfirmationForm):
    """A confirmation dialog asking for confirmation to remove the listed devices from the cluster."""

    pk = forms.ModelMultipleChoiceField(queryset=Device.objects.all(), widget=forms.MultipleHiddenInput())
