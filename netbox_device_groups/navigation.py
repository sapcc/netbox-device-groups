"""Define the Navigation Menu."""

from extras.plugins import PluginMenu, PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_buttons = (
    PluginMenuItem(
        link_text="Device Groups",
        link="plugins:netbox_device_groups:devicegroup_list",
        permissions=["netbox_device_groups.view_devicegroup"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_device_groups:devicegroup_add",
                title="Add Device Group",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_device_groups.add_devicegroup"],
            ),
            PluginMenuButton(
                link="plugins:netbox_device_groups:devicegroup_import",
                title="Import Device Groups",
                icon_class="mdi mdi-upload",
                color=ButtonColorChoices.CYAN,
                permissions=["netbox_device_groups.add_devicegroup"],
            ),
        ),
    ),
    PluginMenuItem(
        link_text="Device Group Types",
        link="plugins:netbox_device_groups:devicegrouptype_list",
        permissions=["netbox_device_groups.view_devicegrouptype"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_device_groups:devicegrouptype_add",
                title="Add Device Group Type",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_device_groups.add_devicegrouptype"],
            ),
            PluginMenuButton(
                link="plugins:netbox_device_groups:devicegrouptype_import",
                title="Import Device Group Types",
                icon_class="mdi mdi-upload",
                color=ButtonColorChoices.CYAN,
                permissions=["netbox_device_groups.add_devicegrouptype"],
            ),
        ),
    ),
)

menu = PluginMenu(
    label="SAP",
    groups=(("Device Groups", menu_buttons),),
    icon_class="mdi mdi-black-mesa",
)
