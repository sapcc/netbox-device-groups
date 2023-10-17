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

from netbox_physical_clusters import filtersets, forms, tables
from netbox_physical_clusters.models import PhysicalCluster, PhysicalClusterType


#
# PhysicalCluster types
#


class PhysicalClusterTypeListView(generic.ObjectListView):
    """
    PhysicalCluster Type list view.

    Return a list of Physical CLuster Types
    """

    queryset = PhysicalClusterType.objects.annotate(cluster_count=count_related(PhysicalCluster, "cluster_type"))
    filterset = filtersets.PhysicalClusterTypeFilterSet
    filterset_form = forms.PhysicalClusterTypeFilterForm
    table = tables.PhysicalClusterTypeTable


@register_model_view(PhysicalClusterType)
class PhysicalClusterTypeView(generic.ObjectView):
    """
    PhysicalCluster Type view.

    Return a Physical CLuster Types
    """

    queryset = PhysicalClusterType.objects.all()


@register_model_view(PhysicalClusterType, "edit")
class PhysicalClusterTypeEditView(generic.ObjectEditView):
    """PhysicalCluster Type view.for Editing."""

    queryset = PhysicalClusterType.objects.all()
    form = forms.PhysicalClusterTypeForm


@register_model_view(PhysicalClusterType, "delete")
class PhysicalClusterTypeDeleteView(generic.ObjectDeleteView):
    """PhysicalCluster Type view.for deleting."""

    queryset = PhysicalClusterType.objects.all()


class PhysicalClusterTypeBulkImportView(generic.BulkImportView):
    """PhysicalCluster Type view.for bulk importing."""

    queryset = PhysicalClusterType.objects.all()
    model_form = forms.PhysicalClusterTypeImportForm


class PhysicalClusterTypeBulkEditView(generic.BulkEditView):
    """PhysicalCluster Type view.for Bulk Editing."""

    queryset = PhysicalClusterType.objects.annotate(cluster_count=count_related(PhysicalCluster, "cluster_type"))
    filterset = filtersets.PhysicalClusterTypeFilterSet
    table = tables.PhysicalClusterTypeTable
    form = forms.PhysicalClusterTypeBulkEditForm


class PhysicalClusterTypeBulkDeleteView(generic.BulkDeleteView):
    """PhysicalCluster Type view.for bulk deletion."""

    queryset = PhysicalClusterType.objects.annotate(cluster_count=count_related(PhysicalCluster, "cluster_type"))
    filterset = filtersets.PhysicalClusterTypeFilterSet
    table = tables.PhysicalClusterTypeTable


#
# PhysicalClusters
#


class PhysicalClusterListView(generic.ObjectListView):
    """PhysicalCluster view.for listing clusters."""

    permission_required = "physicalcluster.view_cluster"
    queryset = PhysicalCluster.objects.annotate(device_count=count_related(Device, "physicalcluster"))
    table = tables.PhysicalClusterTable
    filterset = filtersets.PhysicalClusterFilterSet
    filterset_form = forms.PhysicalClusterFilterForm


@register_model_view(PhysicalCluster)
class PhysicalClusterView(generic.ObjectView):
    """PhysicalCluster view.for retrieving a cluster."""

    queryset = PhysicalCluster.objects.all()


@register_model_view(PhysicalCluster, "devices")
class PhysicalClusterDevicesView(generic.ObjectChildrenView):
    """PhysicalCluster view.for listing clusters."""

    queryset = PhysicalCluster.objects.all()
    child_model = Device
    table = DeviceTable
    filterset = DeviceFilterSet
    template_name = "netbox_physical_clusters/physical_cluster/devices.html"
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
        permission="netbox_physical_clusters.view_devices",
        weight=600,
    )

    def get_children(self, request, parent):
        """Retrieves the devices that make up the cluster."""
        return Device.objects.restrict(request.user, "view").filter(physicalcluster=parent)


@register_model_view(PhysicalCluster, "edit")
class PhysicalClusterEditView(generic.ObjectEditView):
    """PhysicalCluster Type view.for editing."""

    queryset = PhysicalCluster.objects.all()
    form = forms.PhysicalClusterForm


@register_model_view(PhysicalCluster, "delete")
class PhysicalClusterDeleteView(generic.ObjectDeleteView):
    """PhysicalCluster Type view.for deletion."""

    queryset = PhysicalCluster.objects.all()


class PhysicalClusterBulkImportView(generic.BulkImportView):
    """PhysicalCluster view.for bulk import."""

    queryset = PhysicalCluster.objects.all()
    model_form = forms.PhysicalClusterImportForm


class PhysicalClusterBulkEditView(generic.BulkEditView):
    """PhysicalCluster view.for bulk edit."""

    queryset = PhysicalCluster.objects.all()
    filterset = filtersets.PhysicalClusterFilterSet
    table = tables.PhysicalClusterTable
    form = forms.PhysicalClusterBulkEditForm


class PhysicalClusterBulkDeleteView(generic.BulkDeleteView):
    """PhysicalCluster view.for bulk deletion."""

    queryset = PhysicalCluster.objects.all()
    filterset = filtersets.PhysicalClusterFilterSet
    table = tables.PhysicalClusterTable


@register_model_view(PhysicalCluster, "add_devices", path="devices/add")
class PhysicalClusterAddDevicesView(generic.ObjectEditView):
    """PhysicalCluster view.for managing the addition of devices to a cluster."""

    queryset = PhysicalCluster.objects.all()
    form = forms.PhysicalClusterAddDevicesForm
    template_name = "netbox_physical_clusters/cluster_add_devices.html"

    def get(self, request, pk):
        """Retrieve device list."""
        physicalcluster = get_object_or_404(self.queryset, pk=pk)
        form = self.form(physicalcluster, initial=request.GET)

        return render(
            request,
            self.template_name,
            {
                "cluster": physicalcluster,
                "form": form,
                "return_url": reverse("plugins:netbox_physical_clusters:physicalcluster", kwargs={"pk": pk}),
            },
        )

    def post(self, request, pk):
        """Add devices."""
        physicalcluster = get_object_or_404(self.queryset, pk=pk)
        form = self.form(physicalcluster, request.POST)

        if form.is_valid():
            device_pks = form.cleaned_data["devices"]
            with transaction.atomic():
                # Assign the selected Devices to the PhysicalCluster
                for device in Device.objects.filter(pk__in=device_pks):
                    physicalcluster.devices.add(device)
                    physicalcluster.save()

            messages.success(request, "Added {} devices to cluster {}".format(len(device_pks), physicalcluster))
            return redirect(physicalcluster.get_absolute_url())

        return render(
            request,
            self.template_name,
            {
                "cluster": physicalcluster,
                "form": form,
                "return_url": physicalcluster.get_absolute_url(),
            },
        )


@register_model_view(PhysicalCluster, "remove_devices", path="devices/remove")
class PhysicalClusterRemoveDevicesView(generic.ObjectEditView):
    """PhysicalCluster view.for managing the deletion of devices to a cluster."""

    queryset = PhysicalCluster.objects.all()
    form = forms.PhysicalClusterRemoveDevicesForm
    template_name = "generic/bulk_remove.html"

    def post(self, request, pk):
        """Removes teh specified device."""
        physicalcluster = get_object_or_404(self.queryset, pk=pk)

        if "_confirm" in request.POST:
            form = self.form(request.POST)
            if form.is_valid():
                device_pks = form.cleaned_data["pk"]
                with transaction.atomic():
                    # Remove the selected Devices from the PhysicalCluster
                    for device in Device.objects.filter(pk__in=device_pks):
                        physicalcluster.devices.remove(device)
                        physicalcluster.save()

                messages.success(
                    request, "Removed {} devices from cluster {}".format(len(device_pks), physicalcluster)
                )
                return redirect(physicalcluster.get_absolute_url())

        else:
            form = self.form(initial={"pk": request.POST.getlist("pk")})

        selected_objects = Device.objects.filter(pk__in=form.initial["pk"])
        device_table = DeviceTable(list(selected_objects), orderable=False)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "parent_obj": physicalcluster,
                "table": device_table,
                "obj_type_plural": "devices",
                "return_url": physicalcluster.get_absolute_url(),
            },
        )
