from django.test import TestCase

from dcim.models import Region, Site, SiteGroup
from ipam.models import IPAddress
from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_physical_clusters.choices import PhysicalClusterStatusChoices
from netbox_physical_clusters.filtersets import PhysicalClusterFilterSet, PhysicalClusterTypeFilterSet
from netbox_physical_clusters.models import PhysicalCluster, PhysicalClusterType


class PhysicalClusterTypeTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = PhysicalClusterType.objects.all()
    filterset = PhysicalClusterTypeFilterSet

    @classmethod
    def setUpTestData(cls):
        cluster_types = (
            PhysicalClusterType(name="Test Type 1", description="cluster-type-1"),
            PhysicalClusterType(name="Test Type 2", description="cluster-type-2"),
            PhysicalClusterType(name="Test Type 3", description="cluster-type-3"),
        )
        PhysicalClusterType.objects.bulk_create(cluster_types)

    def test_name(self):
        params = {"name": ["Test Type 1", "Test Type 2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_description(self):
        params = {"description": ["cluster-type-1", "cluster-type-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class PhysicalClusterTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = PhysicalCluster.objects.all()
    filterset = PhysicalClusterFilterSet

    @classmethod
    def setUpTestData(cls):
        cluster_types = (
            PhysicalClusterType(name="Cluster Type 1", description="cluster-type-1"),
            PhysicalClusterType(name="Cluster Type 2", description="cluster-type-2"),
            PhysicalClusterType(name="Cluster Type 3", description="cluster-type-3"),
        )
        PhysicalClusterType.objects.bulk_create(cluster_types)

        regions = (
            Region(name="Test Region 1", slug="test-region-1"),
            Region(name="Test Region 2", slug="test-region-2"),
            Region(name="Test Region 3", slug="test-region-3"),
        )
        for r in regions:
            r.save()

        site_groups = (
            SiteGroup(name="Site Group 1", slug="site-group-1"),
            SiteGroup(name="Site Group 2", slug="site-group-2"),
            SiteGroup(name="Site Group 3", slug="site-group-3"),
        )
        for site_group in site_groups:
            site_group.save()

        sites = (
            Site(name="Test Site 1", slug="test-site-1", region=regions[0], group=site_groups[0]),
            Site(name="Test Site 2", slug="test-site-2", region=regions[1], group=site_groups[1]),
            Site(name="Test Site 3", slug="test-site-3", region=regions[2], group=site_groups[2]),
        )
        Site.objects.bulk_create(sites)

        tenant_groups = (
            TenantGroup(name="Tenant group 1", slug="tenant-group-1"),
            TenantGroup(name="Tenant group 2", slug="tenant-group-2"),
            TenantGroup(name="Tenant group 3", slug="tenant-group-3"),
        )
        for tenant_group in tenant_groups:
            tenant_group.save()

        tenants = (
            Tenant(name="Tenant 1", slug="tenant-1", group=tenant_groups[0]),
            Tenant(name="Tenant 2", slug="tenant-2", group=tenant_groups[1]),
            Tenant(name="Tenant 3", slug="tenant-3", group=tenant_groups[2]),
        )
        Tenant.objects.bulk_create(tenants)

        # Assign primary IPs for filtering
        ip_addresses = (
            IPAddress(address="192.0.2.1/24"),
            IPAddress(address="192.0.2.2/24"),
            IPAddress(address="192.0.2.3/24"),
        )
        IPAddress.objects.bulk_create(ip_addresses)

        clusters = (
            PhysicalCluster(
                name="Cluster 1",
                cluster_type=cluster_types[0],
                status=PhysicalClusterStatusChoices.STATUS_PLANNED,
                site=sites[0],
                tenant=tenants[0],
                primary_ip4=ip_addresses[0],
            ),
            PhysicalCluster(
                name="Cluster 2",
                cluster_type=cluster_types[1],
                status=PhysicalClusterStatusChoices.STATUS_STAGING,
                site=sites[1],
                tenant=tenants[1],
                primary_ip4=ip_addresses[1],
            ),
            PhysicalCluster(
                name="Cluster 3",
                cluster_type=cluster_types[2],
                status=PhysicalClusterStatusChoices.STATUS_ACTIVE,
                site=sites[2],
                tenant=tenants[2],
                primary_ip4=ip_addresses[2],
            ),
        )
        PhysicalCluster.objects.bulk_create(clusters)

    def test_name(self):
        params = {"name": ["Cluster 1", "Cluster 2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_site(self):
        sites = Site.objects.all()[:2]
        params = {"site_id": [sites[0].pk, sites[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_status(self):
        params = {"status": [PhysicalClusterStatusChoices.STATUS_PLANNED, PhysicalClusterStatusChoices.STATUS_STAGING]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_type(self):
        types = PhysicalClusterType.objects.all()[:2]
        params = {"cluster_type_id": [types[0].pk, types[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant(self):
        tenants = Tenant.objects.all()[:2]
        params = {"tenant_id": [tenants[0].pk, tenants[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"tenant": [tenants[0].slug, tenants[1].slug]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
