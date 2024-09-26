"""Define the urlpatterns for this plugin."""

from django.urls import include, path

from utilities.urls import get_model_urls
from . import views

urlpatterns = [
    # device group types
    path("device-group-types/", views.DeviceGroupTypeListView.as_view(), name="devicegrouptype_list"),
    path("device-group-types/add/", views.DeviceGroupTypeEditView.as_view(), name="devicegrouptype_add"),
    path("device-group-types/import/", views.DeviceGroupTypeBulkImportView.as_view(), name="devicegrouptype_import"),
    path("device-group-types/edit/", views.DeviceGroupTypeBulkEditView.as_view(), name="devicegrouptype_bulk_edit"),
    path(
        "device-group-types/delete/",
        views.DeviceGroupTypeBulkDeleteView.as_view(),
        name="devicegrouptype_bulk_delete",
    ),
    path("device-group-types/<int:pk>/", include(get_model_urls("netbox_device_groups", "devicegrouptype"))),
    # device-groups
    path("device-groups/", views.DeviceGroupListView.as_view(), name="devicegroup_list"),
    path("device-groups/add/", views.DeviceGroupEditView.as_view(), name="devicegroup_add"),
    path("device-groups/import/", views.DeviceGroupBulkImportView.as_view(), name="devicegroup_import"),
    path("device-groups/edit/", views.DeviceGroupBulkEditView.as_view(), name="devicegroup_bulk_edit"),
    path("device-groups/delete/", views.DeviceGroupBulkDeleteView.as_view(), name="devicegroup_bulk_delete"),
    path("device-groups/<int:pk>/", include(get_model_urls("netbox_device_groups", "devicegroup"))),
]
