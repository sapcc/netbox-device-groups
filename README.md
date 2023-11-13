
A netbox plugin for managing multiple device group types by site

<a href="https://github.com/sapcc/netbox-device-groups/forks"><img src="https://img.shields.io/github/forks/sapcc/netbox-device-groups" alt="Forks Badge"/></a>
<a href="https://github.com/sapcc/netbox-device-groups/pulls"><img src="https://img.shields.io/github/issues-pr/sapcc/netbox-device-groups" alt="Pull Requests Badge"/></a>
<a href="https://github.com/sapcc/netbox-device-groups/issues"><img src="https://img.shields.io/github/issues/sapcc/netbox-device-groups" alt="Issues Badge"/></a>
<a href="https://github.com/sapcc/netbox-device-groups/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/sapcc/netbox-device-groups?color=2b9348"></a>
<a href="https://github.com/sapcc/netbox-device-groups/blob/master/LICENSE"><img src="https://img.shields.io/github/license/sapcc/netbox-device-groups?color=2b9348" alt="License Badge"/></a>

## Installing the Plugin in Netbox

### Prerequisites

- The plugin is compatible with Netbox 3.5.0 and higher.
- Databases supported: PostgreSQL
- Python supported : Python3 >= 3.10

### Install Guide

> NOTE: Plugins can be installed manually or using Python's `pip`. See the [netbox documentation](https://docs.netbox.dev/en/stable/plugins/) for more details. The pip package name for this plugin is [`netbox-device-groups`](https://pypi.org/project/netbox-device-groups/).

The plugin is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install netbox-device-groups
```

To ensure the device cluster plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Netbox root directory (alongside `requirements.txt`) and list the `netbox_device_groups` package:

```shell
echo netbox-device-groups >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your Netbox configuration. The following block of code below shows the additional configuration required to be added to your `$NETBOX_ROOT/netbox/configuration.py` file:

- Append `"netbox_device_groups"` to the `PLUGINS` list.
- Append the `"netbox_device_groups"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
PLUGINS = [
    "netbox_device_groups",
]
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
