"""Choice Sets for the plugin/."""

import graphene

from netbox.graphql.fields import ObjectField, ObjectListField
from .types import PhysicalClusterType, PhysicalClusterTypeType
from utilities.graphql_optimizer import gql_query_optimizer
from netbox_physical_clusters import models


class PhysicalClusterTypeQuery(graphene.ObjectType):
    """Query Definition fo the PhysicalClusterType."""

    physical_cluster_type = ObjectField(PhysicalClusterTypeType)
    physical_cluster_type_list = ObjectListField(PhysicalClusterTypeType)

    def resolve_cluster_type_list(root, info, **kwargs):
        """Optimize database access inside graphene queries."""
        return gql_query_optimizer(models.PhysicalClusterType.objects.all(), info)


class PhysicalClusterQuery(graphene.ObjectType):
    """Query Definition fo the PhysicalCluster."""

    physical_cluster_type = ObjectField(PhysicalClusterType)
    physical_cluster_type_list = ObjectListField(PhysicalClusterType)
