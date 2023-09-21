from extras.plugins import PluginConfig


__author__ = "Pat McLean"
__email__ = "patrick.mclean@sap.com"
__version__ = "0.0.1"

class ExtendedClusterListsConfig(PluginConfig):
    name = 'netbox_plugin_extended_clusters'
    verbose_name = 'Extended Clusters'
    description = 'A Netbox Plugin for extended cluster management'
    version = '0.1'
    author = __author__
    author_email = __email__
    version = __version__
    base_url = "ext-clusters"
    min_version = "3.5.0"


config = ExtendedClusterListsConfig