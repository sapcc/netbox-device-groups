"""
Define the plugin menu buttons & the plugin navigation bar entries.
"""

from extras.plugins import PluginMenu, PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices



#
# Define plugin menu buttons
#
menu_buttons = (
    PluginMenuItem(
        link="plugins:netbox_plugin_extended_clusters:accesslist_list",
        link_text="Extended Cluster Types",
        permissions=["netbox_plugin_extended_clusters.view_accesslist"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_plugin_extended_clusters:accesslist_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_plugin_extended_clusters.add_accesslist"],
            ),
        ),
    ),
)

menu = PluginMenu(
    label="SAP",
    groups=(("Extended Clusters", menu_buttons),),
    icon_class="mdi mdi-unity",
)
