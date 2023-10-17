"""Define the urlpatterns for this plugin."""

from django.urls import include, path

from utilities.urls import get_model_urls
from . import views

urlpatterns = [
    # Physical cluster types
    path("cluster-types/", views.PhysicalClusterTypeListView.as_view(), name="physicalclustertype_list"),
    path("cluster-types/add/", views.PhysicalClusterTypeEditView.as_view(), name="physicalclustertype_add"),
    path(
        "cluster-types/import/", views.PhysicalClusterTypeBulkImportView.as_view(), name="physicalclustertype_import"
    ),
    path("cluster-types/edit/", views.PhysicalClusterTypeBulkEditView.as_view(), name="physicalclustertype_bulk_edit"),
    path(
        "cluster-types/delete/",
        views.PhysicalClusterTypeBulkDeleteView.as_view(),
        name="physicalclustertype_bulk_delete",
    ),
    path("cluster-types/<int:pk>/", include(get_model_urls("netbox_physical_clusters", "physicalclustertype"))),
    # Clusters
    path("clusters/", views.PhysicalClusterListView.as_view(), name="physicalcluster_list"),
    path("clusters/add/", views.PhysicalClusterEditView.as_view(), name="physicalcluster_add"),
    path("clusters/import/", views.PhysicalClusterBulkImportView.as_view(), name="physicalcluster_import"),
    path("clusters/edit/", views.PhysicalClusterBulkEditView.as_view(), name="physicalcluster_bulk_edit"),
    path("clusters/delete/", views.PhysicalClusterBulkDeleteView.as_view(), name="physicalcluster_bulk_delete"),
    path("clusters/<int:pk>/", include(get_model_urls("netbox_physical_clusters", "physicalcluster"))),
]
