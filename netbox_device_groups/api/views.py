"""API Viewsets for the plugin."""

from django.http import JsonResponse
from rest_framework.routers import APIRootView

from dcim.models import Device
from netbox.api.viewsets import NetBoxModelViewSet
from utilities.utils import count_related

from netbox_device_groups import DeviceGroupConfig
from netbox_device_groups import filtersets
from netbox_device_groups.models import DeviceGroup, DeviceGroupType
from . import serializers


def get_version(request):
    """Returns the version of the plugi."""
    config = DeviceGroupConfig
    return JsonResponse(
        {
            config.name: {
                "verbose_name": config.verbose_name,
                "description": config.description,
                "author": config.author,
                "author_email": config.author_email,
                "version": config.version,
                "min_netbox_version": config.min_version,
            }
        }
    )


class DeviceGroupRootView(APIRootView):
    """Device Groups API root view."""

    def get_view_name(self):
        """Return the Root View Name."""
        return " Device Groups"


class DeviceGroupTypeViewSet(NetBoxModelViewSet):
    """A Viewset for the DeviceGroupType."""

    queryset = DeviceGroupType.objects.all().prefetch_related("tags")
    serializer_class = serializers.DeviceGroupTypeSerializer
    filterset_class = filtersets.DeviceGroupTypeFilterSet


class DeviceGroupViewSet(NetBoxModelViewSet):
    """A Viewset for the DeviceGroup."""

    queryset = DeviceGroup.objects.prefetch_related("cluster_type", "tenant", "site", "tags", "devices").annotate(
        device_count=count_related(Device, "cluster"),
    )
    serializer_class = serializers.DeviceGroupSerializer
    filterset_class = filtersets.DeviceGroupFilterSet
