"""
Creates API endpoint URLs for the plugin.
"""

from netbox.api.routers import NetBoxRouter

from . import views

app_name = "netbox_plugin_extended_clusters"

router = NetBoxRouter()
router.register("extclustertype-lists", views.ExtendedClusterTypeListViewSet)
router.register("access-lists", views.AccessListViewSet)
router.register("interface-assignments", views.ACLInterfaceAssignmentViewSet)
router.register("standard-acl-rules", views.ACLStandardRuleViewSet)
router.register("extended-acl-rules", views.ACLExtendedRuleViewSet)

urlpatterns = router.urls
