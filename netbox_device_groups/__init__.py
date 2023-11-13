from importlib import metadata

from extras.plugins import PluginConfig


__version__ = metadata.version(__name__)
__author__ = "Pat McLean"
__email__ = "patrick.mclean@sap.com"


class DeviceGroupConfig(PluginConfig):
    name = "netbox_device_groups"
    verbose_name = "NetBox Device Groups"
    description = "A Netbox Plugin to allow logical grouping of devices by a defined type"
    author = __author__
    author_email = __email__
    version = __version__
    base_url = "device-groups"
    min_version = "3.5.0"


config = DeviceGroupConfig
