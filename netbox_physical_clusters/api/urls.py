"""API routes for the plugin/."""
from django.urls import path

from netbox.api.routers import NetBoxRouter
from . import views


router = NetBoxRouter()
router.APIRootView = views.PhysicalClusterRootView

router.register("cluster-types", views.PhysicalClusterTypeViewSet)
router.register("clusters", views.PhysicalClusterViewSet)

urlpatterns = [
    path("version/", views.get_version),
]


urlpatterns += router.urls
