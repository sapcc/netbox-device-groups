"""Define the Navigation Menu."""

from extras.plugins import PluginMenu, PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_buttons = (
    PluginMenuItem(
        link_text="Clusters",
        link="plugins:netbox_physical_clusters:physicalcluster_list",
        permissions=["netbox_physical_clusters.view_physicalcluster"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_physical_clusters:physicalcluster_add",
                title="Add Cluster",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_physical_clusters.add_physicalcluster"],
            ),
            PluginMenuButton(
                link="plugins:netbox_physical_clusters:physicalcluster_import",
                title="Import Cluster",
                icon_class="mdi mdi-upload",
                color=ButtonColorChoices.CYAN,
                permissions=["netbox_physical_clusters.add_physicalcluster"],
            ),
        ),
    ),
    PluginMenuItem(
        link_text="Cluster Types",
        link="plugins:netbox_physical_clusters:physicalclustertype_list",
        permissions=["netbox_physical_clusters.view_physicalclustertype"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_physical_clusters:physicalclustertype_add",
                title="Add Cluster Type",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_physical_clusters.add_physicalclustertype"],
            ),
            PluginMenuButton(
                link="plugins:netbox_physical_clusters:physicalclustertype_import",
                title="Import Cluster Type",
                icon_class="mdi mdi-upload",
                color=ButtonColorChoices.CYAN,
                permissions=["netbox_physical_clusters.add_physicalclustertype"],
            ),
        ),
    ),
)

menu = PluginMenu(
    label="SAP",
    groups=(("Physical Clusters", menu_buttons),),
    icon_class="mdi mdi-black-mesa",
)
