# Uninstall the Plugin from Netbox

Here you will find any steps necessary to cleanly remove the Plugin from your Netbox environment.

## Uninstall Guide

To uninstall the plugin, remove/comment out the configuration entries for the plugin in that were added in your `$NETBOX_ROOT/netbox/configuration.py` file, to the `PLUGINS` & `PLUGINS_CONFIG` sections.

```python
PLUGINS = [
    #"netbox_device_groups",
    'other plugins here',
]
PLUGINS_CONFIG = {
    # "netbox_device_groups": {
    #     "USERNAME": "foo",
    #     "PASSWORD": "bar",
    # }
    'other plugins here':{
        'other plugin': 'variable
    },
}
```

Now run the [post install steps](install.md/#post-install-steps) to clear the plugin from Netbox Cache.

## Database Clean-up

To ensure the database is clean after the plugin is removed is removed, drop all objects created by the plugin: `netbox_device_groups*`.
