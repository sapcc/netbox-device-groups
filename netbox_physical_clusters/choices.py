"""Choice Sets for the plugin/."""

from utilities.choices import ChoiceSet


class PhysicalClusterStatusChoices(ChoiceSet):
    """Choice set used by the Physical Cluster Model."""

    key = "PhysicalCluster.status"

    STATUS_PLANNED = "planned"
    STATUS_STAGING = "staging"
    STATUS_ACTIVE = "active"
    STATUS_MAINTENANCE = "maintenance"
    STATUS_UNHEALTHY = "unhealthy"
    STATUS_OFFLINE = "offline"

    CHOICES = [
        (STATUS_PLANNED, "Planned", "cyan"),
        (STATUS_STAGING, "Staging", "blue"),
        (STATUS_ACTIVE, "Active", "green"),
        (STATUS_MAINTENANCE, "Maintenance", "yellow"),
        (STATUS_UNHEALTHY, "Unhealthy", "grey"),
        (STATUS_OFFLINE, "Offline", "red"),
    ]
