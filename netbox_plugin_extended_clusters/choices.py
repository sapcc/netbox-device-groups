"""
Defines the various choices to be used by the models, forms, and other plugin specifics.
"""

from utilities.choices import ChoiceSet

__all__ = (
    "ACLActionChoices",
    "ACLAssignmentDirectionChoices",
    "ACLProtocolChoices",
    "ACLRuleActionChoices",
    "ACLTypeChoices",
    "ACLProtocolChoices",
)


class ACLActionChoices(ChoiceSet):
    """
    Defines the choices availble for the Access Lists plugin specific to ACL default_action.
    """

    ACTION_DENY = "deny"
    ACTION_PERMIT = "permit"
    ACTION_REJECT = "reject"

    CHOICES = [
        (ACTION_DENY, "Deny", "red"),
        (ACTION_PERMIT, "Permit", "green"),
        (ACTION_REJECT, "Reject (Reset)", "orange"),
    ]


class ACLRuleActionChoices(ChoiceSet):
    """
    Defines the choices availble for the Access Lists plugin specific to ACL rule actions.
    """

    ACTION_DENY = "deny"
    ACTION_PERMIT = "permit"
    ACTION_REMARK = "remark"

    CHOICES = [
        (ACTION_DENY, "Deny", "red"),
        (ACTION_PERMIT, "Permit", "green"),
        (ACTION_REMARK, "Remark", "blue"),
    ]


class ACLAssignmentDirectionChoices(ChoiceSet):
    """
    Defines the direction of the application of the ACL on an associated interface.
    """

    DIRECTION_INGRESS = "ingress"
    DIRECTION_EGRESS = "egress"

    CHOICES = [
        (DIRECTION_INGRESS, "Ingress", "blue"),
        (DIRECTION_EGRESS, "Egress", "purple"),
    ]


class ACLTypeChoices(ChoiceSet):
    """
    Defines the choices availble for the Access Lists plugin specific to ACL type.
    """

    TYPE_STANDARD = "standard"
    TYPE_EXTENDED = "extended"

    CHOICES = [
        (TYPE_EXTENDED, "Extended", "purple"),
        (TYPE_STANDARD, "Standard", "blue"),
    ]


class ACLProtocolChoices(ChoiceSet):
    """
    Defines the choices availble for the Access Lists plugin specific to ACL Rule protocol.
    """

    PROTOCOL_ICMP = "icmp"
    PROTOCOL_TCP = "tcp"
    PROTOCOL_UDP = "udp"

    CHOICES = [
        (PROTOCOL_ICMP, "ICMP", "purple"),
        (PROTOCOL_TCP, "TCP", "blue"),
        (PROTOCOL_UDP, "UDP", "orange"),
    ]


class ExtendedClusterStatusChoices(ChoiceSet):
    """Defines the choices available for the  the Extended Cluster specific to status."""

    key = 'ExtendedCluster.status'

    STATUS_OFFLINE = 'offline'
    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_STAGED = 'maintenance'
    STATUS_FAILED = 'failed'

    CHOICES = [
        (STATUS_OFFLINE, 'Offline', 'gray'),
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_STAGED, 'Maintenance', 'blue'),
        (STATUS_FAILED, 'Failed', 'red'),
    ]
