"""API routes for the plugin/."""

from netbox.api.routers import NetBoxRouter
from . import views


router = NetBoxRouter()
router.APIRootView = views.PhysicalClusterRootView

router.register("cluster-types", views.PhysicalClusterTypeViewSet)
router.register("clusters", views.PhysicalClusterViewSet)
urlpatterns = router.urls
