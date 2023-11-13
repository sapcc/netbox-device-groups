"""Plugin Form tests."""

from django.test import TestCase

from netbox_device_groups.forms import DeviceGroupTypeForm
from netbox_device_groups.models import DeviceGroupType


class DeviceTestCase(TestCase):
    """Test DeviceGroupType Form."""

    @classmethod
    def setUpTestData(cls):
        """Setup the device group Type object for the test"""

        DeviceGroupType.objects.create(name="Device Group Type 1", description="cluster-type-1")

    def test_racked_device(self):
        """Test that a device group Type object is saved by teh form."""

        form = DeviceGroupTypeForm(
            data={
                "name": "New Test CLuster Type",
                "description": "Describing the New Test CLuster Type",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
