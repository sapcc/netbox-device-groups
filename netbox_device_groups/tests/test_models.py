"""Test Models."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Location, Manufacturer, Site
from netbox_device_groups import models


class TestDeviceGroupTypeObjects(TestCase):
    """Test DeviceGroupType model."""

    def test_create_physical_cluster_type_valid(self):
        """Successfully create various DeviceGroupType records."""

        physical_cluster1 = models.DeviceGroupType(name="Test Type One", description="Test Type One")
        physical_cluster1.validated_save()
        physical_cluster2 = models.DeviceGroupType(name="Test Type Two", description="Test Type Row")
        physical_cluster2.validated_save()

    def test_create_physical_cluster_type_invalid_duplicate_name(self):
        """Only one DeviceGroupType with a given name can be created."""

        models.DeviceGroupType(name="Test Type One", description="Test Type One").validated_save()
        with self.assertRaises(ValidationError):
            models.DeviceGroupType(name="Test Type One", description="Test Type One").validated_save()


class TestDeviceGroupObjects(TestCase):
    """Test DeviceGroup model."""

    @classmethod
    def setUpTestData(cls):
        cluster_type = models.DeviceGroupType.objects.create(
            name="DeviceDevice Group Type 1", description="cluster-type-1"
        )
        models.DeviceGroup.objects.create(name="DeviceCluster 1", cluster_type=cluster_type)

    def test_create_cluster(self):
        manufacturer = Manufacturer.objects.create(name="Manufacturer 1", slug="manufacturer-1")
        device_type = DeviceType.objects.create(manufacturer=manufacturer, model="Device Type 1", slug="device-type-1")
        device_role = DeviceRole.objects.create(name="Device Role 1", slug="device-role-1", color="ff0000")
        site_a = Site.objects.create(name="Site A", slug="site-a")
        location_a1 = Location(site=site_a, name="Location A1", slug="location-a1")
        location_a1.save()
        location_a2 = Location(site=site_a, parent=location_a1, name="Location A2", slug="location-a2")
        location_a2.save()

        device1 = Device.objects.create(
            site=site_a, location=location_a1, name="Device 1", device_type=device_type, device_role=device_role
        )
        device2 = Device.objects.create(
            site=site_a, location=location_a2, name="Device 2", device_type=device_type, device_role=device_role
        )
        test_cluster = models.DeviceGroup.objects.first()
        test_cluster.devices.add(device1)
        test_cluster.devices.add(device2)
        test_cluster.site = site_a

        self.assertEqual(test_cluster.devices.count(), 2)
        self.assertEqual(test_cluster.devices.first().site, site_a)
        self.assertEqual(test_cluster.devices.first().location, location_a1)
        self.assertEqual(test_cluster.devices.first().device_role, device_role)
