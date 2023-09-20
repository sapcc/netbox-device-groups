from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from utilities.testing import APITestCase, APIViewTestCases

from netbox_plugin_extended_clusters.choices import *
from netbox_plugin_extended_clusters.models import *


class AppTest(APITestCase):
    def test_root(self):
        url = reverse("plugins-api:netbox_plugin_extended_clusters-api:api-root")
        response = self.client.get(f"{url}?format=api", **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ACLTestCase(
    APIViewTestCases.APIViewTestCase,
):
    """Test the AccessList Test"""

    model = AccessList
    view_namespace = "plugins-api:netbox_plugin_extended_clusters"
    brief_fields = ["display", "id", "name", "url"]

    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name="Site 1", slug="site-1")
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer 1",
            slug="manufacturer-1",
        )
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer,
            model="Device Type 1",
        )
        device_role = DeviceRole.objects.create(
            name="Device Role 1",
            slug="device-role-1",
        )
        device = Device.objects.create(
            name="Device 1",
            site=site,
            device_type=device_type,
            device_role=device_role,
        )

        access_lists = (
            AccessList(
                name="test_acl_1",
                assigned_object_type=ContentType.objects.get_for_model(Device),
                assigned_object_id=device.id,
                type=ACLTypeChoices.TYPE_STANDARD,
                default_action=ACLActionChoices.ACTION_DENY,
            ),
            AccessList(
                name="test_acl_2",
                assigned_object_type=ContentType.objects.get_for_model(Device),
                assigned_object_id=device.id,
                type=ACLTypeChoices.TYPE_STANDARD,
                default_action=ACLActionChoices.ACTION_DENY,
            ),
            AccessList(
                name="test_acl_3",
                assigned_object_type=ContentType.objects.get_for_model(Device),
                assigned_object_id=device.id,
                type=ACLTypeChoices.TYPE_STANDARD,
                default_action=ACLActionChoices.ACTION_DENY,
            ),
        )
        AccessList.objects.bulk_create(access_lists)

        cls.create_data = [
            {
                "name": "test_acl_4",
                "assigned_object_type": "dcim.device",
                "assigned_object_id": device.id,
                "type": ACLTypeChoices.TYPE_STANDARD,
                "default_action": ACLActionChoices.ACTION_DENY,
            },
            {
                "name": "test_acl_5",
                "assigned_object_type": "dcim.device",
                "assigned_object_id": device.id,
                "type": ACLTypeChoices.TYPE_EXTENDED,
                "default_action": ACLActionChoices.ACTION_DENY,
            },
            {
                "name": "test_acl_6",
                "assigned_object_type": "dcim.device",
                "assigned_object_id": device.id,
                "type": ACLTypeChoices.TYPE_STANDARD,
                "default_action": ACLActionChoices.ACTION_DENY,
            },
        ]
