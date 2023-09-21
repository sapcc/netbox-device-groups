 Installing the Plugin in Netbox

Here you will find detailed instructions on how to __install__ and __configure__ the Plugin.

## Prerequisites

- The plugin is compatible with Netbox 3.5.0 and higher.
- Databases supported: PostgreSQL

### Access Requirements

No external systems access is required to use this plugin.

## Install Guide

!!! note
    Plugins can be installed manually or using Python's `pip`. See the [netbox documentation](https://docs.netbox.dev/en/stable/plugins/) for more details. The pip package name for this plugin is [`netbox_plugin_extended_clusters`](https://pypi.org/project/netbox_plugin_extended_clusters/).

The plugin is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install netbox-plugin-extended-clusters
```

To ensure the extended cluster plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Netbox root directory (alongside `requirements.txt`) and list the `netbox_plugin_extended_clusters` package:

```shell
echo netbox-plugin-extended-clusters >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your Netbox configuration. The following block of code below shows the additional configuration required to be added to your `$NETBOX_ROOT/netbox/configuration.py` file:

- Append `"netbox_plugin_extended_clusters"` to the `PLUGINS` list.
- Append the `"netbox_plugin_extended_clusters"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
PLUGINS = [
    "netbox_plugin_extended_clusters",
]
PLUGINS_CONFIG = {
    "netbox_plugin_extended_clusters": {
        "USERNAME": "foo",
        "PASSWORD": "bar",
    }
}
```

## Post Install Steps

Once the Netbox configuration is updated, run the post install steps from the _Netbox Home_ to run migrations and clear any cache:

```shell
# Apply any database migrations
python3 netbox/manage.py migrate
# Trace any missing cable paths (not typically needed)
python3 netbox/manage.py trace_paths --no-input
# Collect static files
python3 netbox/manage.py collectstatic --no-input
# Delete any stale content types
python3 netbox/manage.py remove_stale_contenttypes --no-input
# Rebuild the search cache (lazily)
python3 netbox/manage.py reindex --lazy
# Delete any expired user sessions
python3 netbox/manage.py clearsessions
# Clear the cache
python3 netbox/manage.py clearcache
```

Then restart the Netbox services:

```shell
sudo systemctl restart netbox netbox-rq
```

## App Configuration

!!! warning "Developer Note - Remove Me!"
    Any configuration required to get the App set up. Edit the table below as per the examples provided.

The plugin behaviour can be controlled with the following list of settings:

| Key     | Example | Default | Description                          |
| ------- | ------ | -------- | ------------------------------------- |
| `example_setting` | `True` | `True` | A boolean to represent whether or not to use the example setting within the plugin. |
