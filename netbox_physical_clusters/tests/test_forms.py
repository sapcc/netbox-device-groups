"""Plugin Form tests."""

from django.test import TestCase

from netbox_physical_clusters.forms import PhysicalClusterTypeForm
from netbox_physical_clusters.models import PhysicalClusterType


class DeviceTestCase(TestCase):
    """Test PhysicalClusterType Form."""

    @classmethod
    def setUpTestData(cls):
        """Setup the Physical CLuster Type object for the test"""

        PhysicalClusterType.objects.create(name="Cluster Type 1", description="cluster-type-1")

    def test_racked_device(self):
        """Test that a Physical CLuster Type object is saved by teh form."""

        form = PhysicalClusterTypeForm(
            data={
                "name": "New Test CLuster Type",
                "description": "Describing the New Test CLuster Type",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
