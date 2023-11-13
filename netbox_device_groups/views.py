"""Define the views for this plugin."""
from collections import defaultdict

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from dcim.filtersets import DeviceFilterSet
from dcim.models import Device
from dcim.tables import DeviceTable
from netbox.views import generic
from utilities.utils import count_related
from utilities.views import ViewTab, register_model_view

from netbox_device_groups import filtersets, forms, tables
from netbox_device_groups.models import DeviceGroup, DeviceGroupType


#
# DeviceGroup types
#


class DeviceGroupTypeListView(generic.ObjectListView):
    """
    DeviceGroup Type list view.

    Return a list of device group Types
    """

    queryset = DeviceGroupType.objects.annotate(cluster_count=count_related(DeviceGroup, "cluster_type"))
    filterset = filtersets.DeviceGroupTypeFilterSet
    filterset_form = forms.DeviceGroupTypeFilterForm
    table = tables.DeviceGroupTypeTable


@register_model_view(DeviceGroupType)
class DeviceGroupTypeView(generic.ObjectView):
    """
    DeviceGroup Type view.

    Return a device group Types
    """

    queryset = DeviceGroupType.objects.all()


@register_model_view(DeviceGroupType, "edit")
class DeviceGroupTypeEditView(generic.ObjectEditView):
    """DeviceGroup Type view.for Editing."""

    queryset = DeviceGroupType.objects.all()
    form = forms.DeviceGroupTypeForm


@register_model_view(DeviceGroupType, "delete")
class DeviceGroupTypeDeleteView(generic.ObjectDeleteView):
    """DeviceGroup Type view.for deleting."""

    queryset = DeviceGroupType.objects.all()


class DeviceGroupTypeBulkImportView(generic.BulkImportView):
    """DeviceGroup Type view.for bulk importing."""

    queryset = DeviceGroupType.objects.all()
    model_form = forms.DeviceGroupTypeImportForm


class DeviceGroupTypeBulkEditView(generic.BulkEditView):
    """DeviceGroup Type view.for Bulk Editing."""

    queryset = DeviceGroupType.objects.annotate(cluster_count=count_related(DeviceGroup, "cluster_type"))
    filterset = filtersets.DeviceGroupTypeFilterSet
    table = tables.DeviceGroupTypeTable
    form = forms.DeviceGroupTypeBulkEditForm


class DeviceGroupTypeBulkDeleteView(generic.BulkDeleteView):
    """DeviceGroup Type view.for bulk deletion."""

    queryset = DeviceGroupType.objects.annotate(cluster_count=count_related(DeviceGroup, "cluster_type"))
    filterset = filtersets.DeviceGroupTypeFilterSet
    table = tables.DeviceGroupTypeTable


#
# DeviceGroups
#


class DeviceGroupListView(generic.ObjectListView):
    """DeviceGroup view.for listing clusters."""

    permission_required = "devicegroup.view_cluster"
    queryset = DeviceGroup.objects.annotate(device_count=count_related(Device, "devicegroup"))
    table = tables.DeviceGroupTable
    filterset = filtersets.DeviceGroupFilterSet
    filterset_form = forms.DeviceGroupFilterForm


@register_model_view(DeviceGroup)
class DeviceGroupView(generic.ObjectView):
    """DeviceGroup view.for retrieving a cluster."""

    queryset = DeviceGroup.objects.all()


@register_model_view(DeviceGroup, "devices")
class DeviceGroupDevicesView(generic.ObjectChildrenView):
    """DeviceGroup view.for listing clusters."""

    queryset = DeviceGroup.objects.all()
    child_model = Device
    table = DeviceTable
    filterset = DeviceFilterSet
    template_name = "netbox_device_groups/physical_cluster/devices.html"
    actions = ("add", "import", "export", "bulk_edit", "bulk_remove_devices")
    action_perms = defaultdict(
        set,
        **{
            "add": {"add"},
            "import": {"add"},
            "bulk_edit": {"change"},
            "bulk_remove_devices": {"change"},
        },
    )
    tab = ViewTab(
        label=_("Devices"),
        badge=lambda obj: obj.devices.count(),
        permission="netbox_device_groups.view_devices",
        weight=600,
    )

    def get_children(self, request, parent):
        """Retrieves the devices that make up the cluster."""
        return Device.objects.restrict(request.user, "view").filter(devicegroup=parent)


@register_model_view(DeviceGroup, "edit")
class DeviceGroupEditView(generic.ObjectEditView):
    """DeviceGroup Type view.for editing."""

    queryset = DeviceGroup.objects.all()
    form = forms.DeviceGroupForm


@register_model_view(DeviceGroup, "delete")
class DeviceGroupDeleteView(generic.ObjectDeleteView):
    """DeviceGroup Type view.for deletion."""

    queryset = DeviceGroup.objects.all()


class DeviceGroupBulkImportView(generic.BulkImportView):
    """DeviceGroup view.for bulk import."""

    queryset = DeviceGroup.objects.all()
    model_form = forms.DeviceGroupImportForm


class DeviceGroupBulkEditView(generic.BulkEditView):
    """DeviceGroup view.for bulk edit."""

    queryset = DeviceGroup.objects.all()
    filterset = filtersets.DeviceGroupFilterSet
    table = tables.DeviceGroupTable
    form = forms.DeviceGroupBulkEditForm


class DeviceGroupBulkDeleteView(generic.BulkDeleteView):
    """DeviceGroup view.for bulk deletion."""

    queryset = DeviceGroup.objects.all()
    filterset = filtersets.DeviceGroupFilterSet
    table = tables.DeviceGroupTable


@register_model_view(DeviceGroup, "add_devices", path="devices/add")
class DeviceGroupAddDevicesView(generic.ObjectEditView):
    """DeviceGroup view.for managing the addition of devices to a cluster."""

    queryset = DeviceGroup.objects.all()
    form = forms.DeviceGroupAddDevicesForm
    template_name = "netbox_device_groups/cluster_add_devices.html"

    def get(self, request, pk):
        """Retrieve device list."""
        devicegroup = get_object_or_404(self.queryset, pk=pk)
        form = self.form(devicegroup, initial=request.GET)

        return render(
            request,
            self.template_name,
            {
                "cluster": devicegroup,
                "form": form,
                "return_url": reverse("plugins:netbox_device_groups:devicegroup", kwargs={"pk": pk}),
            },
        )

    def post(self, request, pk):
        """Add devices."""
        devicegroup = get_object_or_404(self.queryset, pk=pk)
        form = self.form(devicegroup, request.POST)

        if form.is_valid():
            device_pks = form.cleaned_data["devices"]
            with transaction.atomic():
                # Assign the selected Devices to the DeviceGroup
                for device in Device.objects.filter(pk__in=device_pks):
                    devicegroup.devices.add(device)
                    devicegroup.save()

            messages.success(request, "Added {} devices to cluster {}".format(len(device_pks), devicegroup))
            return redirect(devicegroup.get_absolute_url())

        return render(
            request,
            self.template_name,
            {
                "cluster": devicegroup,
                "form": form,
                "return_url": devicegroup.get_absolute_url(),
            },
        )


@register_model_view(DeviceGroup, "remove_devices", path="devices/remove")
class DeviceGroupRemoveDevicesView(generic.ObjectEditView):
    """DeviceGroup view.for managing the deletion of devices to a cluster."""

    queryset = DeviceGroup.objects.all()
    form = forms.DeviceGroupRemoveDevicesForm
    template_name = "generic/bulk_remove.html"

    def post(self, request, pk):
        """Removes teh specified device."""
        devicegroup = get_object_or_404(self.queryset, pk=pk)

        if "_confirm" in request.POST:
            form = self.form(request.POST)
            if form.is_valid():
                device_pks = form.cleaned_data["pk"]
                with transaction.atomic():
                    # Remove the selected Devices from the DeviceGroup
                    for device in Device.objects.filter(pk__in=device_pks):
                        devicegroup.devices.remove(device)
                        devicegroup.save()

                messages.success(request, "Removed {} devices from cluster {}".format(len(device_pks), devicegroup))
                return redirect(devicegroup.get_absolute_url())

        else:
            form = self.form(initial={"pk": request.POST.getlist("pk")})

        selected_objects = Device.objects.filter(pk__in=form.initial["pk"])
        device_table = DeviceTable(list(selected_objects), orderable=False)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "parent_obj": devicegroup,
                "table": device_table,
                "obj_type_plural": "devices",
                "return_url": devicegroup.get_absolute_url(),
            },
        )
