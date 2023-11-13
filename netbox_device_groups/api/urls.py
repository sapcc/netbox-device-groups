"""API routes for the plugin/."""
from django.urls import path

from netbox.api.routers import NetBoxRouter
from . import views


router = NetBoxRouter()
router.APIRootView = views.DeviceGroupRootView

router.register("device-group-types", views.DeviceGroupTypeViewSet)
router.register("device-groups", views.DeviceGroupViewSet)

urlpatterns = [
    path("version/", views.get_version),
]


urlpatterns += router.urls
