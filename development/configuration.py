import os

#########################
#                       #
# Development  settings #
#                       #
#########################
BANNER_TOP = "Netbox Plugin - Device Groups"
BANNER_BOTTOM = BANNER_TOP
BANNER_LOGIN = BANNER_TOP
LOGIN_REQUIRED = False
# Date/time formatting. See the following link for supported formats:
# https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
DATE_FORMAT = "N j, Y"
SHORT_DATE_FORMAT = "Y-m-d"
TIME_FORMAT = "g:i a"
SHORT_TIME_FORMAT = "H:i:s"
DATETIME_FORMAT = "N j, Y g:i a"
SHORT_DATETIME_FORMAT = "Y-m-d H:i"

# exclude all objects from view permissions
EXEMPT_VIEW_PERMISSIONS = ["*"]


ALLOWED_HOSTS = os.getenv("NETBOX_ALLOWED_HOSTS", "*").split(" ")
CHANGELOG_RETENTION = 1
DATABASE = {
    "NAME": os.environ.get("NETBOX_DB_NAME", "netbox"),
    "USER": os.environ.get("NETBOX_DB_USER", "netbox"),
    "PASSWORD": os.environ.get("NETBOX_DB_PASSWORD", "netbox"),
    "HOST": os.environ.get("NETBOX_DB_HOST", "postgres"),
    "PORT": os.environ.get("NETBOX_DB_PORT", "5432"),
}

SECRET_KEY = os.environ.get("NETBOX_SECRET_KEY", "secret-secret-secret-secret-secret-secret-secret-secret")

REDIS = {
    "tasks": {
        "HOST": os.environ.get("REDIS_HOST", "redis"),
        "PORT": 6379,
        "PASSWORD": os.environ.get("REDIS_PASSWORD", "redis"),
        "DATABASE": 0,
        "SSL": False,
    },
    "caching": {
        "HOST": os.environ.get("REDIS_HOST", "redis"),
        "PORT": 6379,
        "PASSWORD": os.environ.get("REDIS_PASSWORD", "redis"),
        "DATABASE": 1,
        "SSL": False,
    },
}

DEBUG = True
DEVELOPER = True

INTERNAL_IPS = ("0.0.0.0", "127.0.0.1", "::1")

PLUGINS = [
    "netbox_device_groups",
]
PLUGINS_CONFIG = {
    # "netbox_device_groups": {
    #     "USERNAME": "foo",
    #     "PASSWORD": "bar",
    # }
}

SCRIPTS_ROOT = "scripts"
