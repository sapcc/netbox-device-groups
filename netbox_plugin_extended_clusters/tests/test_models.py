from django.db.utils import IntegrityError
from django.test import TestCase

from dcim.models import Site
from ..models import ExtendedClusterType

class ExtendedClusterTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name='Site 0', slug='site-0')

    def test_create_cluster_type(self):
        ExtendedClusterType.objects.create(name='Cluster Type 1', slug='cluster-type-1')
        cluster_type = ExtendedClusterType.objects.first()

        self.assertEqual(cluster_type.name, 'Cluster Type 1')
        self.assertEqual(cluster_type.slug, 'cluster-type-1')
