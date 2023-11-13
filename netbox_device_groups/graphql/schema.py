"""Choice Sets for the plugin/."""

import graphene

from netbox.graphql.fields import ObjectField, ObjectListField
from .types import DeviceGroupType, DeviceGroupTypeType
from utilities.graphql_optimizer import gql_query_optimizer
from netbox_device_groups import models


class DeviceGroupTypeQuery(graphene.ObjectType):
    """Query Definition fo the DeviceGroupType."""

    physical_cluster_type = ObjectField(DeviceGroupTypeType)
    physical_cluster_type_list = ObjectListField(DeviceGroupTypeType)

    def resolve_cluster_type_list(root, info, **kwargs):
        """Optimize database access inside graphene queries."""
        return gql_query_optimizer(models.DeviceGroupType.objects.all(), info)


class DeviceGroupQuery(graphene.ObjectType):
    """Query Definition fo the DeviceGroup."""

    physical_cluster_type = ObjectField(DeviceGroupType)
    physical_cluster_type_list = ObjectListField(DeviceGroupType)
