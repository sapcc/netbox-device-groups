from importlib import metadata

from extras.plugins import PluginConfig


__version__ = metadata.version(__name__)
__author__ = "Pat McLean"
__email__ = "patrick.mclean@sap.com"


class PhysicalClusterConfig(PluginConfig):
    name = "netbox_physical_clusters"
    verbose_name = "NetBox Physical Clusters"
    description = "A Netbox Plugin for physical cluster management"
    author = __author__
    author_email = __email__
    version = __version__
    base_url = "clusters"
    min_version = "3.5.0"


config = PhysicalClusterConfig
