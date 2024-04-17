# Upgrading the Plugin

Here you will find any steps necessary to upgrade the plugin in your Netbox environment.

## Upgrade Guide

```shell
pip install --upgrade netbox-device-groups
```

When a new release comes out it may be necessary to run a migration of the database to account for any changes in the data models used by this plugin,  after updating the `netbox-device-groups` package via `pip`.

Run the post upgrade steps from the _Netbox Home_ to run migrations, and clear any cache:

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
